from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.agent import AgentRunResponse
from app.services.incident_service import get_incident
from app.orchestration.runtime import run_incident_workflow
from app.db.repositories import get_run, get_steps

router = APIRouter(prefix="/runs", tags=["runs"])


@router.post(
    "/incident/{incident_id}",
    response_model=AgentRunResponse,
    status_code=status.HTTP_201_CREATED,
)
async def start_incident_run(
    incident_id: str,
    db: Session = Depends(get_db),
):
    incident = get_incident(db, incident_id)

    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found.",
        )

    try:
        run = await run_incident_workflow(db, incident)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Incident workflow failed: {exc}",
        ) from exc

    steps = get_steps(db, run.id)

    return {
        **run.__dict__,
        "steps": steps,
    }


@router.get(
    "/{run_id}",
    response_model=AgentRunResponse,
)
def get_run_by_id(
    run_id: str,
    db: Session = Depends(get_db),
):
    run = get_run(db, run_id)

    if run is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent run not found.",
        )

    steps = get_steps(db, run.id)

    return {
        **run.__dict__,
        "steps": steps,
    }