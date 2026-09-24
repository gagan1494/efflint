from efflint.rules.unused_tools import (
    UnusedToolsRule,
)
from efflint.schema.trace import (
    LLMCall,
    ToolCall,
    ToolDefinition,
)


def test_unused_tools_detected():

    call = LLMCall(
        trace_id="trace-1",
        span_id="1",
        tools=[
            ToolDefinition(
                name="search",
                token_count=100,
            ),
            ToolDefinition(
                name="weather",
                token_count=200,
            ),
        ],
        tool_calls=[
            ToolCall(
                name="search"
            )
        ],
    )

    findings = UnusedToolsRule().analyze(
        [call]
    )

    assert len(findings) == 1

    assert findings[0].evidence[
        "unused_tools"
    ] == ["weather"]

    assert findings[0].evidence[
        "unused_schema_tokens"
    ] == 200