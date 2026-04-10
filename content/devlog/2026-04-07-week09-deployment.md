---
title: "Week 09 - Deployment: Docker, CI/CD & DigitalOcean"
date: 2026-04-07
draft: false
tags: ["JavaJolt", "Docker", "CI/CD", "GitHub Actions", "DigitalOcean", "Watchtower"]
---

## Goal

Get JavaJolt running on a real server accessible from the internet.

## Stack

- Dockerfile using `amazoncorretto:17-alpine`, multi-stage build
- Docker Compose with three services: `db` (PostgreSQL 16), `app`, `watchtower`
- GitHub Actions workflow: builds fat JAR, builds Docker image, pushes to Docker Hub
- DigitalOcean Droplet (Ubuntu 24.04, Frankfurt, 1GB RAM)
- Watchtower polls Docker Hub every 30 seconds — any push to main redeploys automatically

## CI/CD Flow
## HibernateConfig

Added environment variable support so the same JAR works locally and in production. When `DEPLOYED=true`, it reads `JDBC_CONNECTION_STRING`, `JDBC_USER`, `JDBC_PASSWORD` from environment. Locally it falls back to `localhost:5432`.

## Live

`http://209.38.230.212:7070` — verified with curl against `/api/auth/register` and `/api/stackoverflow/questions`.
