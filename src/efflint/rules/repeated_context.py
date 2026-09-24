from collections import defaultdict

from efflint.rules.base import (
    Confidence,
    Finding,
    Rule,
    Severity,
)
from efflint.schema.trace import LLMCall


class RepeatedContextRule(Rule):
    rule_id = "EFF002"
    title = "Repeated context detected"

    def __init__(
        self,
        minimum_occurrences: int = 3,
    ):
        self.minimum_occurrences = (
            minimum_occurrences
        )

    def analyze(
        self,
        calls: list[LLMCall],
    ) -> list[Finding]:

        fingerprints: dict[
            str,
            list[LLMCall],
        ] = defaultdict(list)

        for call in calls:

            fingerprint = (
                call.system_prompt_fingerprint
            )

            if fingerprint:
                fingerprints[
                    fingerprint
                ].append(call)

        findings: list[Finding] = []

        for (
            fingerprint,
            matching_calls,
        ) in fingerprints.items():

            count = len(matching_calls)

            if count < self.minimum_occurrences:
                continue

            total_input_tokens = sum(
                call.usage.input_tokens
                for call in matching_calls
            )

            findings.append(
                Finding(
                    rule_id=self.rule_id,
                    title=self.title,
                    severity=Severity.LOW,
                    confidence=(
                        Confidence.DETERMINISTIC
                    ),
                    message=(
                        "The same system-context "
                        f"fingerprint appeared in "
                        f"{count} LLM calls."
                    ),
                    recommendation=(
                        "Check whether provider prompt "
                        "caching or application-level "
                        "context reuse could reduce "
                        "repeated processing."
                    ),
                    evidence={
                        "occurrences": count,
                        "fingerprint": (
                            fingerprint[:12]
                        ),
                        "combined_input_tokens": (
                            total_input_tokens
                        ),
                    },
                )
            )

        return findings