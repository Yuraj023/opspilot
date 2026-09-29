from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class ApprovalDecisionRequest(BaseModel):
    decision: Literal[
        "approved",
        "rejected",
    ]

    comment: str | None = None


class ApprovalResponse(BaseModel):
    id: str
    run_id: str
    action: str
    risk_level: str
    status: str
    rationale: str
    comment: str | None = None
    created_at: datetime
    decided_at: datetime | None = None

    model_config = {
        "from_attributes": True,
    }