from __future__ import annotations

from redring.core.registry import ScannerRegistry
from redring.core.models.result import ScanResult
from redring.core.models.status import ScanStatus
from redring.core.logging import configure_logging

logger = configure_logging()

class Engine:
    def run(self, stack: str) -> list[ScanResult]:
        logger.info("Engine started | stack=%s", stack)
        scanners = ScannerRegistry.get_by_prefix(stack)
        results = []
        for scanner in scanners:
            try:
                scanner_instance = scanner()
                logger.debug(
                    "Running scanner | %s",
                    scanner_instance.capability()
                )
                result = scanner_instance.scan()
                results.append(result)
                logger.debug(
                    "Scanner completed | %s",
                    scanner_instance.capability()
                )
            except Exception as e:
                logger.error(
                    "Scanner %s failed to complete | Error=%s",
                    scanner.capability(),
                    e
                )
                results.append(
                    ScanResult(
                        capability=scanner.capability(),
                        status=ScanStatus.FAIL,
                        evidence={},
                        warnings=[],
                        errors=[str(e)]
                    )
                )
        logger.info("Engine completed | stack=%s", stack)
        return results