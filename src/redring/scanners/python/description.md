# Python Scanner Reference Guide

> [!NOTE]
> This document details the available and planned Python environment scanners. It is designed to provide contributors with a clear overview of system health checks, their purposes, and their current implementation status.

## 🖥️ Interpreter & System Health

* **`python.version`** [🟢 Built]
  Detects the active Python version and validates it against modern runtime minimums.
* **`python.path`** [🟢 Built]
  Verifies that the Python binary exists on `$PATH` and resolves the exact executable location.
* **`python.ssl`** [🟡 Planned]
  Verifies that `import ssl` functions properly and that default certificates are valid.
  > This is highly necessary to catch silently broken source builds, as well as corporate firewall or proxy configurations that block SSL certificates.

## 📦 Package Management Health

* **`python.pip`** [🟢 Built]
  Ensures `pip` is installed and properly linked to the current interpreter.
* **`python.externally_managed`** [🟢 Built]
  Detects `EXTERNALLY-MANAGED` marker files that block global package installations after introduction of `PEP 668`.
  > [!IMPORTANT]  
  > With the introduction of PEP 668, modern Linux distributions (e.g., Ubuntu 23.04+, Debian 12) strictly enforce externally managed environments. This scanner is critical for preventing unexpected `pip install` failures.

## 📁 Workspace & Environment Context

* **`python.venv`** [🟢 Built]
  Validates if the current execution context is operating within an active virtual environment.
* **`python.project_venv`** [🟡 Planned]
  Scans the target project directory for dormant `.venv` or `venv` folders.
  > This acts as a safety net for a common developer oversight: creating a virtual environment yesterday, but forgetting to activate it in today's terminal session.

---

## 📊 Implementation Summary

| Status | Scanner Count |
| :--- | :---: |
| 🟢 **Ready / Built** | 5 |
| 🟡 **To Build / Planned** | 2 |
| **Total Scanners** | **7** |