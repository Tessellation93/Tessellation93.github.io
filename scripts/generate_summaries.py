#!/usr/bin/env python3
"""
generate_summaries.py — draft a 1-2 sentence `summary:` for posts that lack one.

Same design as scripts/dify_sync.py:
- change detection is a content hash per file stored in a JSON map, not `git diff`
  — so the script only needs the files on disk plus the map from the last run.
  Re-running on unchanged content is a no-op, which keeps the job idempotent.
- the hash is taken over the article *body only* (everything after the closing
  frontmatter `---`), so writing the generated `summary:` line back into the
  frontmatter does not make the file look "changed" on the next run.
- every Groq API call is wrapped in retry + exponential backoff + jitter.

Only published posts are touched: a file with `draft: true` in its frontmatter,
or one that already has a `summary:` key, is skipped.

The script never publishes anything — it just edits files on disk. The workflow
(.github/workflows/generate-summaries.yml) opens a PR with the result for review.

Usage (as a GitHub Actions step):
    GROQ_API_KEY=... python scripts/generate_summaries.py

Config via environment variables:
    GROQ_API_KEY   required — same key the devlog-draft agent uses
    GROQ_MODEL     optional — default "llama-3.1-8b-instant"
    GROQ_BASE_URL  optional — default https://api.groq.com/openai/v1
    CONTENT_DIRS   optional — comma-separated, default "content/posts,content/devlog"
    MAP_FILE       optional — default "summary-map.json"

Note: `_index.md` / `index.md` section-listing pages are skipped — they're
navigation scaffolding, not articles.
"""

import hashlib
import json
import logging
import os
import random
import re
import sys
import time
from pathlib import Path

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("generate_summaries")

API_KEY = os.environ.get("GROQ_API_KEY")
MODEL = os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant")
BASE_URL = os.environ.get("GROQ_BASE_URL", "https://api.groq.com/openai/v1").rstrip("/")
CONTENT_DIRS = [
    Path(d.strip())
    for d in os.environ.get("CONTENT_DIRS", "content/posts,content/devlog").split(",")
    if d.strip()
]
MAP_FILE = Path(os.environ.get("MAP_FILE", "summary-map.json"))
SKIP_NAMES = {"_index.md", "index.md"}

# how much of the post body to send to the model — enough for context, not the
# whole thing, to keep token use and latency down
BODY_CHAR_BUDGET = 6000

MAX_RETRIES = 5
BASE_DELAY = 2.0  # seconds
MIN_INTERVAL = 2.0  # seconds between calls — Groq's free tier is rate limited
_last_call_at = 0.0

SYSTEM_PROMPT = (
    "You write short summaries for the index pages of a software development "
    "portfolio blog. Given one post, reply with a plain-language summary of "
    "1 to 2 sentences (about 40 words maximum) describing what the post is "
    "about. Write in the third person. No preamble, no markdown, no quotes, "
    "no bullet points — just the summary sentences."
)


def require_config():
    if not API_KEY:
        log.error("Missing required env var: GROQ_API_KEY")
        sys.exit(1)


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_map() -> dict:
    if MAP_FILE.exists():
        return json.loads(MAP_FILE.read_text(encoding="utf-8"))
    return {}


