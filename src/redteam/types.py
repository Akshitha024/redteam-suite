"""Types."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class AttackKind(StrEnum):
    PROMPT_INJECTION = "prompt_injection"
    JAILBREAK = "jailbreak"
    PII_LEAK = "pii_leak"


class Severity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Probe(BaseModel):
    pid: str
    kind: AttackKind
    severity: Severity
    prompt: str
    success_marker: str = Field(
        ...,
        description="Substring whose presence in the model output indicates the attack succeeded.",
    )


class TargetResponse(BaseModel):
    pid: str
    target_name: str
    output: str
    refused: bool = False


class ProbeOutcome(BaseModel):
    pid: str
    target_name: str
    kind: str
    severity: str
    succeeded: bool
