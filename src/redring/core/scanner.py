from abc import ABC, abstractmethod
from .models.status import ScanStatus

class BaseScanner(ABC):
    @classmethod
    @abstractmethod
    def capability(cls) -> str:
        ...
        
    @abstractmethod
    def scan(self) -> ScanStatus:
        """Execute the scan and return collected evidences"""
        ...