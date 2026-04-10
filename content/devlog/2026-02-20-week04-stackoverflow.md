---
title: "Week 04 - Replacing Dead Code with a Real External API"
date: 2026-02-20
draft: false
tags: ["JavaJolt", "Stack Overflow API", "HTTP", "External API"]
---

## Task

Integrate a real external API into the project. The week's deliverable was a working HTTP call to an external service returning real data.

## Issue

The project had existing code that looked like a Duolingo API integration. It wasn't. It returned hardcoded mock data and never made a single HTTP call. It was dead code with an external sounding name.

Keeping it would mean presenting fake data as a real integration at the exam. It had to go.

## Replacement

Stack Exchange API. No API key required for basic usage, returns real programming Q&A from Stack Overflow, and maps perfectly to JavaJolt's theme of a coding learning platform.
```
GET https://api.stackexchange.com/2.3/questions
    ?order=desc&sort=activity&tagged=java&site=stackoverflow
```
```java
public List<StackOverflowQuestion> fetchJavaQuestions() throws Exception {
    HttpClient client = HttpClient.newHttpClient();
    HttpRequest request = HttpRequest.newBuilder()
        .uri(URI.create(BASE_URL + "?order=desc&sort=activity&tagged=java&site=stackoverflow"))
        .GET()
        .build();

    HttpResponse<String> response = client.send(
        request, HttpResponse.BodyHandlers.ofString());

    ObjectMapper mapper = new ObjectMapper();
    StackOverflowResponse parsed = mapper.readValue(response.body(), StackOverflowResponse.class);
    return parsed.getItems();
}
```

## The GZIP problem

Stack Exchange compresses responses with GZIP by default. Without handling this, JSON parsing failed with `Not in GZIP format`. Fixed by letting `HttpClient` handle decompression automatically.

## Why this API

- Free, no authentication needed
- Returns structured JSON with real programming questions
- Filterable by language tag (`java`, `python`, etc.)
- Actually demonstrates real API consumption, not mock data

## The flaky test trade-off

The integration test for this hits the live API. When Stack Overflow is slow or unreachable, the test fails. In a production system you'd mock the HTTP call in tests and only hit the real API in a staging environment. For this project, the live test is intentional, proving the integration is real.
