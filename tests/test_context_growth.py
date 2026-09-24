from efflint.rules.context_growth import (
    ContextGrowthRule,
)
from efflint.schema.trace import (
    LLMCall,
    TokenUsage,
)


def test_context_growth_detected():

    calls = [
        LLMCall(
            trace_id="trace-1",
            span_id="1",
            usage=TokenUsage(
                input_tokens=100
            ),
        ),
        LLMCall(
            trace_id="trace-1",
            span_id="2",
            usage=TokenUsage(
                input_tokens=200
            ),
        ),
        LLMCall(
            trace_id="trace-1",
            span_id="3",
            usage=TokenUsage(
                input_tokens=400
            ),
        ),
    ]

    findings = ContextGrowthRule().analyze(
        calls
    )

    assert len(findings) == 1
    assert findings[0].rule_id == "EFF001"
    assert (
        findings[0].evidence["growth_ratio"]
        == 4.0
    )