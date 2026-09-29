from typing import Literal

from pydantic import BaseModel, Field


class RemediationPlan(BaseModel):
    action: Literal[
        "rollback",
        "restart_service",
        "disable_feature",
        "no_action",
    ]

    target: str

    parameters: dict = Field(
        default_factory=dict,
    )

    reason: str

    risk_level: Literal[
        "low",
        "medium",
        "high",
    ]

    rollback_possible: bool


class VerificationResult(BaseModel):
    verified: bool
    status: Literal[
        "healthy",
        "unhealthy",
    ]

    checks: list[str]

    summary: str