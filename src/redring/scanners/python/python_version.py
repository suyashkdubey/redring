import subprocess
from redring.core.scanner import BaseScanner
from redring.core.registry import ScannerRegistry
from redring.core.models.result import ScanResult
from redring.core.models.status import ScanStatus
from redring.core.logging import configure_logging
from redring.utils.python import PythonUtilities

logger = configure_logging()

class PythonVersionScanner(BaseScanner):
    @classmethod
    def capability(cls) -> str:
        return "python.version"

    def scan(self) -> ScanResult:
        python_executable = PythonUtilities().find_python()
        if python_executable is None:
            logger.warning("Unable to find a usable Python interpreter")
            return ScanResult(
                capability=self.capability(),
                status=ScanStatus.FAIL,
                evidence={},
                warnings=[],
                errors=["Unable to find a usable Python interpreter"],
            )

        logger.debug("Checking Python version for executable=%s", python_executable)
        version = subprocess.run([python_executable, "--version"], capture_output=True, text=True)
        detected_version = (version.stdout or version.stderr).strip().replace("Python ", "")
        if version.returncode == 0 and detected_version:
            logger.debug(
                "Python version detected | executable=%s | version=%s",
                python_executable,
                detected_version,
            )
            return ScanResult(
                capability=self.capability(),
                status=ScanStatus.PASS,
                evidence={
                    "version": detected_version,
                    "command": python_executable,
                },
                warnings=[],
                errors=[]
            )

        logger.debug(
            "Python version command failed | executable=%s | returncode=%d",
            python_executable,
            version.returncode,
        )
        return ScanResult(
            capability=self.capability(),
            status=ScanStatus.FAIL,
            evidence={"command": python_executable},
            warnings=[],
            errors=["Python is not installed"]
        )

ScannerRegistry.register(PythonVersionScanner)