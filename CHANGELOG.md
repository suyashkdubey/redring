>[!NOTE]
> **RedRing Architecture & Direction**  
> This document is part of the **RedRing** project documentation. It should evolve alongside the codebase and be updated whenever the architecture or project direction changes.

---

# Changelog

All notable changes to RedRing will be documented in this file.

## Unreleased

<!-- Placeholder for upcoming changes -->

## 0.2.0-alpha.2

### Added

- Python scanners: `python_path`, `python_pip`, `python_venv`, and `python_version`.
- OS scanner enhancements: `os_info` now reports Linux distribution details and Python version.
- CLI renderer: added a Rich-based CLI renderer for improved output formatting.
- Scanner registry improvements: `get_by_prefix` helper and registry robustness.
- Logging configuration and logging integrated across core, engine, registry and scanners.
- CI: GitHub Actions workflow for running tests.

### Changed

- Refactored logging across multiple modules (engine, registry, CLI, python scanners).
- `pyproject.toml` updated to support Python 3.12+ and bump development version to `0.2.0`.
- CLI now integrates the renderer with the diagnostic engine and improves evidence formatting.

### Fixed

- Fixes to renderer internals and evidence/result content helpers for stable output.
- Engine fixes: better fallback when no scanner found and improved exception handling.
- Registry and CLI fixes: import-location fixes and corrected logging messages.
- Multiple bugfixes in python utility functions (including `find_python()` and Windows command handling).

### Docs

- Moved and reorganized docs (README, CONTRIBUTING, ARCHITECTURE, CHANGELOG) and improved diagrams.

### Tests

- Added unit tests for python utilities and other test coverage improvements.


## 0.1.0

### Added

- Initial repository scaffolding.
- Base Python package structure.
- Documentation placeholders for architecture, roadmap, and contributing guidance.
- An initial CLI-first project direction.

### Notes

This version represents the starting foundation for RedRing and is intended to evolve into a broader AI-assisted developer diagnostics system.