# Python Scanner Reference Guide

> [!NOTE]
> This document details the available and planned Python environment scanners. It is designed to provide contributors with a clear overview of system health checks, their purposes, and their current implementation status.

## 🖥️ Interpreter & System Health

* **`python.version`** [🟢 Built]
  Detects the active Python version and validates it against modern runtime minimums.
* **`python.path`** [🟢 Built]
  Verifies that the Python binary exists on `$PATH` and resolves the exact executable location.
* **`python.ssl`** [🟡 Planned]
  Verifies that `import ssl` functions properly and that default certificates are valid. Essential for catching silently broken source builds and firewall/proxy SSL interception.

## 📦 Package Management Health

* **`python.pip`** [🟢 Built]
  Ensures `pip` is installed and properly linked to the current interpreter.
* **`python.externally_managed`** [🟢 Built]
  Detects `EXTERNALLY-MANAGED` marker files that block global package installations under PEP 668.

> [!IMPORTANT]
> Modern Linux distributions (e.g., Ubuntu 23.04+, Debian 12) strictly enforce PEP 668 externally managed environments. This scanner is critical for preventing unexpected `pip install` failures.

## 📁 Workspace & Environment Context

* **`python.venv`** [🟢 Built]
  Validates if the current execution context is operating within an active virtual environment.
* **`python.project_venv`** [🟡 Planned]
  Scans the target project directory for dormant `.venv` or `venv` folders to catch unactivated environments.

---

## 📊 Implementation Summary

| Status | Scanner Count |
| :--- | :---: |
| 🟢 **Ready / Built** | 5 |
| 🟡 **To Build / Planned** | 2 |
| **Total Scanners** | **7** |