from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.incident import IncidentCreate, IncidentResponse
from app.services.incident_service import (
    create_incident,
    get_incident,
)

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.post(
    "",
    response_model=IncidentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_incident(
    payload: IncidentCreate,
    db: Session = Depends(get_db),
):
    return create_incident(db, payload)


@router.get(
    "/{incident_id}",
    response_model=IncidentResponse,
)
def get_incident_by_id(
    incident_id: str,
    db: Session = Depends(get_db),
):
    incident = get_incident(db, incident_id)

    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found.",
        )

    return incident