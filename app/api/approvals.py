from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.agent import AgentRunResponse
from app.schemas.approval import (
    ApprovalDecisionRequest,
    ApprovalResponse,
)
from app.services.approval_service import (
    decide_approval,
    get_approval,
)
from app.db.repositories import get_run, get_steps

router = APIRouter(prefix="/approvals", tags=["approvals"])


@router.get(
    "/{approval_id}",
    response_model=ApprovalResponse,
)
def get_approval_by_id(
    approval_id: str,
    db: Session = Depends(get_db),
):
    approval = get_approval(db, approval_id)

    if approval is None:
        raise HTTPException(
            status_code=404,
            detail="Approval request not found.",
        )

    return approval


@router.post(
    "/{approval_id}/decision",
    response_model=AgentRunResponse,
)
async def approve_or_reject(
    approval_id: str,
    payload: ApprovalDecisionRequest,
    db: Session = Depends(get_db),
):
    approval = get_approval(db, approval_id)

    if approval is None:
        raise HTTPException(
            status_code=404,
            detail="Approval request not found.",
        )

    try:
        run = await decide_approval(
            db=db,
            approval=approval,
            decision=payload.decision,
            comment=payload.comment,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    steps = get_steps(db, run.id)

    return {
        **run.__dict__,
        "steps": steps,
    }