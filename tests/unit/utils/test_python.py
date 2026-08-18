import pytest
import subprocess
from dataclasses import dataclass
from redring.utils.python import PythonUtilities

# ----- testing ----- #
@pytest.fixture
def utility():
    return PythonUtilities()

@pytest.mark.parametrize("system, expected",[
    ('Windows', "windows"),
    ("Darwin", "darwin"),
    ("Linux", "linux")
])
def test_detect_system(utility, monkeypatch, system, expected):
    monkeypatch.setattr("redring.utils.python.platform.system", lambda: system)
    result = utility._detect_system()
    assert result == expected

def test_detect_system_failure(utility, monkeypatch):
    monkeypatch.setattr("redring.utils.python.platform.system", lambda: "")
    result = utility._detect_system()
    assert result == "unknown"

@pytest.mark.parametrize("system, expected", [
    ("windows", ("python", "py")),
    ("linux", ("python", "python3")),
    ("darwin", ("python", "python3")),
    ("unknown", ())
])
def test_determine_python_command_for_system(utility, monkeypatch, system, expected):
    monkeypatch.setattr(utility, "_detect_system", lambda: system)
    commands = utility._determine_python_command_for_system()
    assert commands == expected

def test_find_python_success(utility, monkeypatch, fake_result):
    def fake_run(*args, **kwargs):
        return fake_result(returncode=0, stdout="/fake/python\n")
    
    monkeypatch.setattr(subprocess, "run", fake_run)
    result = utility.find_python()
    assert result == "/fake/python"

def test_find_python_fallback(utility, monkeypatch, fake_result):
    def fake_run(*args, **kwargs):
        command = args[0][0]
        if command == "python":
            return fake_result(returncode=1, stdout="")
        if command == "python3":
            return fake_result(returncode=0, stdout="/fake/python\n")
        
    monkeypatch.setattr(subprocess, "run", fake_run)
    result = utility.find_python()
    assert result == "/fake/python"

def test_find_python_failure(utility, monkeypatch, fake_result):
    def fake_run(*args, **kwargs):
        command = args[0][0]
        if command == "python":
            return fake_result(returncode=1, stdout="")
        if command == "python3":
            return fake_result(returncode=1, stdout="")
    monkeypatch.setattr(subprocess, "run", fake_run)
    result = utility.find_python()
    assert result is None