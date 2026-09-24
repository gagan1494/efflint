from efflint.rules.base import (
    Confidence,
    Finding,
    Rule,
    Severity,
)
from efflint.schema.trace import LLMCall


class CacheEfficiencyRule(Rule):
    rule_id = "EFF005"
    title = "Low cache reuse"

    def __init__(
        self,
        minimum_cache_write_tokens: int = 1000,
        maximum_read_write_ratio: float = 0.25,
    ):
        self.minimum_cache_write_tokens = (
            minimum_cache_write_tokens
        )

        self.maximum_read_write_ratio = (
            maximum_read_write_ratio
        )

    def analyze(
        self,
        calls: list[LLMCall],
    ) -> list[Finding]:

        cache_write_tokens = sum(
            call.usage.cache_write_tokens
            for call in calls
        )

        cache_read_tokens = sum(
            call.usage.cache_read_tokens
            for call in calls
        )

        if (
            cache_write_tokens
            < self.minimum_cache_write_tokens
        ):
            return []

        ratio = (
            cache_read_tokens
            / cache_write_tokens
        )

        if (
            ratio
            > self.maximum_read_write_ratio
        ):
            return []

        return [
            Finding(
                rule_id=self.rule_id,
                title=self.title,
                severity=Severity.MEDIUM,
                confidence=Confidence.EXACT,
                message=(
                    f"{cache_write_tokens:,} cache-write "
                    "tokens produced only "
                    f"{cache_read_tokens:,} cache-read "
                    "tokens."
                ),
                recommendation=(
                    "Inspect whether stable prompt "
                    "prefixes are changing between "
                    "requests or whether cached "
                    "content is reused often enough "
                    "to justify cache creation."
                ),
                evidence={
                    "cache_write_tokens": (
                        cache_write_tokens
                    ),
                    "cache_read_tokens": (
                        cache_read_tokens
                    ),
                    "read_write_ratio": round(
                        ratio,
                        3,
                    ),
                },
            )
        ]