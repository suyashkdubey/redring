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