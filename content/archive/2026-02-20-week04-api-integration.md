---
title: "Week 04 - External API Integration"
date: 2026-02-20
draft: false
tags: ["JavaJolt", "API", "ExecutorService", "Stack Overflow"]
---

This week introduced external API integration. The task was to fetch data from a real API and integrate it into the project using Java's ExecutorService to keep the application responsive during the fetch.

After evaluating options, I chose the Stack Exchange API, specifically Stack Overflow's programming Q&A. It's free, requires no API key for basic use, and maps naturally to JavaJolt's concept of surfacing relevant coding challenges to users. The endpoint filters by tag, so Java specific questions can be fetched and stored.

Implemented the fetch in a separate thread using ExecutorService, parsed the JSON response, and mapped it to the existing entity structure.

**Endpoint used:** `https://api.stackexchange.com/2.3/questions?tagged=java&site=stackoverflow`
