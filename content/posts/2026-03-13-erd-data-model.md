---
title: "The Data Model — ERD & Architecture Decisions"
date: 2026-03-13
draft: false
tags: ["JavaJolt", "Database", "ERD", "Architecture"]
---

Every decision in the backend eventually traces back to the database. Getting the data model right early means everything built on top of it has something solid to stand on.

<img src="/portfolio/images/ERD.png" alt="JavaJolt ERD" style="width:100%;" />

JavaJolt is structured around five core entities: **Users**, **Courses**, **Lessons**, **Exercises**, and **Progress**. The relationships are intentionally straightforward — a course contains lessons, a lesson contains exercises, and a user's progress is tracked per exercise.

A few decisions worth noting:

**Soft delete on users** — the `deleted` flag means user data is never permanently removed, which keeps referential integrity intact and gives room for account recovery later.

**TEXT over VARCHAR for content fields** — lesson content and code examples can be long. VARCHAR(255) would have caused silent truncation bugs down the line. TEXT from the start.

**Timestamps on creation** — every entity records `created_at` on insert and never updates it. Gives a clean audit trail without any extra logic.

The model has stayed stable since it was first designed. Changes at the schema level ripple through everything — the fact that it hasn't needed restructuring means the initial thinking held up.
