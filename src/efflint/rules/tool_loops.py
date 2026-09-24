from collections import Counter

from efflint.rules.base import (
    Confidence,
    Finding,
    Rule,
    Severity,
)
from efflint.schema.trace import LLMCall


class ToolLoopRule(Rule):
    rule_id = "EFF004"
    title = "Repeated tool invocation"

    def __init__(
        self,
        repeat_threshold: int = 3,
    ):
        self.repeat_threshold = (
            repeat_threshold
        )

    def analyze(
        self,
        calls: list[LLMCall],
    ) -> list[Finding]:

        findings: list[Finding] = []

        for call in calls:

            signatures = [
                (
                    tool_call.name,
                    tool_call.arguments_fingerprint,
                )
                for tool_call in call.tool_calls
            ]

            counts = Counter(signatures)

            for (
                tool_name,
                arguments_fingerprint,
            ), count in counts.items():

                if count < self.repeat_threshold:
                    continue

                findings.append(
                    Finding(
                        rule_id=self.rule_id,
                        title=self.title,
                        severity=Severity.HIGH,
                        confidence=(
                            Confidence.DETERMINISTIC
                        ),
                        trace_id=call.trace_id,
                        message=(
                            f"Tool '{tool_name}' was "
                            f"called {count} times with "
                            "the same argument "
                            "fingerprint."
                        ),
                        recommendation=(
                            "Inspect agent termination "
                            "logic, retry handling, and "
                            "tool-result interpretation."
                        ),
                        evidence={
                            "tool": tool_name,
                            "repeat_count": count,
                            "arguments_fingerprint": (
                                arguments_fingerprint
                            ),
                        },
                    )
                )

        return findings