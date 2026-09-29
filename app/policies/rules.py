from dataclasses import dataclass

from app.policies.permissions import (
    ACTION_PERMISSIONS,
    Permission,
    RiskLevel,
)


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    requires_approval: bool
    risk_level: str
    reason: str


def evaluate_policy(action: str) -> PolicyDecision:
    permission = ACTION_PERMISSIONS.get(
        action,
        Permission.BLOCKED,
    )

    if permission == Permission.READ:
        return PolicyDecision(
            allowed=True,
            requires_approval=False,
            risk_level=RiskLevel.LOW.value,
            reason="Read-only action.",
        )

    if permission == Permission.SAFE_WRITE:
        return PolicyDecision(
            allowed=True,
            requires_approval=False,
            risk_level=RiskLevel.MEDIUM.value,
            reason="Low-impact write operation.",
        )

    if permission == Permission.HIGH_RISK:
        return PolicyDecision(
            allowed=True,
            requires_approval=True,
            risk_level=RiskLevel.HIGH.value,
            reason="Production-affecting operation requires human approval.",
        )

    return PolicyDecision(
        allowed=False,
        requires_approval=False,
        risk_level=RiskLevel.BLOCKED.value,
        reason="Action is blocked by policy.",
    )