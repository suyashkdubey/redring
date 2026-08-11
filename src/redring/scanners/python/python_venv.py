import sys
from redring.core.models.result import ScanResult
from redring.core.models.status import ScanStatus
from redring.core.registry import ScannerRegistry
from redring.core.scanner import BaseScanner
from redring.core.logging import configure_logging

logger = configure_logging()

class PythonVenvScanner(BaseScanner):
    @classmethod
    def capability(cls) -> str:
        return "python.venv"

    def scan(self) -> ScanResult:
        prefix = sys.prefix
        base_prefix = sys.base_prefix
        executable = sys.executable
        logger.debug("Checking Python virtual environment | executable=%s", executable)
        logger.debug("Python environment prefixes | prefix=%s | base_prefix=%s", prefix, base_prefix)
        active = prefix != base_prefix
        if active:
            logger.debug("Python virtual environment detected | location=%s",prefix)
        else:
            logger.debug("No Python virtual environment is active")
        return ScanResult(
            capability=self.capability(),
            status=ScanStatus.PASS if active else ScanStatus.WARNING,
            evidence={
                "active": "yes" if active else "no",
                "location": prefix if active else None,
                "python": executable,
                "base_prefix": base_prefix,
            },
            warnings=[] if active else [
                "No virtual environment is currently active"
            ],
            errors=[]
        )
    
ScannerRegistry.register(PythonVenvScanner)