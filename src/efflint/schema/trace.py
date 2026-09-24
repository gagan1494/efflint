from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class TokenUsage(BaseModel):
    input_tokens: int = Field(default=0, ge=0)
    output_tokens: int = Field(default=0, ge=0)
    cache_read_tokens: int = Field(default=0, ge=0)
    cache_write_tokens: int = Field(default=0, ge=0)
    reasoning_tokens: int = Field(default=0, ge=0)

    @property
    def total_tokens(self) -> int:
        """
        Total newly processed/generated tokens.

        Cache reads are intentionally excluded because they represent
        reused input rather than newly processed input.
        """
        return (
            self.input_tokens
            + self.output_tokens
            + self.cache_write_tokens
            + self.reasoning_tokens
        )


class ToolDefinition(BaseModel):
    name: str

    token_count: int | None = Field(
        default=None,
        ge=0,
    )

    fingerprint: str | None = None


class ToolCall(BaseModel):
    name: str

    arguments_fingerprint: str | None = None
    result_fingerprint: str | None = None

    result_tokens: int | None = Field(
        default=None,
        ge=0,
    )

    success: bool | None = None


class LLMCall(BaseModel):
    trace_id: str
    span_id: str

    timestamp: datetime | None = None

    provider: str | None = None
    model: str | None = None

    usage: TokenUsage = Field(
        default_factory=TokenUsage
    )

    latency_ms: float | None = Field(
        default=None,
        ge=0,
    )

    prompt_fingerprint: str | None = None
    system_prompt_fingerprint: str | None = None

    tools: list[ToolDefinition] = Field(
        default_factory=list
    )

    tool_calls: list[ToolCall] = Field(
        default_factory=list
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )