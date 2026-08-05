import platform
from redring.core.registry import ScannerRegistry
from redring.core.scanner import BaseScanner
from redring.core.models.result import ScanResult
from redring.core.models.status import ScanStatus

class OSInfo(BaseScanner):
    @classmethod
    def capability(cls) -> str:
        return "os.info"

    def scan(self) -> ScanResult:
        system = platform.system()
        release = platform.release()
        build_version = platform.version()
        architecture = platform.machine()
        return ScanResult(
            capability=self.capability(),
            status=ScanStatus.PASS,
            evidence={
                "system": system,
                "release": release,
                "build_version": build_version,
                "architecture": architecture
            }
        )

ScannerRegistry.register(OSInfo)