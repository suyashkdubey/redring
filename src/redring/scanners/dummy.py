from redring.core.models.result import ScanResult
from redring.core.models.status import ScanStatus
from redring.core.scanner import BaseScanner
from redring.core.registry import ScannerRegistry

class DummyScanner(BaseScanner):
    @classmethod
    def capability(cls) -> str:
        return "dummy.test"

    def scan(self) -> ScanResult:
        return ScanResult(
            capability=self.capability(),
            status=ScanStatus.PASS,
            evidence= {"message": "Everything working properly"},
            warnings=[],
            errors=[]
        )

ScannerRegistry.register(DummyScanner)