import json
from pathlib import Path

from efflint.schema.trace import LLMCall


def load_jsonl(
    path: str | Path,
) -> list[LLMCall]:
    """
    Load normalized EffLint LLM calls from a JSONL file.
    """

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Trace file does not exist: {path}"
        )

    calls: list[LLMCall] = []

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        for line_number, line in enumerate(
            file,
            start=1,
        ):
            line = line.strip()

            if not line:
                continue

            try:
                payload = json.loads(line)

            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON on line "
                    f"{line_number}: {exc}"
                ) from exc

            try:
                call = LLMCall.model_validate(
                    payload
                )

            except Exception as exc:
                raise ValueError(
                    f"Invalid EffLint trace on "
                    f"line {line_number}: {exc}"
                ) from exc

            calls.append(call)

    return calls