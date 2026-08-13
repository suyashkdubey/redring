from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from .base import BaseRenderer
from redring.core.models.result import ScanResult
from redring.core.models.status import ScanStatus

_STATUS_MAP:dict[ScanStatus, str] = {
    ScanStatus.PASS : ":white_check_mark: [bold green]PASS[/bold green]",
    ScanStatus.FAIL : ":x: [bold red]FAIL[/bold red]",
    ScanStatus.WARNING : ":warning: [bold yellow]WARNING[/bold yellow]",
    ScanStatus.UNKNOWN : ":grey_question: [bold grey]UNKNOWN[/bold grey]"
}

class CLIRenderer(BaseRenderer):
    def _build_status_text(self, result: ScanResult) -> Text:
        status_str = _STATUS_MAP.get(result.status, "")
        return Text.from_markup(status_str)

    def _build_evidence_table(self, result: ScanResult) -> Panel[Table, str] | None:
        table = Table()
        if not result.evidence:
            table.add_row("No evidence found")
            return Panel(table, title=result.capability)
        table.add_column("Evidence")
        table.add_column("Value")
        for key, value in result.evidence.items():
            # Ensure both key and value are renderable strings
            table.add_row(str(key), str(value))
        return Panel(table, title=result.capability)

    def _build_issues(self, result: ScanResult) -> tuple[Panel | None, Panel | None]:
        warning_panel: Panel | None = None
        error_panel: Panel | None = None
        if result.warnings:
            warning_text = "\n".join(f"• {warning}" for warning in result.warnings)
            warning_panel = Panel(
                warning_text,
                title="⚠️  Warnings",
                title_align="left",
                border_style="bold yellow",
                expand=False
            )
        if result.errors:
            error_text = "\n".join(f"• {error}" for error in result.errors)
            error_panel = Panel(
                error_text,
                title="❌  Errors",
                title_align="left",
                border_style="bold red",
                expand=False
            )
        return warning_panel, error_panel

    def _build_result_content(self, result: ScanResult) -> Group:
        status = self._build_status_text(result)
        evidence = self._build_evidence_table(result)
        warnings, errors = self._build_issues(result)
        renderables = [status]
        if evidence is not None:
            renderables.append(evidence)
        if warnings is not None:
            renderables.append(warnings)
        if errors is not None:
            renderables.append(errors)
        return Group(*renderables)

    def render(self, results: list[ScanResult]):
        console = Console()
        for result in results:
            content = self._build_result_content(result)
            console.print(content)