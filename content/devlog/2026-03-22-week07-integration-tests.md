---
title: "Week 07 - Rest Assured Integration Tests"
date: 2026-03-22
draft: false
tags: ["JavaJolt", "Rest Assured", "Integration Testing", "HTTP"]
---

## Task

Write integration tests that verify the full HTTP stack, not only in the database layer, but on the requests going in and responses coming out.

## What was built

13 integration tests in `JavaJoltApiTest` using Rest Assured. The test server runs on port 7777, separate from the production port 7070.
```java
@BeforeAll
static void startServer() {
    app = ApplicationConfig.startServer(7777);
    RestAssured.baseURI = "http://localhost:7777";
}

@AfterAll
static void stopServer() {
    app.stop();
}

@Test
void testGetAllCourses() {
    given()
        .header("Authorization", "Bearer " + validToken)
    .when()
        .get("/api/courses")
    .then()
        .statusCode(200)
        .body("size()", greaterThan(0));
}

@Test
void testProtectedRouteWithoutToken() {
    when()
        .get("/api/users")
    .then()
        .statusCode(401);
}
```

## DAO test vs integration test

A DAO test calls the database directly via `EntityManager`. No server, no HTTP, no routing. It tests: does persisting and retrieving data work correctly?

An integration test sends a real HTTP request to a running Javalin server. It tests the entire stack: does the request reach the right controller, does it authenticate correctly, does the response have the right shape and status code?

Both are needed. A DAO test can pass while a controller is broken. An integration test would catch that.

## Given / When / Then

Rest Assured's syntax maps directly:

- `given()` — set up the request (headers, body, auth)
- `when()` — send it (GET, POST, PUT, DELETE)
- `then()` — assert the response (status code, body fields)

This structure also matches Gherkin/BDD notation, which is what the course uses for describing test scenarios.
