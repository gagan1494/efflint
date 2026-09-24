from efflint.rules.base import (
    Confidence,
    Finding,
    Rule,
    Severity,
)
from efflint.schema.trace import LLMCall


class UnusedToolsRule(Rule):
    rule_id = "EFF003"
    title = "Unused tools detected"

    def analyze(
        self,
        calls: list[LLMCall],
    ) -> list[Finding]:

        registered: set[str] = set()
        invoked: set[str] = set()

        tool_token_counts: dict[str, int] = {}

        for call in calls:

            for tool in call.tools:
                registered.add(tool.name)

                if tool.token_count is not None:
                    tool_token_counts[
                        tool.name
                    ] = tool.token_count

            for tool_call in call.tool_calls:
                invoked.add(tool_call.name)

        unused = registered - invoked

        if not unused:
            return []

        unused_schema_tokens = sum(
            tool_token_counts.get(
                tool_name,
                0,
            )
            for tool_name in unused
        )

        return [
            Finding(
                rule_id=self.rule_id,
                title=self.title,
                severity=Severity.MEDIUM,
                confidence=(
                    Confidence.DETERMINISTIC
                ),
                message=(
                    f"{len(unused)} of "
                    f"{len(registered)} registered "
                    "tools were never invoked in "
                    "the analyzed workload."
                ),
                recommendation=(
                    "Consider exposing tools "
                    "dynamically based on task "
                    "requirements rather than "
                    "including every tool in every "
                    "request."
                ),
                evidence={
                    "registered_tools": (
                        len(registered)
                    ),
                    "invoked_tools": len(invoked),
                    "unused_tools": sorted(unused),
                    "unused_schema_tokens": (
                        unused_schema_tokens
                    ),
                },
            )
        ]