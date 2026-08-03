import subprocess
from redring.core.scanner import BaseScanner
from redring.core.registry import ScannerRegistry
from redring.core.models.result import ScanResult
from redring.core.models.status import ScanStatus

class PythonVersionScanner(BaseScanner):
    @classmethod
    def capability(cls) -> str:
        return "python.version"

    def scan(self) -> ScanResult:
        for command in ("python", "python3"):
            version = subprocess.run([command, "--version"], capture_output=True, text=True)
            if version.returncode == 0:
                return ScanResult(
                    capability=self.capability(),
                    status=ScanStatus.PASS,
                    evidence={
                        "version": version.stdout.strip().replace("Python ", ""),
                        "command": command
                    },
                    warnings=[],
                    errors=[]
                )
        return ScanResult(
            capability=self.capability(),
            status=ScanStatus.FAIL,
            evidence={},
            warnings=[],
            errors=["Python is not installed"]
        )

ScannerRegistry.register(PythonVersionScanner)