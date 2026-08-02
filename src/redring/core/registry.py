from .scanner import BaseScanner

class ScannerRegistry():
    _registry: dict[str, type[BaseScanner]] = {}

    @classmethod
    def register(cls, scanner: type[BaseScanner]):
        cls._registry[scanner.capability()] = scanner

    @classmethod
    def get(cls, capability: str) -> type[BaseScanner] | None:
        return cls._registry.get(capability)

    @classmethod
    def list(cls) -> list[str]:
        return list(cls._registry.keys())

    @classmethod
    def get_by_prefix(cls, stack:str) -> list[type[BaseScanner]]:
        """Returns the list of available scanners for provided tech stack."""
        scanners = []
        for capability, scanner in cls._registry.items():
            if capability.startswith(f"{stack.lower()}."):
                scanners.append(scanner)
        return scanners