#!/usr/bin/env python3
"""
dify_sync.py — upsert changed Hugo markdown posts into a Dify Knowledge Base.

Design notes (see project doc ordliste-mapping.md for the vocabulary):
- change detection is done via a content hash per file, not `git diff` — this
  means the script doesn't need git history at all, just the current files on
  disk plus the mapping file from the last run. Simpler and more robust.
- create-or-update is an upsert; re-running this script on unchanged content
  is a no-op, which is what makes the job idempotent (safe to re-run/retry).
- every Dify API call is wrapped in retry + exponential backoff + jitter to
  respect the free tier's rate limit (10 knowledge requests/min on Sandbox).

Usage (as a GitHub Actions step):
    DIFY_API_KEY=... DIFY_DATASET_ID=... python scripts/dify_sync.py

Config via environment variables:
    DIFY_API_KEY      required — Dify *dataset* API key (not an app key)
    DIFY_DATASET_ID   required — target knowledge base / dataset id
    DIFY_BASE_URL     optional — default https://api.dify.ai/v1
                       (point at your own instance if self-hosting later)
    CONTENT_DIRS      optional — comma-separated, default "content/posts,content/devlog"
                       (paths relative to repo root, matching this repo's structure)
    MAP_FILE          optional — default "dify-sync-map.json"

Note: `_index.md` / `index.md` section-listing pages are skipped — they're
navigation scaffolding, not article content worth putting in the knowledge base.
"""

import hashlib
import json
import logging
import os
import random
import sys
import time
from pathlib import Path

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("dify_sync")

API_KEY = os.environ.get("DIFY_API_KEY")
DATASET_ID = os.environ.get("DIFY_DATASET_ID")
BASE_URL = os.environ.get("DIFY_BASE_URL", "https://api.dify.ai/v1").rstrip("/")
CONTENT_DIRS = [
    Path(d.strip())
    for d in os.environ.get("CONTENT_DIRS", "content/posts,content/devlog").split(",")
    if d.strip()
]
MAP_FILE = Path(os.environ.get("MAP_FILE", "dify-sync-map.json"))
SKIP_NAMES = {"_index.md", "index.md"}

MAX_RETRIES = 5
BASE_DELAY = 2.0  # seconds


def require_config():
    missing = [n for n, v in [("DIFY_API_KEY", API_KEY), ("DIFY_DATASET_ID", DATASET_ID)] if not v]
    if missing:
        log.error("Missing required env vars: %s", ", ".join(missing))
        sys.exit(1)


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_map() -> dict:
    if MAP_FILE.exists():
        return json.loads(MAP_FILE.read_text(encoding="utf-8"))
    return {}


def save_map(mapping: dict) -> None:
    MAP_FILE.write_text(json.dumps(mapping, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def call_with_backoff(method: str, url: str, **kwargs) -> requests.Response:
    """Retry + exponential backoff + jitter, with rate-limit (429) awareness."""
    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {API_KEY}"
    for attempt in range(1, MAX_RETRIES + 1):
        resp = requests.request(method, url, headers=headers, timeout=30, **kwargs)
        if resp.status_code < 400:
            return resp
        if resp.status_code == 429 or resp.status_code >= 500:
            retry_after = resp.headers.get("Retry-After")
            delay = float(retry_after) if retry_after else BASE_DELAY * (2 ** (attempt - 1))
            delay += random.uniform(0, 1)  # jitter
            log.warning(
                "%s %s -> %s (attempt %d/%d), backing off %.1fs",
                method, url, resp.status_code, attempt, MAX_RETRIES, delay,
            )
            time.sleep(delay)
            continue
        # non-retryable client error (400, 401, 404, ...)
        log.error("%s %s -> %s: %s", method, url, resp.status_code, resp.text[:300])
        resp.raise_for_status()
    resp.raise_for_status()  # exhausted retries
    return resp  # unreachable, keeps type-checkers happy


def create_document(name: str, text: str) -> str:
    url = f"{BASE_URL}/datasets/{DATASET_ID}/document/create_by_text"
    payload = {
        "name": name,
        "text": text,
        "indexing_technique": "high_quality",
        "process_rule": {"mode": "automatic"},
    }
    resp = call_with_backoff("POST", url, json=payload)
    data = resp.json()
    doc_id = data.get("document", {}).get("id") or data.get("document_id")
    if not doc_id:
        raise RuntimeError(f"Unexpected create response, no document id: {data}")
    return doc_id


def update_document(document_id: str, name: str, text: str) -> None:
    url = f"{BASE_URL}/datasets/{DATASET_ID}/documents/{document_id}/update_by_text"
    payload = {"name": name, "text": text}
    call_with_backoff("POST", url, json=payload)


def delete_document(document_id: str) -> None:
    url = f"{BASE_URL}/datasets/{DATASET_ID}/documents/{document_id}"
    call_with_backoff("DELETE", url)


def main() -> int:
    require_config()

    missing_dirs = [str(d) for d in CONTENT_DIRS if not d.exists()]
    if missing_dirs:
        log.error("CONTENT_DIRS not found: %s — check the paths", ", ".join(missing_dirs))
        return 1

    mapping = load_map()
    on_disk = {
        str(p): p
        for d in CONTENT_DIRS
        for p in d.rglob("*.md")
        if p.name not in SKIP_NAMES
    }

    created = updated = skipped = deleted = failed = 0

    # creates / updates
    for rel_path, path in sorted(on_disk.items()):
        text = path.read_text(encoding="utf-8")
        h = content_hash(text)
        entry = mapping.get(rel_path)

        if entry and entry.get("content_hash") == h:
            skipped += 1
            continue

        name = str(path)  # e.g. "content/posts/2026-03-13-erd-data-model.md" — unique across dirs
        try:
            if entry and entry.get("document_id"):
                log.info("Updating %s (content changed)", rel_path)
                update_document(entry["document_id"], name, text)
                mapping[rel_path] = {"document_id": entry["document_id"], "content_hash": h}
                updated += 1
            else:
                log.info("Creating %s (new file)", rel_path)
                doc_id = create_document(name, text)
                mapping[rel_path] = {"document_id": doc_id, "content_hash": h}
                created += 1
            save_map(mapping)  # persist after every successful call, not just at the end
        except Exception:
            log.exception("Failed to sync %s", rel_path)
            failed += 1

    # deletes — files that used to exist but don't anymore
    for rel_path in list(mapping.keys()):
        if rel_path not in on_disk:
            doc_id = mapping[rel_path].get("document_id")
            try:
                log.info("Deleting %s (removed from repo)", rel_path)
                if doc_id:
                    delete_document(doc_id)
                del mapping[rel_path]
                deleted += 1
                save_map(mapping)
            except Exception:
                log.exception("Failed to delete %s", rel_path)
                failed += 1

    log.info(
        "Done. created=%d updated=%d skipped=%d deleted=%d failed=%d",
        created, updated, skipped, deleted, failed,
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
