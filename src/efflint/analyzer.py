from pydantic import BaseModel, Field

from efflint.rules import (
    CacheEfficiencyRule,
    ContextGrowthRule,
    RepeatedContextRule,
    ToolLoopRule,
    UnusedToolsRule,
)
from efflint.rules.base import Finding, Rule
from efflint.schema.trace import LLMCall


class AnalysisReport(BaseModel):
    calls_analyzed: int

    input_tokens: int
    output_tokens: int

    cache_read_tokens: int
    cache_write_tokens: int

    reasoning_tokens: int

    findings: list[Finding] = Field(
        default_factory=list
    )


class Analyzer:

    def __init__(
        self,
        rules: list[Rule] | None = None,
    ):
        self.rules = rules or [
            ContextGrowthRule(),
            RepeatedContextRule(),
            UnusedToolsRule(),
            ToolLoopRule(),
            CacheEfficiencyRule(),
        ]

    def run(
        self,
        calls: list[LLMCall],
    ) -> AnalysisReport:

        findings: list[Finding] = []

        for rule in self.rules:
            findings.extend(
                rule.analyze(calls)
            )

        return AnalysisReport(
            calls_analyzed=len(calls),
            input_tokens=sum(
                call.usage.input_tokens
                for call in calls
            ),
            output_tokens=sum(
                call.usage.output_tokens
                for call in calls
            ),
            cache_read_tokens=sum(
                call.usage.cache_read_tokens
                for call in calls
            ),
            cache_write_tokens=sum(
                call.usage.cache_write_tokens
                for call in calls
            ),
            reasoning_tokens=sum(
                call.usage.reasoning_tokens
                for call in calls
            ),
            findings=findings,
        )