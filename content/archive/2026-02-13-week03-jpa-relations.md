---
title: "Week 03 - JPA Relations & DAO Interfaces"
date: 2026-02-13
draft: false
tags: ["JavaJolt", "JPA", "Relations", "DAO"]
---

This week's focus was adding JPA relations to the project. Declared DAO methods using Java interfaces, covering both CRUD operations and JPQL queries, then implemented and tested them incrementally.

Key decisions made this week: keeping relationships unidirectional where possible, being conservative with cascade types, and only adding complexity where it was clearly needed. The instinct to overengineer early is real, resisting it is its own discipline.Something that I've had issues with earlier, but am now sussing out.

Added JPQL queries to fetch data across joined entities. Set up unit tests for the DAO interfaces alongside the implementation.

**Entities in play:** User, Lesson, Exercise. Relations mapped between them with appropriate cascade handling.
