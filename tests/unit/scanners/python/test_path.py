import pytest
from redring.core.models.status import ScanStatus
from redring.scanners.python.python_path import PythonPathScanner
from redring.utils.python import PythonUtilities

@pytest.fixture
def path_scanner():
    return PythonPathScanner()

@pytest.mark.parametrize("system, executable, expected_command",[
    ("linux", "/fake/python3", "python3"),
    ("windows", "/fake/python", "python"),
    ("darwin", "/fake/python3", "python3"),
])
def test_path_detection_success(path_scanner, monkeypatch, system, executable, expected_command):
    monkeypatch.setattr(
        PythonPathScanner,
        "_detect_system",
        lambda self: system
    )
    monkeypatch.setattr(
        PythonUtilities,
        "find_python",
        lambda self: executable
    )
    result = path_scanner.scan()

    assert result.status == ScanStatus.PASS
    assert result.evidence["system"] == system
    assert result.evidence["executable"] == executable
    assert result.evidence["command"] == expected_command
    assert result.warnings == []
    assert result.errors == []

@pytest.mark.parametrize("system, commands", [
    ("linux", ["python", "python3"]),
    ("windows", ["python", "py"]),
    ("darwin", ["python", "python3"])
])
def test_python_detection_failure(path_scanner, monkeypatch, system, commands):
    monkeypatch.setattr(
        PythonPathScanner,
        "_detect_system",
        lambda self: system
    )
    monkeypatch.setattr(
        PythonUtilities,
        "find_python",
        lambda self: None
    )
    result = path_scanner.scan()

    assert result.status == ScanStatus.FAIL
    assert result.evidence["system"] == system
    assert result.evidence["attempted_commands"] == commands
    assert result.warnings == []
    assert result.errors == ["Python executable not found on PATH"]

def test_system_detection_failure(path_scanner, monkeypatch):
    monkeypatch.setattr(
        PythonPathScanner,
        "_detect_system",
        lambda self: ""
    )

    def fake_python_run(self):
        raise AssertionError("python path should not be called")
    
    monkeypatch.setattr(
        PythonUtilities,
        "find_python",
        fake_python_run
    )

    result = path_scanner.scan()

    assert result.status == ScanStatus.UNKNOWN
    assert result.evidence == {}
    assert result.warnings == []
    assert result.errors == ["Unable to determine the host operating system"]