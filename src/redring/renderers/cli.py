from .base import BaseRenderer
from redring.core.models.result import ScanResult
from redring.core.models.status import ScanStatus

_STATUS_MAP = {
    ScanStatus.PASS: "✅ PASS",
    ScanStatus.FAIL: "❌ FAIL",
    ScanStatus.WARNING: "⚠️ WARNING"
}
_SEPARATOR = "-" * 35

class CLIRenderer(BaseRenderer):
    def _format_capability(self, result:ScanResult, lines: list[str]) -> None:
        parts = result.capability.split(".")
        capability_capitalize = [name.capitalize() for name in parts]
        capability = " ".join(capability_capitalize)
        lines.append(capability)
        lines.append(_SEPARATOR)

    def _format_status(self, result: ScanResult, lines: list[str]) -> None:
        lines.append(f"Status: {_STATUS_MAP[result.status]}")
        lines.append(_SEPARATOR)

    def _format_evidence(self, result: ScanResult, lines: list[str]) -> None:
        lines.append("Evidence:")
        lines.append("")
        max_len = max(
            len(k.replace("_", " ").title())
            for k in result.evidence.keys()
        )
        for key, value in result.evidence.items():
            display_key = key.replace("_", " ").title()
            lines.append(f"• {display_key.ljust(max_len)} : {value}")
        lines.append(_SEPARATOR)

    def _format_issues(self, result: ScanResult, lines: list[str]) -> None:
        if result.warnings:
            lines.append("⚠️ Warnings:")
            for warning in result.warnings:
                lines.append(f"• {warning}")
            lines.append(_SEPARATOR)
        if result.errors:
            lines.append("❌ Errors:")
            for error in result.errors:
                lines.append(f"• {error}")
            lines.append(_SEPARATOR)

    def render(self, results: list[ScanResult]) -> str:
        lines: list[str] = []
        for result in results:
            self._format_capability(result, lines)
            self._format_status(result, lines)
            self._format_evidence(result, lines)
            self._format_issues(result, lines)
            lines.append("="*50)
            lines.append("")
        return "\n".join(lines)