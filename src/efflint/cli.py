import json
from pathlib import Path

import typer

from efflint.adapters.jsonl import load_jsonl
from efflint.analyzer import Analyzer
from efflint.reporters.console import print_report


app = typer.Typer(
    help=(
        "EffLint analyzes LLM and agent traces "
        "for potential execution inefficiencies."
        )
    )


@app.command()
def analyze(
    path: Path = typer.Argument(
        ...,
        help="Path to normalized JSONL trace file.",
        exists=True,
        readable=True,
    ),
    output_json: Path | None = typer.Option(
        None,
        "--output-json",
        "-o",
        help="Optionally write the report as JSON.",
    ),
) -> None:
    """
    Analyze an LLM trace file.
    """

    calls = load_jsonl(path)
    
    analyzer = Analyzer()
    
    report = analyzer.run(calls)
    
    print_report(report)
    
    if output_json:

        output_json.write_text(
            json.dumps(
                report.model_dump(
                    mode="json"
                ),
                indent=2,
            ),
            encoding="utf-8",
        )

        typer.echo(
            f"\nReport written to "
            f"{output_json}"
        )


if __name__ == "__main__":
    app()