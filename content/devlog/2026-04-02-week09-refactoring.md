---
title: "Week 09 - Refactoring: Removing Redundant isAdmin Field"
date: 2026-04-02
draft: false
tags: ["JavaJolt", "refactoring", "JPA", "clean code"]
---

## Problem

The `User` entity had an `isAdmin` boolean column stored in the database. It was also derivable from the `roles` table — if a user has the ADMIN role, they are an admin. Two sources of truth for the same fact.

## Fix

Removed the `isAdmin` column from the `User` entity entirely. Replaced it with a method that checks the roles collection:

```java
public boolean isAdmin() {
    return roles.stream().anyMatch(r -> r.getName().equals("ADMIN"));
}
```

The database no longer stores `isAdmin`. It is always derived from roles at runtime.

## Result

All 40 tests passed after the change. The JWT token still includes `isAdmin` in the claims — it is now populated from the derived method rather than a stored field. Single source of truth, cleaner design.
