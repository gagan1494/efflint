from efflint.rules.tool_loops import (
    ToolLoopRule,
)
from efflint.schema.trace import (
    LLMCall,
    ToolCall,
)


def test_tool_loop_detected():

    call = LLMCall(
        trace_id="trace-1",
        span_id="1",
        tool_calls=[
            ToolCall(
                name="search",
                arguments_fingerprint="abc",
            ),
            ToolCall(
                name="search",
                arguments_fingerprint="abc",
            ),
            ToolCall(
                name="search",
                arguments_fingerprint="abc",
            ),
        ],
    )

    findings = ToolLoopRule().analyze(
        [call]
    )

    assert len(findings) == 1
    assert findings[0].rule_id == "EFF004"
    assert (
        findings[0].evidence["repeat_count"]
        == 3
    )