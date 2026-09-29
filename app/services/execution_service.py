from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.repositories import create_execution
from app.policies.engine import evaluate_action


def execute_remediation(
    db: Session,
    run,
    action: str,
):
    """
    Phase-1 execution layer.

    Nothing here touches a real server.
    The future simulator/MCP deployment layer will replace this.
    """

    policy = evaluate_action(action)

    if policy.requires_approval:
        # Approval has already been handled by approval_service.
        pass

    result = {
        "success": True,
        "simulation": True,
        "action": action,
        "message": _simulation_message(action),
        "executed_at": datetime.now(timezone.utc).isoformat(),
    }

    execution = create_execution(
        db=db,
        run_id=run.id,
        action=action,
        status="completed",
        result=result,
    )

    return execution


def _simulation_message(action: str) -> str:
    messages = {
        "rollback": (
            "Simulated rollback completed successfully."
        ),
        "restart_service": (
            "Simulated service restart completed successfully."
        ),
        "disable_feature": (
            "Simulated feature disable completed successfully."
        ),
        "no_action": (
            "No remediation was executed."
        ),
    }

    return messages.get(
        action,
        "Simulated action completed.",
    )