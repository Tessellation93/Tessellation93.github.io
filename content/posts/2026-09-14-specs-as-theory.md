---
title: "Specs as the Theory Behind the Code"
date: 2026-09-14T14:00:00+02:00
draft: true
tags: ["AIDA", "spec-driven development", "Naur", "reflection"]
categories: ["reflection"]
summary: "Peter Naur argued the real product of programming is the theory the programmers hold, not the code. Working with a code agent makes that argument louder."
---

This lesson was about working with specifications in AI-driven development, anchored in Peter Naur's essay *Programming as Theory Building*.

## Naur's point, louder now

Naur argued the real product of programming is not the code but the *theory* the programmers hold: why the system is shaped the way it is, which changes are safe. Code is the residue. A code agent sharpens this: it can produce correct-looking code without anyone holding the theory, so the gap Naur warned about can open on day one. The defence is the specification. If the "why" is written down before the agent writes the "how," the theory lives somewhere durable.

## In practice

On Standflow every user story was written as a spec before any code — goal, acceptance criteria, boundaries — and `AGENTS.md` encoded the architectural theory. When a feature needed a decision the spec did not cover, such as how to store uploaded files, the work stopped and asked instead of inventing an architecture nobody had agreed to.

## What I will carry forward

The more of the typing an AI does, the more the specification is the part that is actually mine, and the part that still makes sense when I come back a month later.
