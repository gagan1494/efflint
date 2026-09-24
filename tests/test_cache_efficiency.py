from efflint.rules.cache_efficiency import (
    CacheEfficiencyRule,
)
from efflint.schema.trace import (
    LLMCall,
    TokenUsage,
)


def test_low_cache_reuse_detected():

    calls = [
        LLMCall(
            trace_id="trace-1",
            span_id="1",
            usage=TokenUsage(
                cache_write_tokens=1000,
                cache_read_tokens=50,
            ),
        ),
        LLMCall(
            trace_id="trace-1",
            span_id="2",
            usage=TokenUsage(
                cache_write_tokens=1000,
                cache_read_tokens=100,
            ),
        ),
    ]

    findings = (
        CacheEfficiencyRule().analyze(calls)
    )

    assert len(findings) == 1
    assert findings[0].rule_id == "EFF005"