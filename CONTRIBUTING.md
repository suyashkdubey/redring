>[!NOTE]
> **RedRing Architecture & Direction**  
> This document is part of the **RedRing** project documentation. It should evolve alongside the codebase and be updated whenever the architecture or project direction changes.

---

# Contributing to RedRing

Thank you for helping improve RedRing.

RedRing is a developer-focused diagnostics platform that aims to make local environment troubleshooting more understandable, evidence-based, and practical. Contributions should support that mission.

---

## How to Contribute

You can contribute by:

- improving the CLI experience,
- adding new scanners for supported developer stacks,
- refining diagnosis logic,
- improving output clarity,
- expanding documentation,
- adding tests and validation.

---

## Development Setup

1. Clone the repository.
2. Create a Python environment.
3. Install the project in editable mode.
4. Run tests and validation commands before submitting changes.

---

## Contribution Guidelines

### Code Style

- Prefer clear, readable Python code.
- Keep modular boundaries intact.
- Avoid mixing scanner logic with output or AI explanation logic.

### Scanner Contributions

When adding a new scanner:

- keep it focused on one technology domain,
- return structured evidence,
- avoid hard-coded assumptions,
- make failures observable and diagnosable.

> *To know more about scanners and its templates, check out the detailed [scanner-docs](https://redring.pages.dev/docs-scanner-spec)*

### Diagnosis Contributions

When improving diagnosis behavior:

- prefer evidence-based reasoning,
- explain confidence or severity when relevant,
- ensure results remain understandable for developers.

---

## Branch Naming

Use a consistent branch format such as:

- `feature/docker-scanner`
- `bugfix/gpu-detection`
- `docs/roadmap-update`

---

## Commit Message Style

Use conventional prefixes such as:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `refactor:` for structural improvements
- `test:` for tests and validation

---

## Pull Requests

Before opening a pull request:

- describe the problem clearly,
- explain the change and its rationale,
- add or update tests where appropriate,
- update documentation if user-facing behavior changes,
- keep the discussion respectful and constructive.

---

## Community Expectations

RedRing should remain:

- practical,
- trustworthy,
- evidence-first,
- developer-friendly.

Contributors should aim to improve the reliability and usefulness of the system rather than adding unnecessary complexity.