from abc import ABC, abstractmethod
from .models.result import ScanResult

class BaseScanner(ABC):
    @classmethod
    @abstractmethod
    def capability(cls) -> str:
        ...
        
    @abstractmethod
    def scan(self) -> ScanResult:
        """Execute the scan and return collected evidences"""
        ...