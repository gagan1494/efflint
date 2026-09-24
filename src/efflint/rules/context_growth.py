from collections import defaultdict

from efflint.rules.base import (
    Confidence,
    Finding,
    Rule,
    Severity,
)
from efflint.schema.trace import LLMCall


class ContextGrowthRule(Rule):
    rule_id = "EFF001"
    title = "Rapid context growth"

    def __init__(
        self,
        growth_threshold: float = 3.0,
        minimum_calls: int = 3,
    ):
        self.growth_threshold = growth_threshold
        self.minimum_calls = minimum_calls

    def analyze(
        self,
        calls: list[LLMCall],
    ) -> list[Finding]:

        traces: dict[str, list[LLMCall]] = (
            defaultdict(list)
        )

        for call in calls:
            traces[call.trace_id].append(call)

        findings: list[Finding] = []

        for trace_id, trace_calls in traces.items():

            trace_calls = sorted(
                trace_calls,
                key=lambda call: (
                    call.timestamp is None,
                    call.timestamp,
                ),
            )

            if (
                len(trace_calls)
                < self.minimum_calls
            ):
                continue

            token_counts = [
                call.usage.input_tokens
                for call in trace_calls
            ]

            first = token_counts[0]
            last = token_counts[-1]

            if first <= 0:
                continue

            growth_ratio = last / first

            if (
                growth_ratio
                < self.growth_threshold
            ):
                continue

            findings.append(
                Finding(
                    rule_id=self.rule_id,
                    title=self.title,
                    severity=Severity.MEDIUM,
                    confidence=Confidence.HEURISTIC,
                    trace_id=trace_id,
                    message=(
                        "Input context increased "
                        f"{growth_ratio:.1f}x across "
                        f"{len(trace_calls)} LLM calls."
                    ),
                    recommendation=(
                        "Inspect accumulated conversation "
                        "history, retrieved context, and "
                        "tool results for unnecessary growth."
                    ),
                    evidence={
                        "first_input_tokens": first,
                        "last_input_tokens": last,
                        "growth_ratio": round(
                            growth_ratio,
                            3,
                        ),
                        "calls": len(trace_calls),
                    },
                )
            )

        return findings