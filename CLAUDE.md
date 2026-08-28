# Portfolio site — CLAUDE.md

Context for Claude Code (or any code agent) working in this repo. Read this before making changes.

## What this is

Stephanie "Tess" van Slyck's coursework portfolio: a Hugo static site using the **Blowfish** theme, deployed via GitHub Actions to GitHub Pages. Built for the AIDA (AI Drevne Applikationer) course, but also a general dev portfolio.

It has two content sections:

- `content/posts/` — course-facing blog posts (AIDA session write-ups, decision docs, reflections). Narrative, first person, can be longer.
- `content/devlog/` — technical devlog entries about her separate **JavaJolt** project (a Java/Spring Boot backend — DAO patterns, JPA, JWT auth, REST API, tests). JavaJolt's code lives in its own project, not this repo; these are write-ups *about* that work. Devlog entries follow a tighter **Problem / Fix / Result** structure, usually with one small code snippet.

## Frontmatter convention

Every post/devlog file starts with:

```yaml
---
title: "Human-readable title"
date: YYYY-MM-DD
draft: false   # true = not yet published, still safe to edit/scrap
tags: ["tag1", "tag2"]
---
```

Filenames follow `content/{posts,devlog}/YYYY-MM-DD-short-slug.md`.

## Voice

First person, casual but precise, technically specific. Documents real friction honestly — wrong assumptions, dead ends, what actually broke — not just clean success stories. See existing posts for tone before drafting new ones.

## Automation already wired up (don't duplicate, understand before touching)

**`scripts/dify_sync.py`** + **`.github/workflows/sync-dify.yml`** — on push to `main` touching `content/posts/**.md` or `content/devlog/**.md`, upserts changed files into a Dify Knowledge Base (the RAG chatbot's data source) via content-hash change detection (`dify-sync-map.json` tracks file → Dify document_id + hash, so unchanged files are skipped and reruns are idempotent). The Dify dataset uses **Economy** (keyword) indexing — no embedding model, so no credit/dimension issues. Needs `DIFY_API_KEY` and `DIFY_DATASET_ID` repo secrets.

**`scripts/devlog_draft.py`** + **`.github/workflows/devlog-draft.yml`** — on push to `main` touching non-content files (actual site/code changes), asks an LLM (Groq, `GROQ_API_KEY` secret) to draft a devlog entry from the commit messages + diff, writes it with `draft: true`, and opens a PR for review. Never auto-publishes. Skips itself on commits containing `[skip devlog]` or `[skip ci]` — use one of those markers in commit messages for any automated/bot commit that shouldn't re-trigger this.

Both scripts are self-contained single-file Python scripts by design (class convention) — keep that pattern if extending them rather than splitting logic across workflow steps.

## Working conventions (Tess's stated preferences)

- **One feature per commit/PR.** Keep changes scoped; don't bundle unrelated work.
- **Plan before big changes.** For anything non-trivial, propose the approach first and wait for approval rather than editing straight away.
- **Generate commit messages from the actual diff**, don't hand-write generic ones.
- **Never flip `draft: true` to `false`** on a post without Tess explicitly reviewing it first — draft posts and auto-drafted PRs are intentionally held for human review, that's the whole point of the devlog-draft agent.
- Hugo version/build: run `hugo server -D` locally to preview drafts before publishing if you need to sanity-check rendering.

## Things to watch for

- `content/**` changes should NOT trigger the devlog-draft workflow (it's filtered out on purpose — otherwise it'd try to draft-about-drafts).
- The `themes/blowfish` submodule and a few nested project folders (`javajolt-*`, `node_modules/`) may show as modified/untracked locally — those are usually not meant to be committed here; check before `git add -A`.
- Any link a chatbot answer surfaces should resolve to the live rendered page URL, not the raw `.md` source — noted requirement from class, not yet implemented as a hard rule anywhere in code.
