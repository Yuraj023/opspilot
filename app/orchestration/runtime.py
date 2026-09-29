from sqlalchemy.orm import Session

from app.agents.incident_agent import (
    build_model,
)
from app.agents.investigator import run_investigation
from app.agents.rca import run_rca
from app.agents.remediation import run_remediation
from app.db.repositories import (
    add_step,
    create_approval,
    create_run,
    get_run,
    update_run,
)
from app.orchestration.state import RunState
from app.orchestration.workflow import transition
from app.policies.engine import evaluate_action
from app.services.incident_service import update_incident_status


async def run_incident_workflow(db: Session, incident):
    run = create_run(
        db=db,
        incident_id=incident.id,
        state=RunState.RECEIVED.value,
    )

    try:
        run.state = transition(
            run.state,
            RunState.TRIAGING.value,
        )
        update_run(db, run)

        model = build_model()

        incident_context = f"""
Incident ID: {incident.id}
Title: {incident.title}
Description: {incident.description}
Service: {incident.service}
Severity: {incident.severity}
Environment: {incident.environment}
"""

        run.state = transition(
            run.state,
            RunState.INVESTIGATING.value,
        )
        update_run(db, run)

        investigation, investigation_usage = await run_investigation(
            incident_id=incident.id,
            incident_context=incident_context,
            model=model,
        )

        add_step(
            db=db,
            run_id=run.id,
            step_number=1,
            phase="investigation",
            action="collect_evidence",
            status="completed",
            output_json={
                "result": investigation.model_dump(),
                "usage": investigation_usage,
            },
        )

        run.state = transition(
            run.state,
            RunState.RCA_READY.value,
        )
        run.root_cause = "Analysis pending"
        update_run(db, run)

        rca, rca_usage = await run_rca(
            incident_context=incident_context,
            investigation=investigation.model_dump(),
            model=model,
        )

        add_step(
            db=db,
            run_id=run.id,
            step_number=2,
            phase="rca",
            action="identify_root_cause",
            status="completed",
            output_json={
                "result": rca.model_dump(),
                "usage": rca_usage,
            },
        )

        run.root_cause = rca.root_cause
        run.confidence = rca.confidence
        update_run(db, run)

        run.state = transition(
            run.state,
            RunState.PLAN_READY.value,
        )
        update_run(db, run)

        remediation, remediation_usage = await run_remediation(
            incident_context=incident_context,
            rca=rca.model_dump(),
            model=model,
        )

        add_step(
            db=db,
            run_id=run.id,
            step_number=3,
            phase="remediation_planning",
            action=remediation.action,
            status="completed",
            output_json={
                "result": remediation.model_dump(),
                "usage": remediation_usage,
            },
        )

        run.recommendation = remediation.action
        run.risk_level = remediation.risk_level
        update_run(db, run)

        policy = evaluate_action(remediation.action)

        if policy.requires_approval:
            run.state = transition(
                run.state,
                RunState.AWAITING_APPROVAL.value,
            )

            update_run(db, run)

            create_approval(
                db=db,
                run_id=run.id,
                action=remediation.action,
                risk_level=policy.risk_level,
                rationale=policy.reason,
            )

        else:
            run.state = transition(
                run.state,
                RunState.EXECUTING.value,
            )
            update_run(db, run)

            update_incident_status(
                db=db,
                incident_id=incident.id,
                status="EXECUTING",
            )

        db.refresh(run)
        return run

    except Exception:
        run.state = RunState.FAILED.value
        update_run(db, run)
        raise