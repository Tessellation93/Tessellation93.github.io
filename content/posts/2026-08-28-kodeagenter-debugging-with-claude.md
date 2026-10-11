---
title: "Kodeagenter: What It Actually Looks Like to Debug With a Code Agent"
date: 2026-08-28
draft: false
tags: ["AIDA", "kodeagenter", "Dify", "GitHub Actions", "Claude"]
---

Session 4's exercise is simple to state: solve a programming task with a code agent, and document the workflow. I missed presenting this one live in class, but the honest version is that I spent the day actually *doing* the exercise instead, on a real task rather than a toy one: getting the RAG chatbot from session 3 from "architecture decided" to "actually working end to end." Claude was the code agent throughout. This is that log.

The point of this exercise isn't "the agent got it right first try." It's the opposite, every one of the friction points below is a place where the agent's first assumption was wrong in a specific, diagnosable way, and fixing it was a real back-and-forth, not a black box. That's a more honest and more useful thing to document than a clean success story would be.

## Friction 1: the agent can't reach the internet the way you'd assume

First surprise: Claude's own execution environment, and its bridge to my laptop, turned out to be sandboxed behind a network allowlist. Calls to Dify's API came back `403 Forbidden` from an internal proxy, not from Dify itself. The same restriction had already quietly affected an earlier `git push`.

The fix wasn't clever, it was just correct: run the actual API-calling script from my own real Terminal, where the network access is normal, and have the agent write and hand me the code rather than trying to execute it live. Worth naming as a real lesson, a code agent's own sandbox is part of the system you're debugging, not a neutral wrapper around your machine.

## Friction 2: the rate limit wasn't the rate limit we expected

Dify's free Sandbox tier caps knowledge-base calls at 10/minute. Standard practice is to detect that via an HTTP `429`. Dify doesn't do that, it returns a `403` with the real reason buried in a JSON message (`{"code":"forbidden","message":"...rate limit..."}`). The first version of the sync script's retry/backoff logic only watched for `429`, so the first ten documents synced fine and then the rest failed immediately with no retry at all.

Diagnosed straight from the actual error text in the logs, then patched: detect this specific 403-plus-message pattern as a rate limit too, and self-throttle to roughly one call every 6.5 seconds so we mostly avoid tripping the limit in the first place, rather than only reacting after the fact.

## Friction 3: the docs didn't match the UI

Dify's own documentation page for finding your API key didn't match the actual Cloud dashboard layout. It took a few rounds of screenshots back and forth before finding the real control (a "Service API" link, top-right of the Knowledge list page, not where the docs implied it'd be). Small, but a good reminder that an agent's training data can be stale against a product's current UI in ways that are only findable by actually looking at a screenshot together.

## Friction 4: the embedding model ran out of runway, twice

Once documents were syncing, the knowledge base itself wouldn't come online, the chat app kept showing it as "Unavailable." Cause: Dify's Sandbox plan shares one pool of 200 free AI credits across *every* default model provider, for both chat and embeddings. That pool was already spent.

Chasing a free embedding provider turned into its own small saga. Google AI Studio was blocked by a regional account restriction. Jina AI's dashboard kept dropping me onto an interactive request-builder page instead of anywhere to actually get a key. Hugging Face worked, but not on the first try, the first model I picked was tagged `sentence-similarity` when Dify's integration specifically requires `feature-extraction`, and after switching models, the first API token I generated didn't have the right permission scope (it needed a **fine-grained** token with "Make calls to Inference Providers" explicitly checked, not the default read-only kind).

Then, once the new embedding model was finally live: switching an *existing, already-populated* dataset to a differently-sized embedding model doesn't work. OpenAI's model produces 1536-dimension vectors; the Hugging Face one produces 384. Dify's vector index is fixed to whatever dimension it was created with, and every document errored out with a flat "vectors dimensions does not fit." The real fix wasn't a config change, it was structural: build a brand-new knowledge base from the start with the new embedding model selected, so its vector index is the right shape from day one. Or better, sidestep embeddings entirely by choosing Dify's "Economy" indexing mode, which matches by keyword instead of by vector and needs no embedding model at all. Given how much of the day had already gone to chasing free embedding credits, that felt like the right call rather than a compromise.

## Friction 5: even the "no embeddings needed" path had its own graph to untangle

Dify's newer knowledge bases are built as visual pipelines, a small node graph (data source, extractor, chunker, knowledge base) rather than a single form. The template came pre-wired with data-source nodes for Notion, Google Drive, Jina Reader, and Firecrawl, none of which I use, and Dify refused to publish the pipeline until every node in it, used or not, was either configured or removed. Deleting the unused ones then left two "Variable Aggregator" nodes with dangling references to the data sources that no longer existed, which had to be found and cleared by hand, one validation error at a time, before publish would succeed.

## Friction 6: the last mile was mundane, and mundane things still break

Getting from "it works when I run it manually" to "it runs itself" surfaced two very ordinary problems that had nothing to do with AI at all: a stale `.git/index.lock` file from an earlier interrupted commit blocking every subsequent `git commit`, and, after wiring the sync into GitHub Actions with repository secrets, a "document limit reached" error, because an old, permanently broken dataset from the failed embedding-model attempts was still sitting in the workspace, counting against the same free-tier document quota as the new, working one. Deleting it fixed the sync in one shot. Neither problem was interesting, and both were exactly the kind of thing that eats an afternoon if you don't know to look for them.

## Where it ended up

By the end of the day the chatbot's knowledge base syncs itself automatically: pushing a content change to `main` triggers a GitHub Actions workflow that diffs what changed, calls Dify's API directly (from GitHub's own runners, which don't have the sandboxing problem from friction 1), and keeps the mapping file that makes reruns idempotent. No manual re-upload, ever again, for as long as that workflow keeps running.

As a small bonus once the core pipeline was solid, we used the same collaborative pattern, agent proposes, human reviews, to build a second, smaller agent: a GitHub Actions step that reads each push's commit messages and diff, asks an LLM to draft a devlog entry about it in my own established style, and opens a pull request with the draft rather than publishing anything automatically. It's a fitting note to end a "kodeagenter" session on: an agent that helps document the work of other agents, with a human still firmly in the loop before anything goes live.

## The honest takeaway

Every one of these six friction points had a plausible, wrong first answer. Sandboxing looked like a permissions bug, the rate limit looked like it wasn't happening at all, the dimension mismatch looked like a settings problem, the pipeline errors looked unrelated to what I'd actually changed. None of them were solved by the agent guessing harder; they were solved by reading the actual error text, checking the actual UI, and treating each wrong assumption as data rather than trying the same fix twice. That back-and-forth, propose, verify, correct, retry, is the actual skill this exercise is about, more than any individual line of code that came out of it.
