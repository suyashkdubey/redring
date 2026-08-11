import subprocess
from redring.core.scanner import BaseScanner
from redring.core.registry import ScannerRegistry
from redring.core.models.result import ScanResult
from redring.core.models.status import ScanStatus
from redring.core.logging import configure_logging

logger = configure_logging()

class PythonVersionScanner(BaseScanner):
    @classmethod
    def capability(cls) -> str:
        return "python.version"

    def scan(self) -> ScanResult:
        for command in ("python", "python3"):
            logger.debug("Checking Python command | command=%s", command)
            version = subprocess.run([command, "--version"], capture_output=True, text=True)
            if version.returncode == 0:
                detected_version = version.stdout.strip().replace("Python ", "")
                logger.debug("Python version detected | command=%s | version=%s", command, detected_version)
                return ScanResult(
                    capability=self.capability(),
                    status=ScanStatus.PASS,
                    evidence={
                        "version": detected_version,
                        "command": command
                    },
                    warnings=[],
                    errors=[]
                )
            logger.debug("Python version command failed | command=%s | returncode=%d", command, version.returncode)
        logger.warning("Failed to detect Python version")
        return ScanResult(
            capability=self.capability(),
            status=ScanStatus.FAIL,
            evidence={},
            warnings=[],
            errors=["Python is not installed"]
        )

ScannerRegistry.register(PythonVersionScanner)