---
title: "Architecture of an LLM-Backed Rubric Assessor"
date: 2026-09-04T09:30:00+02:00
draft: false
tags: ["AIDA", "LLM", "Node.js", "Express", "prompt engineering", "architecture"]
categories: ["technical"]
summary: "How a small Express service turns a rubric and a student report into structured, schema-validated AI feedback: the data flow, the prompt contract, the error handling, and how it was tested without a real API call."
---

This is the technical companion to the reflective post about the same project. This one is about the how: the data flow, the prompt contract, the failure modes, and the testing strategy.

## The problem in one sentence

Take an unstructured internship report, apply a fixed rubric to it through an LLM, and return structured, machine checkable feedback, without ever letting the model wander outside the rubric or return something the client cannot parse.

## System overview

The request path is: client posts `reportText` to the Express server; the server loads `rubric.json` and builds a system prompt and a user prompt from it; the LLM client sends those to the chat completions API; the response comes back as a JSON string; validation checks it against the expected schema; and the server returns either the validated assessment or a controlled error.

Four modules, each with one job:

| Module | Responsibility |
|---|---|
| `rubric.json` | The single source of truth for criteria, weights, and level descriptors |
| `prompts.js` | Turns the rubric and the report text into a system prompt and a user prompt |
| `llmClient.js` | Owns the network call: timeout, error mapping, JSON parsing |
| `validate.js` | Checks the model's JSON against the exact schema the client expects |

No module reaches past its neighbour. The server never talks to the model provider directly, and the LLM client never sees Express. That boundary is what made the whole thing testable without a real network call.

## The validation step

`response_format: { type: "json_object" }` guarantees the model returns parseable JSON. It does not guarantee the JSON has the fields you asked for, in the shape you asked for, with values from the set you allowed. Those are two different failure classes and only one of them is solved by the API parameter. `validate.js` catches the second one before it reaches a client that might otherwise crash trying to read `assessment.criteriaFeedback[3].level`.

## Prompt design

Two prompts, built fresh on every request from the same rubric object, so the rubric and the prompt can never drift out of sync.

**System prompt** sets the model's role (an experienced, constructive advisor, not a judge), and does three things worth calling out: it forbids the model from using any criterion not in the rubric and forbids inventing quotes; it requires the model to say so explicitly when the report does not give it enough to go on; and it specifies the exact JSON shape expected in return, field by field.

**User prompt** carries two things and nothing else: the rubric serialised as JSON, and the report text wrapped in triple quotes as a clear boundary. Keeping them in the same message keeps the request stateless.

Two small settings do a lot of the stability work: `temperature` defaults to `0.2`, low enough to keep repeated runs close to each other, and the request timeout defaults to 30 seconds with an `AbortController`, so a hung request fails loudly with a `504`.

## Error handling

| Situation | Status |
|---|---|
| `reportText` missing or under 50 characters | 400 |
| API key not set | 500 |
| Request to the provider exceeds timeout | 504 |
| Network failure reaching the provider | 502 |
| Provider responds with a non-2xx status | 502 |
| Model response is not valid JSON | 502 |
| Model response is valid JSON but does not match the expected schema | 502 |

That last row is the one most tutorials skip. A model that returns syntactically valid JSON with a missing `disclaimer` field, or a `level` value outside the rubric's three allowed levels, is a real failure mode with real language models, and it deserves the same explicit handling as a network timeout.

## Testing without a real API call

The environment this was built in has no route to the npm registry, so `express` and `dotenv` could not be installed. Rather than treat that as a dead end, it turned into a forcing function for a cleaner separation of concerns.

`rubric.json`, `prompts.js`, and `validate.js` have zero external dependencies. That made it possible to write a dry run that loads the rubric and example reports, builds the real prompts, runs a small mock model standing in for the provider, runs the mock response through the same validation the real server uses, and writes the result for inspection.

All three example reports produced schema valid output in this dry run. That proves the plumbing: rubric loading, prompt construction, and schema validation all work correctly end to end. It does not prove the model gives good feedback. The honest way to say this: the dry run tests the pipe, not the water flowing through it.

## What I would build next

A numeric score derived from the existing per criterion weights; a small script that runs the same report through the real API multiple times to measure how stable `temperature 0.2` is in practice; and basic request authentication before this ever runs anywhere reachable by more than one person.
