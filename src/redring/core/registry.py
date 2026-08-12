from __future__ import annotations
from .scanner import BaseScanner
from .logging import configure_logging

logger = configure_logging()

class ScannerRegistry():
    _registry: dict[str, type[BaseScanner]] = {}

    @classmethod
    def register(cls, scanner: type[BaseScanner]):
        cls._registry[scanner.capability()] = scanner
        logger.debug("Registered scanner | capability=%s", scanner.capability())

    @classmethod
    def get(cls, capability: str) -> type[BaseScanner] | None:
        logger.debug("fetched %s scanner", capability)
        return cls._registry.get(capability)

    @classmethod
    def list(cls) -> list[str]:
        logger.debug("fetched all the available scanners | Count=%s", list(cls._registry.keys()))
        return list(cls._registry.keys())

    @classmethod
    def get_by_prefix(cls, stack:str) -> list[type[BaseScanner]]:
        """Returns the list of available scanners for provided tech stack."""
        scanners = []
        logger.debug("Started fetching available scanners for stack=%s", stack)
        for capability, scanner in cls._registry.items():
            if capability.startswith(f"{stack.lower()}."):
                logger.debug("Found scanner | capability=%s", scanner.capability())
                scanners.append(scanner)
        logger.debug("Found %s scanners in total", len(scanners))
        return scanners