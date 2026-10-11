---
title: "The Legal and Ethical Side"
date: 2026-09-25T10:00:00+02:00
draft: false
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

"High-risk" sounded heavy when I first read it, and then I built the thing and it stopped being an abstract category. A language model assessing an internship report has no access to the internship. It cannot know whether the student actually did what the report claims, only whether the text reads as though they did. Once that is clear, returning advisory feedback and follow-up questions instead of a grade is not a compromise made to satisfy a regulation. It is the only output the tool can honestly produce.

That is the pattern I keep finding in this part of the course: the responsible choice and the good-engineering choice usually turn out to be the same choice, arrived at from different directions. Only index material you have the right to use is also how you avoid a knowledge base full of content you cannot vouch for. Do not re-run unchanged jobs is both a token-cost argument and an energy argument. Do not let the model be the final authority is ethics, and it is also just an accurate description of what the model can do.

Where I am less comfortable is the energy question, because it is the one where my own incentives do not help me. I can justify every individual call I make. "It is only one call" is exactly the reasoning that scales badly, and I do not have a good answer for it yet beyond not being wasteful on purpose.
