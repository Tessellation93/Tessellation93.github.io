---
title: "RAG II: Making the Chatbot Keep Up With Itself"
date: 2026-08-24
draft: false
tags: ["AIDA", "RAG", "Dify", "GitHub Actions", "CI/CD"]
---

Today's session picked up exactly where the last one left off: a RAG chatbot is only as good as its last upload, and manually re-uploading content every time a post changes isn't a real solution, it's just a chore waiting to be forgotten. The actual task was getting a chatbot onto this portfolio site that answers questions about the content on it, and automating it so it updates itself whenever a post is added or changed. No manual step, no logging into a dashboard.

Before touching code, the plan was to actually lay out the options and their tradeoffs rather than pick the first thing that sounded reasonable, a habit worth carrying over from last semester's more process-heavy systems development work, where picking and documenting a method mattered as much as the code itself. So: brainstorm first, Kanban board and pull requests to track it, decision written down before implementation.

Routes considered, roughly in order of how tempting they looked before the cost/benefit math caught up:

- **A ChatGPT Custom GPT or CustomGPT.ai**, ruled out for the same reasons as last session: no real automation path, or priced for a company, not a student.
- **Dify's built-in website/sitemap import**, crawling the live site via a third-party scraper (Jina Reader or Firecrawl), genuinely less code to write, since Dify does the crawling itself. But it looks like every resync re-crawls and re-embeds the *entire* site rather than just what changed, and it adds a dependency on yet another external service. I even found a working example of exactly this approach from a reference repo: sitemap in, Jina Reader converts each page to markdown, pushes it to Dify, and it confirmed the concern directly, no change detection at all, every URL gets re-uploaded on every run.
- **Self-hosting Dify** on the DigitalOcean droplet instead of using their Cloud tier, no document limits, but a real Docker Compose stack to maintain (Postgres, Redis, TLS) for a portfolio-scale chatbot. Filed as a phase-two idea, not a today problem.
- **A fully custom-built RAG pipeline**, no platform at all, the most impressive on paper, and the least realistic given the timeline. Worth naming as considered and rejected, since that's an honest engineering call, not a shortcut.

Landed on: **Dify Cloud, with a GitHub Action that pushes only what changed.** Dify's Knowledge Base API supports creating and updating documents by text directly, separately from its chat API, which means the sync doesn't need Dify to read the repo at all, no GitHub token, no scraper. The script hashes each markdown file's content and only calls the API when the hash has actually changed, which makes the whole thing idempotent, re-running it never creates duplicate documents, and keeps it well inside the free tier's rate limit instead of re-embedding the entire site on every push.

What's actually built as of today: the Python sync script and the GitHub Actions workflow are written, tested for logic, and sitting in an open pull request against this repo. Dify account and knowledge base setup is in progress. The chat widget isn't embedded yet, and end-to-end testing, edit a post, push, watch it show up in the bot's answers, hasn't happened yet either. That's genuinely where it stands: decided, mostly built, not yet proven. Next entry should either confirm it works or explain what broke.
