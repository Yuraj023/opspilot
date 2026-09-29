from app.policies.rules import (
    PolicyDecision,
    evaluate_policy,
)


def evaluate_action(action: str) -> PolicyDecision:
    decision = evaluate_policy(action)

    if not decision.allowed:
        raise ValueError(
            f"Action '{action}' is not allowed: {decision.reason}"
        )

    return decision