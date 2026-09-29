from app.agents.verifier import verify_execution
from app.services.incident_service import update_incident_status
from app.db.repositories import update_execution


def verify_remediation(
    db,
    run,
    execution,
):
    verification = verify_execution(
        action=execution.action,
        execution_result=execution.result,
    )

    update_execution(
        db=db,
        execution=execution,
        verification=verification.model_dump(),
    )

    if verification.verified:
        update_incident_status(
            db=db,
            incident_id=run.incident_id,
            status="RESOLVED",
        )

    return verification