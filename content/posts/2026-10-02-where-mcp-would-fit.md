---
title: "Where MCP Would Fit in a Project Like Standflow"
date: 2026-10-02T10:00:00+02:00
draft: false
tags: ["AIDA", "MCP", "architecture", "reflection"]
categories: ["reflection"]
summary: "Model Context Protocol is not a replacement for a REST API. A short reflection on what it is, and where it would actually belong in a system I have already built."
---

## What MCP is

A standard way for a model or agent to talk to external capabilities. A server exposes **tools** (actions it can take), **resources** (data it can read) and **prompts** (templates), over stdio for local use or streamable HTTP for remote.

The framing that made it click: it does not replace a REST API. REST is frontend-to-backend. MCP is model-to-tools. A real system can expose both, serving its own frontend over REST and its capabilities to an assistant over MCP.

## Where it would fit in Standflow

An MCP **tool** wrapping existing endpoints, "list pending applications", "draft a reply to this applicant", so an assistant could help the organiser triage without a bespoke integration written for each action.

An MCP **resource** exposing the template library and FAQ, the non-personal, consented material, so a model reads the real current source rather than a stale copy pasted into a prompt.

An MCP **prompt** template for newsletter tone, so the phrasing stays consistent whoever is drafting.

Each of those is a small capability behind a standard interface, which is the same boundary discipline that made working with a code agent safe: narrow, described, and explicitly scoped.

## Honest caveat

I have not built an MCP server for this project. This is a reflection on where it would go, not a report on something I shipped. What the lesson gave me is a clearer mental model, REST for app-to-backend and MCP for model-to-tools, and a concrete reason to keep AI features behind narrow, described tools rather than wiring a model straight into the database.
