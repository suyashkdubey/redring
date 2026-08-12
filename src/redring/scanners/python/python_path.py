import subprocess
from pathlib import Path
from redring.core.registry import ScannerRegistry
from redring.core.scanner import BaseScanner
from redring.core.models.result import ScanResult
from redring.core.models.status import ScanStatus
from redring.scanners.os.os_info import OSInfo
from redring.core.logging import configure_logging
from redring.utils.python import PythonUtilities

logger = configure_logging()

class PythonPathScanner(BaseScanner):
    @classmethod
    def capability(cls) -> str:
        return "python.path"

    def scan(self) -> ScanResult:
        system = self._detect_system()
        logger.debug("Detected system=%s", system)
        if not system:
            logger.warning("Unable to detect the operating system")
            return ScanResult(
                capability=self.capability(),
                status=ScanStatus.UNKNOWN,
                evidence={},
                warnings=[],
                errors=["Unable to determine the host operating system"]
            )

        python_executable = PythonUtilities().find_python()
        if python_executable:
            command = Path(python_executable).name
            logger.debug(
                "Resolved Python executable | command=%s | executable=%s",
                command,
                python_executable,
            )
            return self._build_result(command, python_executable, system)

        logger.warning("Python executable not found in PATH")
        return ScanResult(
            capability=self.capability(),
            status=ScanStatus.FAIL,
            evidence={
                "system": system,
                "attempted_commands": list(self._candidate_commands(system)),
            },
            warnings=[],
            errors=["Python executable not found on PATH"]
        )

    def _detect_system(self) -> str:
        info = OSInfo().scan()
        system = info.evidence.get("system")
        if not isinstance(system, str):
            return ""
        return system.strip().lower()

    def _candidate_commands(self, system: str) -> tuple[str, ...]:
        if system == "windows":
            return ("python","py")
        return ("python", "python3")

    def _build_result(self, command: str, executable: str, system: str) -> ScanResult:
        return ScanResult(
            capability=self.capability(),
            status=ScanStatus.PASS,
            evidence={
                "system": system,
                "command": command,
                "executable": executable
            },
            warnings=[],
            errors=[]
        )

ScannerRegistry.register(PythonPathScanner)