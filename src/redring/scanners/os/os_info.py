import platform
from typing import Any, Dict
from redring.core.registry import ScannerRegistry
from redring.core.scanner import BaseScanner
from redring.core.models.result import ScanResult
from redring.core.models.status import ScanStatus

class OSInfo(BaseScanner):
    """Helper scanner providing OS-level context to other scanners."""

    @classmethod
    def capability(cls) -> str:
        return "os.info"

    def scan(self) -> ScanResult:
        evidence: Dict[str, Any] = {
            "system": platform.system(),
            "release": platform.release(),
            "build_version": platform.version(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
        }

        # Include freedesktop OS release metadata on compatible Linux systems
        if hasattr(platform, "freedesktop_os_release"):
            try:
                evidence["os_release_details"] = platform.freedesktop_os_release()
            except OSError:
                evidence["os_release_details"] = {}

        return ScanResult(
            capability=self.capability(),
            status=ScanStatus.PASS,
            evidence=evidence,
        )


ScannerRegistry.register(OSInfo)