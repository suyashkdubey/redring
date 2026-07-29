from abc import ABC, abstractmethod
from .models.status import ScanStatus

class BaseScanner(ABC):
    @property
    @abstractmethod
    def capability(self) -> None:
        pass