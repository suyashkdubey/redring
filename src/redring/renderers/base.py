from abc import ABC, abstractmethod
from redring.core.models.result import ScanResult

class BaseRenderer(ABC):
    @abstractmethod
    def render(self, results: list[ScanResult]) -> str:
        ...