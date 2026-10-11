---
title: "Building a Whole Project with a Code Agent"
date: 2026-09-18T10:00:00+02:00
draft: false
tags: ["AIDA", "code agents", "collaborative agentic development", "git", "software architecture", "reflection"]
categories: ["technical", "reflection"]
summary: "I used an AI code agent to take over and finish an entire group project, Standflow. This is the honest version: what the agent did, what I kept for myself, the guardrails that made it safe, the near-disaster, and what actually makes agentic development work."
---

The assignment behind this post was about collaborative agentic development: working with AI agents, and with each other, to build real software. I did not just try it on a toy task. I used an AI code agent to take over and finish an entire group project, [Standflow](https://standflow.roneu.dk/), a stall-holder application system for a Christmas market, after a teammate ran out of credits mid-sprint and the remaining user stories had nobody on them.

This is the honest version of how that went.

## The situation

Standflow had seven user stories spread across the group. Partway through, work stalled: branches were half-merged, one teammate was out, and the stories for newsletters, the public vendor page and the admin control panel were unfinished. With the tech lead's go-ahead, I became the integration lead and used a code agent to close everything out: merge every open feature branch into our `Review` branch, resolve the conflicts, finish the newsletter frontend, wire the admin panel and the public vendor page to live data, fix a backend bug, and get the test suite green.

The thing I want to be precise about is the division of labour, because "I used AI" is not a reflection, it is a slogan.

## What the agent did, and what I kept

The agent read the code, wrote and edited files, made local commits, and explained what it was doing. I did the thinking that decides what "done" means, and I kept three things firmly in my own hands.

**I kept every irreversible git action.** The agent was never allowed to push or merge. It made commits locally; I reviewed them and ran `git push` myself, in my own terminal. That one rule meant the agent could move fast without ever being able to put something into shared history that I had not looked at.

**I kept the conventions.** Partway through I decided our commits should not carry AI co-author trailers, that there should be no comments left in the code, and that repo-facing text should be in English. The agent applied those going forward and amended the commits that had already broken the rules. The point is that the human owns the house style; the agent follows it.

**I kept verification honest.** The agent's sandbox could not reach the package registries, so it could not actually run our frontend build or the backend tests. It fell back to static checks: confirming every import resolved to a real file and that the syntax balanced. The real verification, `mvn test` and `npm run dev`, happened on my machine. I think this distinction matters more than anything else in the post: an agent saying "I checked it" can mean "I statically checked it," which is not the same as "the tests pass." Knowing where verification actually happens is part of the job now.

## The guardrails that made it work

Our repo already shipped an `AGENTS.md`: read the architecture and code-standard docs first, only touch the files the issue needs, no unrelated refactors, no architecture changes without approval, tests and lint must pass, and a list of protected files. On top of that, our user stories were written as guardrail tickets, each with explicit acceptance criteria.

That combination is what let an agent work inside a real repo instead of generating a plausible-looking mess. The ticket said what "done" looked like; `AGENTS.md` said what the agent was not allowed to touch on the way there. When the agent proposed a new feature that needed an architecture decision, where to store uploaded files, it stopped and asked instead of guessing, because the guardrails told it to. A code agent without guardrails is a very fast junior who has never read your codebase. With guardrails, it is a very fast junior who respects your boundaries.

## The near-disaster

It was not all smooth, and pretending it was would make this a worse reflection. At one point a pull request that should have gone into `Review` was merged into `main` instead. That is exactly the kind of mistake that is easy to make when you are moving quickly across a lot of branches.

The recovery was itself a lesson: reset `main` back to the last known-good commit with `git reset --hard`, push it back with `git push --force-with-lease` (the "with-lease" part is what stops you from clobbering someone else's work you have not seen), and then re-merge the branch into `Review` the correct way. After that we were strict about base branches. The takeaway is not "AI caused a bug," it did not, a human merge did, it is that speed without branch discipline is how you end up rewriting history at eleven at night.

There was also a very ordinary layer of friction underneath all of this: a new Windows laptop where Git, Node, Java and Maven all had to be installed from scratch, a Danish keyboard being read as a US layout, and, best of all, OneDrive quietly fighting Git because the repo lived inside a syncing folder, which caused lock conflicts and files that reappeared after I stashed them. The fix was to move the repo out of OneDrive entirely. None of that is glamorous, but it is the real texture of building software, and it is worth saying out loud that the agent could not fix my environment for me; it could only work once the environment worked.

## What I actually learned

A code agent changes where your effort goes, not how much of it you need. I spent almost no time typing boilerplate and almost all of it on three things: deciding what each ticket really required, reviewing what came back, and owning the git and verification steps the agent was not allowed to own. The quality of the output tracked the quality of the guardrails and the review, not the cleverness of any single prompt.

If I did it again I would write the guardrail tickets even more tightly, protect the base branches at the repository level so a wrong merge is impossible rather than just discouraged, and be even more explicit, from the first commit, about the difference between "statically checked" and "tested." The project shipped and is deployed. The part I am proudest of is not that an AI wrote a lot of it, it is that I can tell you exactly which parts I verified, how, and where the gaps still are.
