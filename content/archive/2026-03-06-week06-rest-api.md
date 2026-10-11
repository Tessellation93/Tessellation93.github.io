---
title: "Week 06 - REST API Implementation"
date: 2026-03-06
draft: false
tags: ["JavaJolt", "REST", "Javalin", "API"]
---

This week the backend got its REST layer. Implemented the full API using Javalin 7.0.1, defining endpoints across the core resources: users, lessons, exercises, and progress tracking.

25 endpoints total, structured around standard REST conventions. Each resource has full CRUD coverage where appropriate, with consistent response formats and HTTP status codes throughout.

Documented the API in a structured spec file covering endpoint paths, request/response formats, status codes and error handling. This becomes the contract the frontend will eventually work against.

**Running on:** `localhost:7070`. Framework: Javalin 7.0.1.
