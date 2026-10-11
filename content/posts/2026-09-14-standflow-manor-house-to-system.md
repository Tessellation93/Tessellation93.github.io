---
title: "Standflow: From a Manor-House Visit to a Working System"
date: 2026-09-14T10:00:00+02:00
draft: false
tags: ["AIDA", "Standflow", "software architecture", "project", "requirements"]
categories: ["technical", "project"]
summary: "The project case: a real customer with a real problem, the idea we proposed, and the system we sketched and then built to solve it."
---

This post covers two lessons at once: the idea proposal that came out of visiting a company, and the project description and system sketch that followed. The company was Engestofte Gods, a manor running a Christmas market, and the project became [Standflow](https://standflow.roneu.dk/).

## The problem, in the customer's own terms

The organiser runs a Christmas market with more than 80 stalls. Every stall-holder applies by email. That sounds manageable until you picture the inbox: applications arrive in no particular order, half of them are missing a piece of information, and there is no single place that answers the three questions the organiser actually has, who is still waiting on a decision, who is approved, and how do I send one message to a whole group of them without doing it by hand eighty times.

So the problem was never "build a website." It was "replace an inbox that has stopped scaling."

## The idea we proposed

A customer register, not a form. One place where the organiser can read an application, approve it, reject it, or ask for the missing piece, and attach a private internal note to a troublesome one. On top of that, a way to message stall-holders, individually or in segments (same stall category, new this year, previous years), using reusable templates with merge-fields so a hundred personalised emails are written once. And a public side that shows only the approved stall-holders, so the market's visitors see a clean list and the applicants' private data never leaks.

## The system sketch

The architecture is a straightforward three-layer web application, and keeping it straightforward was a deliberate choice.

The frontend is React. It never talks to the database; it only makes HTTP/JSON calls to our own backend. The backend is Java with Javalin exposing a REST API, business logic in a service layer, and Hibernate mapping to PostgreSQL (with an in-memory H2 database standing in during tests). Authentication is JWT with BCrypt-hashed passwords, and every endpoint is gated by a role, ANYONE, USER, ADMIN or OWNER, checked centrally before the endpoint runs rather than scattered through each handler.

The data flows one way and is easy to narrate, which matters for an oral exam: a component in the browser calls the API, a controller validates the request, the service does the work, Hibernate persists it, and a DTO shapes what goes back out so internal fields never reach the client. That last detail is what lets the public vendor page exist safely next to the private admin panel: they read from the same data but through different DTOs.

## What it turned into

The sketch became seven user stories, each written as a ticket with acceptance criteria: login and consent, application handling, customer–admin chat, templates and variables, newsletters with recipient segmentation, GDPR (consent, secure-token unsubscribe, account deletion), and the paginated public vendor page. All seven are built, the backend test suite passes, and the app is deployed.

The lesson I took from the idea-to-system step is that the hardest part was not the architecture, it was being honest about what the customer's problem actually was. "Too many emails" is not a feature request. Turning it into "a register with status, notes, segmented messaging and a public view" was the real design work; everything after that was execution.
