---
title: "Flaky Tests & External APIs"
date: 2026-03-15
draft: false
tags: ["JavaJolt", "Testing", "Stack Overflow API", "Debugging"]
---

Something confusing happened today. The tests failed, but then I ran them again without changing anything and they passed. That shouldn't be possible or at least, that's what I thought.

The failing test was the one that calls the Stack Overflow API. After some digging, the issue seems to be that the API doesn't always send back data in the same format. Sometimes it's compressed, sometimes it isn't and the code was only prepared for one of those cases. When it got the other one, it crashed. When it got the expected one, it worked fine. So the test wasn't actually broken, it was just telling me that the thing it depends on is inconsistent.

The fix involved making the code try one format first and quietly fall back to the other if that doesn't work. I understand what the code does at a surface level but I'm still not fully comfortable with what gzip compression actually is or why an API would sometimes use it and sometimes not. That's something to come back to.

What I do understand now: a test that randomly fails isn't always a broken test. Sometimes it's a warning that something outside your code is unreliable. That distinction matters and I wouldn't have thought to make it a week ago.
