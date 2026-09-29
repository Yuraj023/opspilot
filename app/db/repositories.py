from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import (
    AgentRun,
    AgentStep,
    Approval,
    Execution,
    Incident,
)


def create_incident_record(
    db: Session,
    title: str,
    description: str,
    service: str,
    severity: str,
    environment: str,
):
    incident = Incident(
        id=str(uuid4()),
        title=title,
        description=description,
        service=service,
        severity=severity,
        environment=environment,
        status="OPEN",
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident


def get_incident_record(
    db: Session,
    incident_id: str,
):
    return db.get(Incident, incident_id)


def update_incident_record(
    db: Session,
    incident: Incident,
):
    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident


def create_run(
    db: Session,
    incident_id: str,
    state: str,
):
    run = AgentRun(
        id=str(uuid4()),
        incident_id=incident_id,
        state=state,
    )

    db.add(run)
    db.commit()
    db.refresh(run)

    return run


def get_run(
    db: Session,
    run_id: str,
):
    return db.get(AgentRun, run_id)


def update_run(
    db: Session,
    run: AgentRun,
):
    run.updated_at = datetime.now(timezone.utc)

    db.add(run)
    db.commit()
    db.refresh(run)

    return run


def add_step(
    db: Session,
    run_id: str,
    step_number: int,
    phase: str,
    action: str,
    status: str,
    input_json: dict | None = None,
    output_json: dict | None = None,
):
    step = AgentStep(
        id=str(uuid4()),
        run_id=run_id,
        step_number=step_number,
        phase=phase,
        action=action,
        status=status,
        input_json=input_json,
        output_json=output_json,
    )

    db.add(step)
    db.commit()
    db.refresh(step)

    return step


def get_steps(
    db: Session,
    run_id: str,
):
    stmt = (
        select(AgentStep)
        .where(AgentStep.run_id == run_id)
        .order_by(AgentStep.step_number)
    )

    return list(db.scalars(stmt).all())


def create_approval(
    db: Session,
    run_id: str,
    action: str,
    risk_level: str,
    rationale: str,
):
    approval = Approval(
        id=str(uuid4()),
        run_id=run_id,
        action=action,
        risk_level=risk_level,
        rationale=rationale,
        status="pending",
    )

    db.add(approval)
    db.commit()
    db.refresh(approval)

    return approval


def get_approval_record(
    db: Session,
    approval_id: str,
):
    return db.get(Approval, approval_id)


def update_approval_record(
    db: Session,
    approval: Approval,
):
    approval.decided_at = datetime.now(timezone.utc)

    db.add(approval)
    db.commit()
    db.refresh(approval)

    return approval


def create_execution(
    db: Session,
    run_id: str,
    action: str,
    status: str,
    result: dict,
):
    execution = Execution(
        id=str(uuid4()),
        run_id=run_id,
        action=action,
        status=status,
        result=result,
    )

    db.add(execution)
    db.commit()
    db.refresh(execution)

    return execution


def update_execution(
    db: Session,
    execution: Execution,
    verification: dict,
):
    execution.verification = verification

    db.add(execution)
    db.commit()
    db.refresh(execution)

    return execution