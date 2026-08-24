---
title: "RAG I: Three Ways to Build a Chatbot, One Afternoon to Compare Them"
date: 2026-08-21
draft: false
tags: ["AIDA", "RAG", "Dify"]
---

Second session was the actual introduction to RAG, retrieval-augmented generation, or in plain terms: how to connect an LLM to documents it wasn't trained on, so it can answer questions grounded in *your* material instead of whatever it happened to learn during training. We talked through when RAG is worth the complexity (you have a real, changing body of domain content you want answered from) and when it isn't (a static FAQ doesn't need a vector database).

The useful part of the session was comparing three concrete ways to actually build one:

**ChatGPT's Custom GPT**, fastest to a working demo, zero infrastructure, but it lives inside ChatGPT. No real API for automating what's in its knowledge, and nothing you can embed as a widget on your own site.

**CustomGPT.ai**, a proper hosted RAG platform with a real API, closer to production-grade. The catch: no meaningful free tier, plans start around $99/month, which is a hard sell for a student project.

**Dify.ai**, open source, has a genuinely free Cloud tier, and exposes both a chat API and a separate Knowledge Base API for managing documents programmatically. That combination, free plus scriptable, is what made it the one worth actually building with.

We used Dify for the mini-project: uploaded the study curriculum (studieordning) PDF, converted to markdown first since markdown chunks and indexes far more predictably than raw PDF text, and had a working chatbot answering questions about the programme within the session. It's a small example, but it made the abstract "embeddings and retrieval" explanation from earlier concrete, you could watch it retrieve the actual paragraph an answer came from, which does a lot for trusting (or correctly *not* trusting) what it says.

The obvious next problem, which session three is apparently going to be entirely about: this only works if someone remembers to re-upload the document every time it changes. For a study curriculum that's rare. For a portfolio blog that updates weekly, that's not going to hold up.
