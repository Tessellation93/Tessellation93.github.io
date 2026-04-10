---
title: "Week 03–04 - REST API, Javalin & Route Design"
date: 2026-03-06
draft: false
tags: ["JavaJolt", "REST", "Javalin", "Controllers", "HTTP"]
---

## Task

Expose the database as a REST API. Map HTTP methods to CRUD operations and return proper JSON responses with correct status codes.

## What was built

`ApplicationConfig` sets up the Javalin server. `Routes.java` registers all 25 endpoints in one place. Five controllers handle the HTTP layer.
```java
public class ApplicationConfig {
    public static Javalin startServer(int port) {
        Javalin app = Javalin.create(config -> {
            config.bundledPlugins.enableCors(cors ->
                cors.addRule(it -> it.allowHost("http://localhost:3000")));
            config.http.defaultContentType = "application/json";
        });

        app.exception(NotFoundException.class, (e, ctx) ->
            ctx.status(404).json(Map.of("error", e.getMessage())));
        app.exception(NumberFormatException.class, (e, ctx) ->
            ctx.status(400).json(Map.of("error", "Invalid ID format")));
        app.exception(Exception.class, (e, ctx) ->
            ctx.status(500).json(Map.of("error", "Internal server error")));

        Routes.registerRoutes(app);
        return app.start(port);
    }
}
```

All endpoints are registered in `Routes.java`, nothing is scattered across controllers:
```java
app.get("/api/courses",       cc::getAll);
app.get("/api/courses/{id}",  cc::getById);
app.post("/api/courses",      cc::create);
app.put("/api/courses/{id}",  cc::update);
app.delete("/api/courses/{id}", cc::delete);
```

Controllers are thin, they receive request, call DAO, return response. No business logic:
```java
public void getById(Context ctx) {
    Long id = Long.parseLong(ctx.pathParam("id"));
    Course course = courseDAO.findById(id);
    if (course == null) throw new NotFoundException("Course not found: " + id);
    ctx.json(course);
}
```

## Status Codes

| Code | When |
|------|------|
| 200 | Successful GET, PUT |
| 201 | Successful POST — new resource created |
| 204 | Successful DELETE — nothing to return |
| 400 | Bad input (invalid ID format, bad enum value) |
| 401 | Missing or invalid JWT |
| 404 | Resource not found (NotFoundException) |
| 500 | Unexpected error — caught by global handler |

## Why throw instead of returning null?

Returning `null` when a resource isn't found forces the caller to do null-checks everywhere. Throwing `NotFoundException` means the global handler converts it to a proper 404 automatically. The controller stays clean.

## Why centralise routes?

Having all endpoint registrations in one file means you can see the entire API surface at a glance. No hunting through controllers to find which routes exist.
