from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from efflint.schema.trace import LLMCall


class Confidence(str, Enum):
    EXACT = "exact"
    DETERMINISTIC = "deterministic"
    HEURISTIC = "heuristic"
    REPLAY_REQUIRED = "replay_required"


class Severity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Finding(BaseModel):
    rule_id: str
    title: str

    severity: Severity
    confidence: Confidence

    message: str
    recommendation: str

    trace_id: str | None = None

    evidence: dict[str, Any] = Field(
        default_factory=dict
    )


class Rule(ABC):
    rule_id: str
    title: str

    @abstractmethod
    def analyze(
        self,
        calls: list[LLMCall],
    ) -> list[Finding]:
        raise NotImplementedError