import sys
import pytest
from redring.core.models.status import ScanStatus
from redring.scanners.python.python_venv import PythonVenvScanner

@pytest.fixture
def venv_scanner():
    return PythonVenvScanner()

def test_active_venv(venv_scanner, monkeypatch):
    monkeypatch.setattr(
        sys,
        "prefix",
        "/project/.venv"
    )
    monkeypatch.setattr(
        sys,
        "base_prefix",
        "/usr"
    )
    monkeypatch.setattr(
        sys,
        "executable",
        "/project/.venv/bin/python"
    )
    result = venv_scanner.scan()

    assert result.status == ScanStatus.PASS
    assert result.evidence["active"] == "yes"
    assert result.evidence["location"] == "/project/.venv"
    assert result.evidence["python"] == "/project/.venv/bin/python"
    assert result.evidence["base_prefix"] == "/usr"
    assert result.warnings == []
    assert result.errors == []

def test_no_active_venv(venv_scanner, monkeypatch):
    monkeypatch.setattr(
        sys,
        "prefix",
        "/usr"
    )
    monkeypatch.setattr(
        sys,
        "base_prefix",
        "/usr"
    )
    monkeypatch.setattr(
        sys,
        "executable",
        "/usr/bin/python3"
    )
    result = venv_scanner.scan()

    assert result.status == ScanStatus.WARNING
    assert result.evidence["active"] == "no"
    assert result.evidence["location"] is None
    assert result.evidence["python"] == "/usr/bin/python3"
    assert result.evidence["base_prefix"] == "/usr"
    assert result.warnings == ["No virtual environment is currently active"]
    assert result.errors == []