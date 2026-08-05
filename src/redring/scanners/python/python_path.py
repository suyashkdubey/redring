import subprocess
from redring.core.registry import ScannerRegistry
from redring.core.scanner import BaseScanner
from redring.core.models.result import ScanResult
from redring.core.models.status import ScanStatus
from redring.scanners.os.os_info import OSInfo


class PythonPathScanner(BaseScanner):
    @classmethod
    def capability(cls) -> str:
        return "python.path"

    def scan(self) -> ScanResult:
        system = self._detect_system()
        if not system:
            return ScanResult(
                capability=self.capability(),
                status=ScanStatus.UNKNOWN,
                evidence={},
                warnings=[],
                errors=["Unable to determine the host operating system"]
            )

        for command in self._candidate_commands(system):
            executable = self._resolve_executable(command)
            if executable:
                return self._build_result(command, executable, system)

        return ScanResult(
            capability=self.capability(),
            status=ScanStatus.FAIL,
            evidence={
                "system": system,
                "attempted_commands": list(self._candidate_commands(system))
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
            return ("python", "python3", "py")
        return ("python3", "python")

    def _resolve_executable(self, command: str) -> str | None:
        completed = subprocess.run(
            [command, "-c", "import sys; print(sys.executable)"],
            capture_output=True,
            text=True
        )
        if completed.returncode != 0:
            return None
        return completed.stdout.strip()

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