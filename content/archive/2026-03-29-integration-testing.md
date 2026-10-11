---
title: "Integration, Error Handling & The Presentation Problem"
date: 2026-03-29
draft: false
tags: ["JavaJolt", "Testing", "Rest Assured", "Exam Prep"]
---

Two things dominated this week, finishing the integration test and starting to think about how to present this project to someone who hasn't lived inside it for two months. That was also difficult in my last exam, but there's major growth happening at the reviews. Being more specific and systematic when presenting is something I need to work on, but there's progress being made. Standing on your own at a review is nervewracking, but less evertime. 

The integration tests took longer than expected, not because the API was broken, but because writing good tests means defining what correct actually looks like in edge cases and that forces decisions I'd been putting off. What should happen when a user requests progress data for an exercise they haven't started yet? What's the right response when a request is technically valid but logically empty? These aren't hard problems, but they need answers and the tests are what made me answer them. There's a point somewhere in this process where the thinking starts to shift, some of the problems that would have stopped me cold a few weeks ago are not stressful, but fun debugging adventures where I get gratification and tiny dopamine hits everytime i see my tests going through. 

Error handling got a proper pass this week. The API was functional, but the error responses were inconsistent. I had some that returned useful messages, others didn't. Standardized across all endpoints now. 

The presentation is the new pressure. Explaining a backend to an examiner means translating technical decisions into clear reasoning not just what I built, but why the structure looks the way it does, what I'd change and what I learned. I kode intuitively, so I need to get out of my own head and rememember there are many moving parts to tend to. The gap between understanding something and being able to explain it cleanly is its own skill and I'm working on it. I understand my own thought process, so now I'm regarding the review meetings as a sort of exam prep.

**Next focus:** finalizing the API, locking the data model and building out the presentation structure.
