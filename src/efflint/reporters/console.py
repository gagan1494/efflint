from collections import Counter

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from efflint.analyzer import AnalysisReport
from efflint.rules.base import Severity


console = Console()


SEVERITY_COLORS = {
    Severity.HIGH: "bold red",
    Severity.MEDIUM: "yellow",
    Severity.LOW: "cyan",
    Severity.INFO: "blue",
}


def print_report(
    report: AnalysisReport,
) -> None:

    console.print()

    console.print(
        Panel.fit(
            "[bold]EffLint v0.1[/bold]\n"
            "GenAI execution efficiency analysis",
            border_style="blue",
        )
    )

    console.print()

    summary = Table(
        title="Workload Summary"
    )

    summary.add_column("Metric")
    summary.add_column(
        "Value",
        justify="right",
    )

    summary.add_row(
        "Calls analyzed",
        f"{report.calls_analyzed:,}",
    )

    summary.add_row(
        "Input tokens",
        f"{report.input_tokens:,}",
    )

    summary.add_row(
        "Output tokens",
        f"{report.output_tokens:,}",
    )

    summary.add_row(
        "Cache reads",
        f"{report.cache_read_tokens:,}",
    )

    summary.add_row(
        "Cache writes",
        f"{report.cache_write_tokens:,}",
    )

    summary.add_row(
        "Reasoning tokens",
        f"{report.reasoning_tokens:,}",
    )

    console.print(summary)

    console.print()

    if not report.findings:

        console.print(
            "[bold green]"
            "✓ No efficiency findings detected."
            "[/bold green]"
        )

        return

    console.print(
        f"[bold]Findings "
        f"({len(report.findings)})[/bold]"
    )

    console.print()

    for finding in report.findings:

        color = SEVERITY_COLORS[
            finding.severity
        ]

        console.print(
            f"[{color}]"
            f"{finding.severity.value.upper()}"
            f"[/{color}] "
            f"[bold]{finding.rule_id}[/bold] "
            f"{finding.title}"
        )

        console.print(
            f"  {finding.message}"
        )

        console.print(
            "  Confidence: "
            f"[bold]{finding.confidence.value.upper()}"
            "[/bold]"
        )

        console.print(
            f"  → {finding.recommendation}"
        )

        console.print()

    counts = Counter(
        finding.severity
        for finding in report.findings
    )

    findings_table = Table(
        title="Finding Summary"
    )

    findings_table.add_column(
        "Severity"
    )

    findings_table.add_column(
        "Count",
        justify="right",
    )

    for severity in [
        Severity.HIGH,
        Severity.MEDIUM,
        Severity.LOW,
        Severity.INFO,
    ]:
        findings_table.add_row(
            severity.value.upper(),
            str(counts.get(severity, 0)),
        )

    console.print(findings_table)