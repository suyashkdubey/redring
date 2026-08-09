import sys
from redring.core.models.result import ScanResult
from redring.core.models.status import ScanStatus
from redring.core.registry import ScannerRegistry
from redring.core.scanner import BaseScanner


class PythonVenvScanner(BaseScanner):
    @classmethod
    def capability(cls) -> str:
        return "python.venv"

    def scan(self) -> ScanResult:
        prefix = sys.prefix
        base_prefix = sys.base_prefix
        executable = sys.executable

        active = prefix != base_prefix

        return ScanResult(
            capability=self.capability(),
            status=ScanStatus.PASS if active else ScanStatus.WARNING,
            evidence={
                "active": "yes" if active else "no",
                "location": prefix if active else None,
                "python": executable,
                "base_python": base_prefix,
            },
            warnings=[] if active else [
                "No virtual environment is currently active"
            ],
            errors=[]
        )


ScannerRegistry.register(PythonVenvScanner)