def save_map(mapping: dict) -> None:
    MAP_FILE.write_text(json.dumps(mapping, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def split_frontmatter(text: str):
    """Return (frontmatter_lines, body) for a file that starts with a `---`
    YAML frontmatter block. Returns (None, text) if there is no such block.

    frontmatter_lines is the list of lines *between* the `---` fences (without
    the fences themselves); body is everything after the closing fence,
    verbatim.
    """
    if not text.startswith("---\n") and text != "---":
        return None, text
    lines = text.split("\n")
    # lines[0] == "---"; find the closing fence
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm = lines[1:i]
            body = "\n".join(lines[i + 1:])
            return fm, body
    return None, text


def frontmatter_has_key(fm_lines, key: str) -> bool:
    pat = re.compile(rf"^\s*{re.escape(key)}\s*:", re.IGNORECASE)
    return any(pat.match(line) for line in fm_lines)


def frontmatter_is_draft(fm_lines) -> bool:
    pat = re.compile(r"^\s*draft\s*:\s*true\s*(#.*)?$", re.IGNORECASE)
    return any(pat.match(line) for line in fm_lines)


def frontmatter_title(fm_lines) -> str:
    for line in fm_lines:
        m = re.match(r"^\s*title\s*:\s*(.+?)\s*$", line)
        if m:
            return m.group(1).strip().strip('"').strip("'")
    return ""


def yaml_double_quote(value: str) -> str:
    """Escape a string for a YAML double-quoted scalar."""
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def insert_summary(text: str, fm_lines, summary: str) -> str:
    """Return `text` with a `summary:` line inserted into its frontmatter block.

    Inserted right after the `title:` line if there is one, otherwise as the
    last frontmatter line. Only the frontmatter is touched; the body is left
    byte-for-byte identical.
    """
    lines = text.split("\n")
    # frontmatter body occupies lines[1 .. close-1]; find the closing fence
    close = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")

    new_line = f"summary: {yaml_double_quote(summary)}"

    insert_at = close  # default: just before the closing fence
    for i in range(1, close):
        if re.match(r"^\s*title\s*:", lines[i]):
            insert_at = i + 1
            break

    lines.insert(insert_at, new_line)
    return "\n".join(lines)


def _is_rate_limited(resp: requests.Response) -> bool:
    return resp.status_code == 429


def call_with_backoff(method: str, url: str, **kwargs) -> requests.Response:
    """Retry + exponential backoff + jitter, with rate-limit (429) and 5xx
    awareness. Also self-throttles to MIN_INTERVAL between calls."""
    global _last_call_at
    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {API_KEY}"
    for attempt in range(1, MAX_RETRIES + 1):
        elapsed = time.monotonic() - _last_call_at
        if elapsed < MIN_INTERVAL:
            time.sleep(MIN_INTERVAL - elapsed)
        resp = requests.request(method, url, headers=headers, timeout=60, **kwargs)
        _last_call_at = time.monotonic()
        if resp.status_code < 400:
            return resp
        if _is_rate_limited(resp) or resp.status_code >= 500:
            retry_after = resp.headers.get("Retry-After")
            delay = float(retry_after) if retry_after else max(BASE_DELAY * (2 ** (attempt - 1)), MIN_INTERVAL)
            delay += random.uniform(0, 1)  # jitter
            log.warning(
                "%s %s -> %s (attempt %d/%d), backing off %.1fs",
                method, url, resp.status_code, attempt, MAX_RETRIES, delay,
            )
            time.sleep(delay)
            continue
        log.error("%s %s -> %s: %s", method, url, resp.status_code, resp.text[:300])
        resp.raise_for_status()
    resp.raise_for_status()  # exhausted retries
    return resp  # unreachable, keeps type-checkers happy


def clean_summary(raw: str) -> str:
    s = raw.strip()
    # models sometimes wrap the whole thing in quotes
    if len(s) >= 2 and s[0] == s[-1] and s[0] in {'"', "'"}:
        s = s[1:-1].strip()
    # collapse any internal whitespace / newlines to single spaces
    s = re.sub(r"\s+", " ", s)
    return s


def generate_summary(title: str, body: str) -> str:
    excerpt = body.strip()
    if len(excerpt) > BODY_CHAR_BUDGET:
        excerpt = excerpt[:BODY_CHAR_BUDGET].rsplit(" ", 1)[0] + " …"
    user_content = f"Title: {title}\n\n{excerpt}"
    payload = {
        "model": MODEL,
        "temperature": 0.3,
        "max_tokens": 160,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
    }
    resp = call_with_backoff("POST", f"{BASE_URL}/chat/completions", json=payload)
    data = resp.json()
    try:
        raw = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise RuntimeError(f"Unexpected Groq response: {data}")
    summary = clean_summary(raw)
    if not summary:
        raise RuntimeError("Groq returned an empty summary")
    return summary


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

    generated = skipped = pruned = failed = 0

    for rel_path, path in sorted(on_disk.items()):
        text = path.read_text(encoding="utf-8")
        fm_lines, body = split_frontmatter(text)

        if fm_lines is None:
            log.info("Skipping %s (no frontmatter block)", rel_path)
            skipped += 1
            continue
        if frontmatter_has_key(fm_lines, "summary"):
            # the file itself is the source of truth — once it has a summary we
            # leave it alone; drop any now-stale map entry so a later manual
            # removal of the line gets a fresh summary
            if mapping.pop(rel_path, None) is not None:
                save_map(mapping)
            skipped += 1
            continue
        if frontmatter_is_draft(fm_lines):
            log.info("Skipping %s (draft: true)", rel_path)
            skipped += 1
            continue

        h = content_hash(body)
        entry = mapping.get(rel_path)
        if entry and entry.get("content_hash") == h:
            # body unchanged since last run and still no summary in the file —
            # nothing new to do
            skipped += 1
            continue

        title = frontmatter_title(fm_lines)
        try:
            log.info("Generating summary for %s", rel_path)
            summary = generate_summary(title, body)
            new_text = insert_summary(text, fm_lines, summary)
            path.write_text(new_text, encoding="utf-8")
            mapping[rel_path] = {"content_hash": h, "summary": summary}
            save_map(mapping)
            generated += 1
        except Exception:
            log.exception("Failed to generate summary for %s", rel_path)
            failed += 1

    # prune map entries for files that no longer exist
    for rel_path in list(mapping.keys()):
        if rel_path not in on_disk:
            del mapping[rel_path]
            pruned += 1
    if pruned:
        save_map(mapping)

    log.info(
        "Done. generated=%d skipped=%d pruned=%d failed=%d",
        generated, skipped, pruned, failed,
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
