import json
import pytest
import subprocess
from redring.core.models.status import ScanStatus
from redring.scanners.python.python_externally_managed import PythonExternallyManagedScanner
from redring.utils.python import PythonUtilities

@pytest.fixture
def externally_managed_scanner():
    return PythonExternallyManagedScanner()

def test_inspect_environment_success(externally_managed_scanner, monkeypatch, fake_result):
    def fake_run(*args, **kwargs):
        return fake_result(
            returncode=0,
            stdout=json.dumps({
                "is_managed": True,
                "marker_path": "/fake/lib/python-3.12/EXTERNALLY-MANAGED",
                "is_venv": True
            })
        )

    monkeypatch.setattr(
        subprocess,
        "run",
        fake_run
    )
    result = externally_managed_scanner._inspect_environment("/fake/python")

    assert result["is_managed"] == True
    assert result["marker_path"] == "/fake/lib/python-3.12/EXTERNALLY-MANAGED"
    assert result["is_venv"] == True

def test_inspect_environment_invalid_json(externally_managed_scanner, monkeypatch, fake_result):
    def fake_run(*args, **kwargs):
        return fake_result(
            returncode=0,
            stdout="not a json"
        )

    monkeypatch.setattr(
        subprocess,
        "run",
        fake_run
    )
    result = externally_managed_scanner._inspect_environment("/fake/python")

    assert result is None

def test_inspect_environment_command_exception(externally_managed_scanner, monkeypatch):
    def fake_run(*args, **kwargs):
        raise OSError("Subprocess failed to launch")

    monkeypatch.setattr(
        subprocess,
        "run",
        fake_run
    )
    result = externally_managed_scanner._inspect_environment("/fake/python")

    assert result is None

def test_python_not_found(externally_managed_scanner, monkeypatch):
    monkeypatch.setattr(
        PythonUtilities,
        "find_python",
        lambda self, *args: None
    )
    result = externally_managed_scanner.scan()

    assert result.status == ScanStatus.FAIL
    assert result.evidence == {}
    assert result.warnings == []
    assert result.errors == ["Unable to find a usable Python interpreter"]

def test_probe_payload_none(externally_managed_scanner, monkeypatch):
    monkeypatch.setattr(
        PythonUtilities,
        "find_python",
        lambda self, *args: "/fake/python"
    )

    monkeypatch.setattr(
        PythonExternallyManagedScanner,
        "_inspect_environment",
        lambda self, *args: None
    )
    result = externally_managed_scanner.scan()

    assert result.status == ScanStatus.FAIL
    assert result.evidence == {}
    assert result.warnings == []
    assert result.errors == ["Failed to inspect Python environment management status"]

@pytest.mark.parametrize("is_managed, is_venv, status, expected_errors",[
    (False, False, ScanStatus.PASS, []),
    (True, True, ScanStatus.PASS, []),
    (True, False, ScanStatus.FAIL, ["Python environment is externally managed (PEP 668). Use a virtual environment to install packages."])
])
def test_externally_managed_evaluation(externally_managed_scanner, monkeypatch, is_managed, is_venv, status, expected_errors):
    monkeypatch.setattr(
        PythonUtilities,
        "find_python",
        lambda self, *args: "/fake/python"
    )

    monkeypatch.setattr(
        PythonExternallyManagedScanner,
        "_inspect_environment",
        lambda self, *args: {
            "is_managed": is_managed,
            "marker_path": "/fake/lib/python-3.12/EXTERNALLY-MANAGED",
            "is_venv": is_venv
        }
    )
    result = externally_managed_scanner.scan()

    assert result.status == status
    assert result.errors == expected_errors