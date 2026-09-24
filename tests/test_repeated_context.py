from efflint.rules.repeated_context import (
    RepeatedContextRule,
)
from efflint.schema.trace import LLMCall


def test_repeated_context_detected():

    calls = [
        LLMCall(
            trace_id=f"trace-{i}",
            span_id=str(i),
            system_prompt_fingerprint="abc123",
        )
        for i in range(4)
    ]

    findings = (
        RepeatedContextRule().analyze(calls)
    )

    assert len(findings) == 1
    assert findings[0].rule_id == "EFF002"
    assert (
        findings[0].evidence["occurrences"]
        == 4
    )