---
title: "The Legal and Ethical Side"
date: 2026-09-25T10:00:00+02:00
draft: true
tags: ["AIDA", "EU AI Act", "ethics", "copyright", "sustainability"]
categories: ["reflection"]
summary: "The EU AI Act puts educational assessment in the high-risk category, which lands directly on the rubric assessor I built. Plus copyright in RAG, and the energy cost nobody sees."
---

## The EU AI Act and my rubric assessor

The Act is risk-based, and AI used in education and assessment is explicitly **high-risk**. That lands directly on the rubric assessor I built.

It shaped a design decision rather than staying an abstract concern: the tool never returns a grade or a verdict. Every response is labelled as guiding, AI-generated feedback, and every response produces follow-up questions intended for a human conversation. That is human-in-the-loop and transparency made concrete, not a disclaimer bolted on afterwards.

## Copyright and RAG

RAG retrieves real documents and can reproduce them in its answers. For a bot built on my own portfolio that is fine, because the material is mine. The line worth stating: only index material you have the right to use, and ideally cite what was retrieved so a reader can check the source. Your own documents are the clean case. Someone else's corpus without permission is not.

## Sustainability

Generative AI has a real energy and water footprint. The lever a developer actually controls is inference: minimise what is sent per call, reuse prior results, and do not re-run unchanged jobs. The content-hash change detection in my RAG sync exists for cost reasons, but it has the same effect on energy. The cheapest call is also the greenest one.

## Where I land

*(This section is mine to finish — my own view on the trade-offs, not a summary of the reading.)*
