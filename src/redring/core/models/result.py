from dataclasses import dataclass, field
from typing import Any
from .status import ScanStatus

@dataclass(frozen=True)
class ScanResult:
    capability: str
    status: ScanStatus
    evidence: dict[str, Any]
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)