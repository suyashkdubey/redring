>[!NOTE]
> **RedRing Architecture & Direction**  
> This document is part of the **RedRing** project documentation. It should evolve alongside the codebase and be updated whenever the architecture or project direction changes.

---

# Project Decisions

This document records the major strategic and technical decisions behind RedRing.

---

## Decision 001: Build the project in Python

### Why

- Faster product iteration.
- Strong ecosystem for system inspection and automation.
- Easy onboarding for contributors.
- Good fit for CLI and diagnostic tooling.

### Trade-offs

- Lower raw performance than systems programming languages.
- Higher memory usage in some workflows.

### Status

Accepted.

---

## Decision 002: Use an evidence-first diagnostic model

### Why

RedRing should not tell users what is wrong based on guesswork. It should inspect the environment, confirm requirements, and only then provide a proposed diagnosis.

### Outcome

This keeps the system trustworthy and makes the AI layer more reliable.

### Status

Accepted.

---

## Decision 003: Keep the AI layer as an explanation engine, not the authority

### Why

The AI should help explain findings, suggest next steps, and summarize evidence. It should not replace the system’s own inspection logic.

### Outcome

The architecture remains grounded in real machine context rather than purely language-model assumptions.

### Status

Accepted.

---

## Decision 004: Support developer stacks by scanner domain

### Why

The product’s core use case is environment troubleshooting for developers. Each supported stack should have a focused scanner or a diagnostic-check profile.

### Initial support scope

- Python
- Docker
- Git
- Node.js
- Java
- Rust
- Go
- PostgreSQL
- MySQL
- Redis
- MongoDB
- CUDA
- Android
- Flutter
- Kubernetes

### Status

Planned / in design.

---

## Decision 005: Prioritize CLI-first delivery

### Why

A lightweight CLI-first approach allows the project to validate the core diagnostic workflow quickly and efficiently.

### Outcome

The product can mature from a terminal tool into richer interfaces later, without changing the underlying diagnosis pipeline.

### Status

Accepted.