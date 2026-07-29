from abc import ABC, abstractmethod
from .models.status import ScanStatus

class BaseScanner(ABC):
    @property
    @abstractmethod
    def capability(self) -> str:
        """Unique capability identifier"""
        ...

    @abstractmethod
    def scan(self) -> ScanStatus:
        """Execute the scan and return collected evidences"""
        ...