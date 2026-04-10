---
title: "Week 08 - Git Strategy, README & Project Wrap-Up"
date: 2026-03-29
draft: false
tags: ["JavaJolt", "Git", "GitHub", "Documentation", "Deployment"]
---

## Task

Get the project into a state ready for exam submission. Clean repository, documentation, and a branching strategy that tells the story of how it was built.

## Git Branching
```
main     ← clean release branch, only fully working merged features
  |
dev      ← integration branch, all features merge here first
  |
  +-- feature/users
  +-- feature/courses
  +-- feature/jwt
  +-- feature/stackoverflow
  +-- feature/integration-tests
  +-- feature/docs
```

Every feature got its own branch off `dev`. When finished and tested, it merged into `dev`. When `dev` was stable, it merged into `main`. Main has 8 clean commits — each one represents a completed, working feature.

## Kanban

A GitHub Projects board was set up mid-project. In hindsight it should have been there from day one. Working solo doesn't mean you don't need structure. The board made it immediately clear what was done, what was in progress and what was being deprioritised. 

## Final test count

- 27 DAO unit tests
- 13 REST Assured integration tests  
- 40 total, BUILD SUCCESS

The Stack Overflow test is intentionally live, it hits the real API and is documented as such.
