---
title: "Back in the Code"
date: 2026-03-22
draft: false
tags: ["JavaJolt", "Refactoring", "Testing"]
---

Returned to the JavaJolt codebase this week with fresh eyes, which turned out to be more useful than I expected. Distance from a project has a way of making the structural decisions you glossed over suddenly very visible.

The first day back was mostly reading. Going through what I'd built, running the tests again and making sure everything I thought worked was still compiling with the tooling updates from last week. It did, mostly. One endpoint was returning the wrong status code on a specific null case that the tests had missed, because the test data was too clean. That was fixed, noted and I added a messier test case to make sure it stays fixed.

The bigger focus this week was on the data layer. I've been thinking about how the API models the core JavaJolt concepts: exercises, progress tracking and user state. There were a few places where the structure made sense when I first wrote it but doesn't hold up as the feature set grows. I refactored two of those relationships, before they became issues.

It's the kind of work that doesn't produce anything visibly new, but makes everything that comes next easier. It was something that made me feel like a real developer. I've learned to stop resenting that phase and start recognizing it as part of the job.

**Still ahead:** fleshing out the remaining endpoints, writing the integration test  and  thinking seriously about the exam presentation.
