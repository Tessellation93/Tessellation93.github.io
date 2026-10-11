---
title: "Secrets, Escaping and Safe Choices"
date: 2026-09-21T10:00:00+02:00
draft: false
tags: ["AIDA", "security", "GDPR", "XSS", "API keys"]
categories: ["technical"]
summary: "How keys, escaping and consent are handled across my two projects, and why the safest choices were the ones that removed the unsafe option rather than guarding it."
---

## Keys never touch the client

The frontend never calls the LLM provider directly, because anything in the browser is readable. The flow is frontend → my own backend → external API. The key sits in a backend `.env`, never committed, never sent to the client. Because every call goes through my backend, that is also where validation, rate limiting and logging live.

## XSS: handled by construction, and provable

Standflow's chat cannot be injected, and I can say why rather than hoping. React escapes interpolated text automatically and there is no `dangerouslySetInnerHTML` anywhere in the codebase. Notification emails are sent as plain text, not HTML. Message fields are validated server-side: length limits, unknown fields rejected, strict JSON parsing.

The protection is not a filter we hope catches everything. The dangerous sinks, raw-HTML rendering and HTML email, simply do not exist in the data path.

## Access control

Role-based, with four roles (ANYONE, USER, ADMIN, OWNER), enforced centrally before each endpoint runs rather than checked ad hoc inside handlers. Internal notes are never exposed publicly, and the public vendor page serves only non-identifying fields through its own DTO: no email, no phone, no CVR number.

Passwords are hashed with BCrypt, sessions use JWT with a token version so tokens can be invalidated, and tokens are stored hashed with SHA-256.

## GDPR, built in

Three separate consents: terms and privacy are mandatory, marketing is optional, and the distinction is enforced in code. Only users who gave marketing consent receive newsletters; transactional mail is exempt because it is necessary to the service. Unsubscribe works through a secure token link without requiring login, and account deletion implements the right to be forgotten.

## Still on the list

File-upload hardening is designed but not built: magic-byte type validation so only PDFs and images are accepted regardless of file extension, a size limit, image compression, and SHA-256 deduplication. It becomes necessary as soon as stall-holders upload photos and the organiser distributes site-plan PDFs, so it is the next security work rather than a finished claim.

## What I learned

Good security here was mostly about *removing* the unsafe option rather than guarding it. The key is safe because the client cannot read it. The chat is safe because there is no raw-HTML sink. Marketing consent is safe because the code checks it before sending. Structural choices are the ones you can still explain, and prove, weeks later, which is a lower bar to clear than remembering every filter you wrote.
