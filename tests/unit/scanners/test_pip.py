import subprocess
import pytest
from redring.core.models.status import ScanStatus
from redring.utils.python import PythonUtilities
from redring.scanners.python.python_pip import PythonPipScanner

@pytest.fixture
def pip_scanner():
    return PythonPipScanner()

def test_python_detection_failure(pip_scanner, monkeypatch):
    monkeypatch.setattr(
        PythonUtilities,
        "find_python",
        lambda self: None
    )
    def fake_pip_info(*args):
        raise AssertionError("_get_pip_info should not be called")

    monkeypatch.setattr(
        PythonPipScanner,
        "_get_pip_info",
        fake_pip_info
    )
    result = pip_scanner.scan()

    assert result.status == ScanStatus.FAIL
    assert result.evidence == {}
    assert result.warnings == []
    assert result.errors == ["Unable to find a usable Python interpreter"]

def test_pip_detection_failure(pip_scanner, monkeypatch):
    monkeypatch.setattr(
        PythonUtilities,
        "find_python",
        lambda self: "/fake/python"
    )
    monkeypatch.setattr(
        PythonPipScanner,
        "_get_pip_info",
        lambda self, *args: None
    )
    result = pip_scanner.scan()

    assert result.status == ScanStatus.FAIL
    assert result.evidence["python"] == "/fake/python"
    assert result.warnings == []
    assert result.errors == ["pip is not available for this Python interpreter"]

def test_pip_matches_active_env(pip_scanner, monkeypatch):
    monkeypatch.setattr(
        PythonUtilities,
        "find_python",
        lambda self: "/project/.venv/bin/python"
    )
    monkeypatch.setattr(
        PythonPipScanner,
        "_get_pip_info",
        lambda self, *args: ("","/project/.venv/lib/python3.14/site-packages/pip","")
    )

    monkeypatch.setattr(
        PythonPipScanner,
        "_get_python_prefix",
        lambda self,*args: "/project/.venv"
    )

    monkeypatch.setattr(
        PythonPipScanner,
        "_is_inside_environment",
        lambda self, *args: True
    )

    result = pip_scanner.scan()

    assert result.status == ScanStatus.PASS
    assert result.evidence["python"] == "/project/.venv/bin/python"
    assert result.evidence["python_prefix"] == "/project/.venv"
    assert result.evidence["pip_location"] == "/project/.venv/lib/python3.14/site-packages/pip"
    assert result.evidence["same_environment"] == True
    assert result.warnings == []
    assert result.errors == []

def test_pip_mismatches_active_env(pip_scanner, monkeypatch):
    monkeypatch.setattr(
        PythonUtilities,
        "find_python",
        lambda self: "/somewhere/else/python"
    )

    monkeypatch.setattr(
        PythonPipScanner,
        "_get_pip_info",
        lambda self, *args: ("", "/somewhere/else/site-packages/pip", "")
    )

    monkeypatch.setattr(
        PythonPipScanner,
        "_get_python_prefix",
        lambda self, *args: "/project/.venv"
    )

    monkeypatch.setattr(
        PythonPipScanner,
        "_is_inside_environment",
        lambda self, *args: False
    )

    result = pip_scanner.scan()

    assert result.status == ScanStatus.WARNING
    assert result.evidence["python"] == "/somewhere/else/python"
    assert result.evidence["python_prefix"] == "/project/.venv"
    assert result.evidence["pip_location"] == "/somewhere/else/site-packages/pip"
    assert result.evidence["same_environment"] == False
    assert result.warnings == ["pip location does not appear to belong to the Python environment"]
    assert result.errors == []

# NOTE: Structured as a parametrized test to facilitate adding diverse stdout formats, legacy versions, and edge cases
@pytest.mark.parametrize("text, pip_version, pip_location, python_version",[
    ("pip 26.2.1 from /fake/site-packages/pip (python 3.12)", "26.2.1", "/fake/site-packages/pip", "3.12")
])
def test_get_pip_info_success(pip_scanner, monkeypatch, fake_result, text, pip_version, pip_location, python_version):
    def fake_run(*args, **kwargs):
        return fake_result(
            returncode=0,
            stdout=text
        )
    monkeypatch.setattr(
        subprocess,
        "run",
        fake_run
    )
    result = pip_scanner._get_pip_info("/fake/python")

    assert result[0] == pip_version
    assert result[1] == pip_location
    assert result[2] == python_version

def test_get_pip_info_failure(pip_scanner, monkeypatch, fake_result):
    def fake_run(*args, **kwargs):
        return fake_result(
            returncode=1,
            stdout="",
            stderr="fake error"
        )
    monkeypatch.setattr(
        subprocess,
        "run",
        fake_run
    )
    result = pip_scanner._get_pip_info("/fake/python")

    assert result is None

def test_get_pip_info_regex_failure(pip_scanner, monkeypatch, fake_result):
    def fake_run(*args, **kwargs):
        return fake_result(
            returncode=0,
            stdout="this is not pip version output"
        )
    monkeypatch.setattr(
        subprocess,
        "run",
        fake_run
    )
    result = pip_scanner._get_pip_info("/fake/python")

    assert result is None

def test_get_python_prefix_success(pip_scanner, monkeypatch, fake_result):
    def fake_run(*args, **kwargs):
        return fake_result(
            returncode=0,
            stdout="/project/.venv\n"
        )
    monkeypatch.setattr(
        subprocess,
        "run",
        fake_run
    )
    result = pip_scanner._get_python_prefix("/fake/python")

    assert result == "/project/.venv"

def test_get_python_prefix_failure(pip_scanner, monkeypatch, fake_result):
    def fake_run(*args, **kwargs):
        return fake_result(
            returncode=1,
            stdout="",
            stderr="this is fake error"
        )
    monkeypatch.setattr(
        subprocess,
        "run",
        fake_run
    )
    result = pip_scanner._get_python_prefix("/fake/python")

    assert result is None

def test_get_python_prefix_empty_output(pip_scanner, monkeypatch, fake_result):
    def fake_run(*args, **kwargs):
        return fake_result(
            returncode=0,
            stdout=""
        )
    monkeypatch.setattr(
        subprocess,
        "run",
        fake_run
    )
    result = pip_scanner._get_python_prefix("/fake/python")

    assert result is None

def test_is_inside_env_success(pip_scanner, tmp_path):
    prefix_path = tmp_path / ".venv"
    pip_path = prefix_path / "lib" / "python-3.14" / "site-packages" / "pip"

    pip_path.mkdir(parents=True)

    result = pip_scanner._is_inside_environment(str(pip_path), str(prefix_path))

    assert result is True

def test_is_inside_env_failure_outside_path(pip_scanner, tmp_path):
    prefix_path = tmp_path / "project" / ".venv"
    pip_path = tmp_path / "global" / "lib" / "site-packages" / "pip"

    prefix_path.mkdir(parents=True)
    pip_path.mkdir(parents=True)

    result = pip_scanner._is_inside_environment(str(pip_path), str(prefix_path))

    assert result is False

def test_is_inside_env_handles_oserror(pip_scanner, monkeypatch):
    from pathlib import Path

    def mock_resolve(*args, **kwargs):
        raise OSError("Mocked permission denied")

    monkeypatch.setattr(Path, "resolve", mock_resolve)
    result = pip_scanner._is_inside_environment("/fake/pip", "/fake/prefix")

    assert result is False