---
title: "Building an AI Rubric Assessor: What Today Actually Taught Me"
date: 2026-08-31T09:00:00+02:00
draft: false
tags: ["AIDA", "LLM", "reflection", "rubric", "prompt design"]
categories: ["journal"]
summary: "A personal walkthrough of building a small AI grading tool: the loose thoughts I started with, the wall I hit, and what it taught me about trusting a model to judge someone else's work."
---

The day started messy, the way most of my good days do. I had three unrelated thoughts sitting in my notes before I even opened the actual assignment: how do you build theory, not just text, when you are working with code agents all day, and who actually owns that theory once the agent has written it. A half formed idea about a screenscraper that only needs to run once a week, and whether that result should live in a JSON file or in a database. And a genuinely boring but necessary question: how do you schedule a Linux cron job to hit an API endpoint with curl once a week, without babysitting it.

None of those made it into today's build directly, but I want to keep them here because they are the kind of question that only shows up when you are actually building things regularly, not when you are studying for an exam.

The real task was this: build a small AI powered application that gives a first, guiding assessment of an internship report using a rubric, and a call to an external LLM API. Not "get an answer from a model." Design a small application where an LLM is one piece of a real data flow.

## The part that felt obvious and wasn't

I assumed the rubric would be the easy part. Read the requirements document, turn the bullet points into criteria, done in fifteen minutes. It was not fifteen minutes.

The requirements document for a praktikrapport is short. Company description, how you met the learning objectives, the tasks you did and how they connect to theory from school, reflection on your personal development, reflection on what both you and the company got out of it, and proof you filled in the evaluation form. That is five requirements, not six criteria, and definitely not six criteria with three distinguishable difficulty levels each.

Turning "reflect on your personal development" into something a model can actually score consistently forced me to be honest about what "good" looks like here. It is not enough to say a student reflected. A low score report barely mentions it. A middle score report gives an episode but only shows one dimension of growth. A high score report shows the DARE, SHARE, and CARE values we are actually graded on, through something the student lived through, not something they claim.

## Where I got stuck

I wanted to test the whole thing end to end against a real OpenAI call, and I could not. The sandbox this was built in has no route to the npm registry, so `npm install` failed on the very first dependency. No Express, no dotenv, nothing.

My first instinct was frustration, but the fix ended up teaching me something about designing for testability that I would not have learned if the install had just worked. I split the logic that has nothing to do with the network, rubric loading, prompt construction, and response validation, into plain Node functions with zero external dependencies. Then I wrote a tiny mock model that returns a schema shaped response using simple keyword matching instead of a real LLM call. That let me prove the entire data flow works without ever touching the network.

It is not a substitute for testing against a real model. The mock cannot tell me if the model actually gives useful, stable feedback. But it proved something that matters just as much before spending a single token: the plumbing does not lie to you.

## The thing I keep circling back to

Building this made me think about my own practicum reports differently. If a version of this tool had graded mine, would it have caught what actually mattered, or would it have rewarded whichever report happened to be the most fluently written.

That is the honest limitation I wrote into the disclaimer field of every response this app returns: this is a guiding, AI based assessment, not truth. A language model has no access to what actually happened during someone's internship. It can only judge the text in front of it, and text can be well written without being true, or true without being well written. The rubric narrows how much room the model has to freelance, it does not remove the gap between "sounds reflective" and "is reflective."

I do not think that makes the tool useless. I think it makes it exactly what the assignment asked for: a first pass, a set of follow up questions to bring into an actual conversation with a real person, not a verdict.

## What I am taking into tomorrow

Test the boring parts first, especially when the exciting part (the actual model call) is the one thing you cannot fully control today. A rubric is not a checklist, it is a definition of what "good" means, and writing one honestly is harder than reading one.

Next up: the technical writeup, with the architecture, the prompt design choices, and the actual JSON schema, for anyone who wants the how instead of the why.
