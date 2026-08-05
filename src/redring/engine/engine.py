from __future__ import annotations
from redring.core.registry import ScannerRegistry
from redring.core.models.result import ScanResult

class Engine:
    def run(self, stack:str) -> list[ScanResult]:
        scanners = ScannerRegistry.get_by_prefix(stack)
        results = []
        for scanner in scanners:
            scanner_instance = scanner()
            results.append(scanner_instance.scan())
        return results