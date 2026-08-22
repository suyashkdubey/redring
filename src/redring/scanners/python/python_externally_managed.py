import json
import subprocess
from redring.core.models.result import ScanResult
from redring.core.models.status import ScanStatus
from redring.core.registry import ScannerRegistry
from redring.core.scanner import BaseScanner
from redring.core.logging import configure_logging
from redring.utils.python import PythonUtilities

logger = configure_logging()

class PythonExternallyManagedScanner(BaseScanner):
    @classmethod
    def capability(cls) -> str:
        return "python.externally_managed"

    def _inspect_environment(self, python_executable: str) -> dict | None:
        try:
            logger.debug("Probing environment management status | executable=%s", python_executable)
            payload = subprocess.run([python_executable, "-c", '''
                        import json, sys, sysconfig
                        from pathlib import Path
                        
                        is_venv = sys.prefix != sys.base_prefix
                        marker = Path(sysconfig.get_path("stdlib")) / "EXTERNALLY-MANAGED"
                        exists = marker.is_file()
                        
                        payload = {
                            "is_managed": exists,
                            "marker_path": str(marker) if exists else None,
                            "is_venv": is_venv,
                        }
                        print(json.dumps(payload))
                    '''], capture_output=True, text=True)
            return json.loads(payload.stdout) or None
        except (json.JSONDecodeError, Exception) as e:
            logger.warning("Failed to probe environment management | executable=%s | error=%s", python_executable, e)
            return None

    def scan(self) -> ScanResult:
        logger.debug("Checking for externally managed python")
        python_executable = PythonUtilities().find_python()
        if python_executable is None:
            logger.warning("Unable to find a usable Python interpreter")
            return ScanResult(
                capability=self.capability(),
                status=ScanStatus.FAIL,
                evidence={},
                warnings=[],
                errors=["Unable to find a usable Python interpreter"]
            )
        logger.debug("Found python executable | executable=%s", python_executable)
        probe_payload = self._inspect_environment(python_executable)
        if probe_payload is None:
            logger.warning("Failed to inspect Python environment management status | executable=%s", python_executable)
            return ScanResult(
                capability=self.capability(),
                status=ScanStatus.FAIL,
                evidence={},
                warnings=[],
                errors=["Failed to inspect Python environment management status"]
            )

        evidence = {
            "is_managed": probe_payload["is_managed"],
            "marker_path": probe_payload["marker_path"],
            "is_venv": probe_payload["is_venv"]
        }
        
        if not probe_payload["is_managed"] or probe_payload["is_venv"]:
            logger.debug("PEP 668 status resolved | is_managed=%s | is_venv=%s | status=%s", probe_payload["is_managed"], probe_payload["is_venv"], ScanStatus.PASS)
            return ScanResult(
                capability=self.capability(),
                status=ScanStatus.PASS,
                evidence=evidence,
                warnings=[],
                errors=[]
            )
        else:
            logger.debug("PEP 668 status resolved | is_managed=%s | is_venv=%s | status=%s", probe_payload["is_managed"], probe_payload["is_venv"], ScanStatus.FAIL)
            return ScanResult(
                capability=self.capability(),
                status=ScanStatus.FAIL,
                evidence=evidence,
                warnings=[],
                errors=["Python environment is externally managed (PEP 668). Use a virtual environment to install packages."]
            )
        
ScannerRegistry.register(PythonExternallyManagedScanner)