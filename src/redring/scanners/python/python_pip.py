import re
import subprocess
from redring.core.models.result import ScanResult
from redring.core.models.status import ScanStatus
from redring.core.registry import ScannerRegistry
from redring.core.scanner import BaseScanner
from redring.core.logging import configure_logging
from redring.utils.python import PythonUtilities

logger = configure_logging()

class PythonPipScanner(BaseScanner):
    @classmethod
    def capability(cls) -> str:
        return "python.pip"

    def scan(self) -> ScanResult:
        logger.debug("Checking pip for the active Python interpreter")
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
        logger.debug(
            "Python interpreter resolved | executable=%s",
            python_executable,
        )
        pip_info = self._get_pip_info(python_executable)
        if pip_info is None:
            logger.warning("pip is not available for Python | executable=%s",python_executable)
            return ScanResult(
                capability=self.capability(),
                status=ScanStatus.FAIL,
                evidence={
                    "python": python_executable,
                },
                warnings=[],
                errors=["pip is not available for this Python interpreter"],
            )
        pip_version, pip_location, pip_python_version = pip_info
        logger.debug(
            "pip detected | version=%s | location=%s | python=%s",
            pip_version,
            pip_location,
            pip_python_version,
        )
        python_prefix = self._get_python_prefix(python_executable)
        same_environment = False
        if python_prefix and pip_location:
            same_environment = self._is_inside_environment(
                pip_location,
                python_prefix,
            )
        logger.debug(
            "pip environment check | prefix=%s | same_environment=%s",
            python_prefix,
            same_environment,
        )
        warnings = []
        if python_prefix and not same_environment:
            warnings.append(
                "pip location does not appear to belong to the Python environment"
            )
        return ScanResult(
            capability=self.capability(),
            status=(
                ScanStatus.WARNING
                if warnings
                else ScanStatus.PASS
            ),
            evidence={
                "python": python_executable,
                "python_prefix": python_prefix,
                "pip_version": pip_version,
                "pip_location": pip_location,
                "pip_python_version": pip_python_version,
                "same_environment": same_environment,
            },
            warnings=warnings,
            errors=[],
        )

    def _get_pip_info(self, python_executable: str) -> tuple[str, str, str] | None:
        result = subprocess.run(
            [python_executable,"-m","pip","--version"],capture_output=True,text=True)
        if result.returncode != 0:
            logger.debug(
                "python -m pip failed | returncode=%d | stderr=%s",
                result.returncode,
                result.stderr.strip(),
            )
            return None
        output = result.stdout.strip()
        match = re.match(r"pip\s+(\S+)\s+from\s+(.+?)\s+\(python\s+([^)]+)\)", output)
        if not match:
            logger.warning("Unable to parse pip version output | output=%s",output)
            return None

        pip_version = match.group(1)
        pip_location = match.group(2)
        python_version = match.group(3)
        return pip_version, pip_location, python_version

    def _get_python_prefix(self, python_executable: str) -> str | None:
        result = subprocess.run(
            [
                python_executable,
                "-c",
                "import sys; print(sys.prefix)",
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            logger.debug(
                "Unable to determine Python prefix | returncode=%d",
                result.returncode,
            )
            return None
        prefix = result.stdout.strip()
        return prefix or None

    def _is_inside_environment(self,pip_location: str,python_prefix: str) -> bool:
        try:
            from pathlib import Path
            pip_path = Path(pip_location).resolve()
            prefix_path = Path(python_prefix).resolve()
            pip_path.relative_to(prefix_path)
            return True
        except (ValueError, OSError):
            return False

ScannerRegistry.register(PythonPipScanner)