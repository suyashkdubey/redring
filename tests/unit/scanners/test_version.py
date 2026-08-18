import pytest
import subprocess
from dataclasses import dataclass
from redring.core.models.status import ScanStatus
from redring.scanners.python.python_version import PythonVersionScanner
from redring.utils.python import PythonUtilities

@dataclass(frozen=True)
class FakeResult:
    returncode: int
    stdout: str
    stderr: str

@pytest.fixture
def version_scanner():
    return PythonVersionScanner()

def test_version_detection_success(version_scanner, monkeypatch):
    monkeypatch.setattr(
        PythonUtilities,
        "find_python",
        lambda self: "/fake/python"
    )
    def fake_run(*args, **kwargs):
        return FakeResult(
            returncode=0,
            stdout="Python 3.12.7\n",
            stderr=""
        )
    monkeypatch.setattr(subprocess, "run", fake_run)
    result = version_scanner.scan()

    assert result.status == ScanStatus.PASS
    assert result.evidence["version"] == "3.12.7"
    assert result.evidence["command"] == "/fake/python"
    assert result.warnings == []
    assert result.errors == []

def test_python_not_found(version_scanner, monkeypatch):
    monkeypatch.setattr(
        PythonUtilities,
        "find_python",
        lambda self: None
    )
    result = version_scanner.scan()

    assert result.status == ScanStatus.FAIL
    assert result.evidence == {}
    assert result.warnings == []
    assert result.errors == ["Unable to find a usable Python interpreter"]

def test_version_command_failure(version_scanner, monkeypatch):
    monkeypatch.setattr(
        PythonUtilities,
        "find_python",
        lambda self: "/fake/python"
    )
    def fake_run(*args, **kwargs):
        return FakeResult(
            returncode=1,
            stdout="",
            stderr=""
        )
    monkeypatch.setattr(subprocess, "run", fake_run)
    result = version_scanner.scan()

    assert result.status == ScanStatus.FAIL
    assert result.evidence["command"] == "/fake/python"
    assert result.errors == ["Python is not installed"]

def test_version_from_stderr(version_scanner, monkeypatch):
    monkeypatch.setattr(
        PythonUtilities,
        "find_python",
        lambda self: "/fake/python"
    )
    def fake_run(*args, **kwargs):
        return FakeResult(
            returncode=0,
            stdout="",
            stderr="Python 3.12.7\n"
        )
    monkeypatch.setattr(subprocess, "run", fake_run)
    result = version_scanner.scan()

    assert result.status == ScanStatus.PASS
    assert result.evidence["version"] == "3.12.7"
    assert result.evidence["command"] == "/fake/python"