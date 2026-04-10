---
title: "Week 02 - First JPA Entity"
date: 2026-02-06
draft: false
tags: ["JavaJolt", "JPA", "PostgreSQL", "CRUD"]
---

Goal for today: get the project started with a first entity and basic JPA CRUD operations.

Set up the project structure using the established `app/` package convention, configured HibernateConfig with PostgreSQL, and created the first entity — `Lesson`. This covers the core fields: title, programming language, difficulty level, content, and estimated duration.

Implemented the DAO interface and first CRUD operations: create, read, update, delete. Ran initial unit tests against the local database to verify the setup was working correctly.

Starting small was the right call. One entity, a working database connection, and passing tests is a solid foundation to build on.

**Stack so far:** Java, JPA/Hibernate, PostgreSQL, Maven, `app/` package structure.
