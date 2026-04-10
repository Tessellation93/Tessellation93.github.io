---
title: "Week 06 - JUnit 5 DAO Tests"
date: 2026-03-13
draft: false
tags: ["JavaJolt", "JUnit", "Testing", "TDD", "PostgreSQL"]
---

## Task

Write unit tests for the data access layer. Every CRUD operation on every entity should be tested against a real database.

## What was built

27 DAO tests across `UserDAOTest`, `CourseDAOTest`, `LessonDAOTest`, `ExerciseDAOTest`, `ProgressDAOTest`. Each test class follows the same structure:
```java
@BeforeAll
static void setUpClass() {
    HibernateConfig.getEntityManagerFactory();
    userDAO = UserDAO.getInstance();
}

@BeforeEach
void setUp() {
    // Clear test data before each test so tests don't affect each other
    userDAO.findAll().forEach(u -> userDAO.delete(u.getId()));
}

@Test
void testPasswordHashing() {
    User user = new User("hashtest", "hash@example.com", "mypassword", false);
    User created = userDAO.save(user);
    assertNotEquals("mypassword", created.getPassword()); // never stored as plain text
    assertTrue(created.verifyPassword("mypassword"));     // but still verifiable
}

@Test
void testSoftDelete() {
    User user = new User("deletetest", "del@example.com", "pass", false);
    User created = userDAO.save(user);
    userDAO.delete(created.getId());
    User found = userDAO.findById(created.getId());
    assertNull(found); // soft deleted users are invisible to findById
}
```

## Separate Test Database

Tests run against `javajolt_test`, not `javajolt`. The test Hibernate config uses `create-drop` — tables are created when tests start and dropped when they finish. Production data is never touched.

## Why @BeforeEach cleanup instead of @AfterEach?

Cleanup before each test means you start with a known-empty state regardless of what happened in the previous test. If a test fails mid-way and @AfterEach doesn't run, the next test still starts clean.

## Test Coverage

Every DAO gets: `findById`, `findAll`, `save`, `update`, `delete`. `UserDAO` additionally tests BCrypt hashing, `verifyPassword`, and `findByEmail`. Soft delete behaviour is verified — deleted records must not appear in `findAll` or `findById` results.
