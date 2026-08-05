from __future__ import annotations
from redring.core.registry import ScannerRegistry
from redring.core.models.result import ScanResult
from redring.core.models.status import ScanStatus

class Engine:
    def run(self, stack:str) -> list[ScanResult]:
        scanners = ScannerRegistry.get_by_prefix(stack)
        results = []
        for scanner in scanners:
            try:
                scanner_instance = scanner()
                results.append(scanner_instance.scan())
            except Exception as e:
                results.append(ScanResult(
                    capability=scanner.capability(),
                    status=ScanStatus.FAIL,
                    evidence={},
                    warnings={},
                    errors=[str(e)]
                ))
        return results