from sqlalchemy.orm import Session

from app.db.repositories import (
    create_approval,
    get_approval_record,
    get_run,
    update_approval_record,
    update_run,
)
from app.orchestration.state import RunState
from app.services.execution_service import execute_remediation
from app.services.verification_service import verify_remediation


def get_approval(db: Session, approval_id: str):
    return get_approval_record(db, approval_id)


def request_approval(
    db: Session,
    run_id: str,
    action: str,
    risk_level: str,
    rationale: str,
):
    return create_approval(
        db=db,
        run_id=run_id,
        action=action,
        risk_level=risk_level,
        rationale=rationale,
    )


async def decide_approval(
    db: Session,
    approval,
    decision: str,
    comment: str | None = None,
):
    if approval.status != "pending":
        raise ValueError(
            f"Approval is already {approval.status}."
        )

    run = get_run(db, approval.run_id)

    if run is None:
        raise ValueError("Associated agent run not found.")

    approval.status = decision
    approval.comment = comment

    update_approval_record(db, approval)

    if decision == "rejected":
        run.state = RunState.HUMAN_REVIEW.value
        update_run(db, run)
        return run

    if decision != "approved":
        raise ValueError(
            "Decision must be 'approved' or 'rejected'."
        )

    run.state = RunState.EXECUTING.value
    update_run(db, run)

    execution = execute_remediation(
        db=db,
        run=run,
        action=approval.action,
    )

    run.state = RunState.VERIFYING.value
    update_run(db, run)

    verification = verify_remediation(
        db=db,
        run=run,
        execution=execution,
    )

    if verification.verified:
        run.state = RunState.RESOLVED.value
    else:
        run.state = RunState.HUMAN_REVIEW.value

    update_run(db, run)

    return run