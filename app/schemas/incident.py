from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class IncidentCreate(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=255,
    )

    description: str = Field(
        min_length=5,
    )

    service: str = Field(
        min_length=2,
        max_length=100,
    )

    severity: Literal[
        "low",
        "medium",
        "high",
        "critical",
    ]

    environment: Literal[
        "development",
        "staging",
        "production",
    ] = "production"


class IncidentResponse(BaseModel):
    id: str
    title: str
    description: str
    service: str
    severity: str
    environment: str
    status: str
    created_at: datetime
    resolved_at: datetime | None = None

    model_config = {
        "from_attributes": True,
    }