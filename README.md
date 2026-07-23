# RedRing

RedRing is an AI-assisted developer diagnostics tool focused on solving real environment and toolchain issues with evidence-first guidance.

Instead of guessing, RedRing inspects the local machine, verifies compatibility requirements, and helps developers understand what is blocking their setup.

---

## What RedRing Does

RedRing is designed to help developers troubleshoot problems related to their technology stack. It can inspect local setup conditions and guide the user through practical next steps.

A typical workflow might include:

- checking whether a tool's system requirements are met,
- validating available resources such as RAM or disk space,
- confirming internet access when downloads are required,
- checking hardware support such as virtualization,
- identifying BIOS or system-level blockers,
- producing a developer-friendly explanation of what is wrong and what to do next.

---

## Supported Developer Stacks

RedRing is being designed to support a wide range of developer stacks, including:

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

---

## Example Use Case

A developer trying to install Docker may not know whether their machine is capable of running it.

RedRing can check:

- whether the system meets Docker prerequisites,
- whether enough RAM is available,
- whether internet access is available,
- whether virtualization is present,
- whether virtualization is enabled in BIOS.

If the issue is a BIOS setting, RedRing can explain the exact next step clearly and practically.

---

## Core Principles

- Evidence first
- Explain before fixing
- Ask before making changes
- Prefer clear, actionable output
- Keep AI grounded in machine inspection

---

## Project Status

RedRing is currently in its early foundation phase, with the architecture, documentation, and scanner-oriented roadmap being shaped around the developer troubleshooting use case.

---

## Quick Start

```bash
redring analyze
```

---

## Documentation

See the project docs for the architecture, roadmap, vision, and contribution guidance:

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [docs/VISION.md](docs/VISION.md)
- [docs/ROADMAP.md](docs/ROADMAP.md)
- [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)
- [docs/SCANNER_SPEC.md](docs/SCANNER_SPEC.md)

---

## License

MIT