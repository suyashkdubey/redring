import pytest
from dataclasses import dataclass

@dataclass(frozen=True)
class FakeResult:
    returncode: int
    stdout: str
    stderr: str = ""

@pytest.fixture
def fake_result():
    def _factory(returncode: int, stdout: str, stderr: str = ""):
        return FakeResult(returncode=returncode, stdout=stdout, stderr=stderr)
    return _factory