from datetime import datetime

from pydantic import BaseModel, Field


class EvidenceItem(BaseModel):
    source: str
    finding: str


class InvestigationResult(BaseModel):
    summary: str
    signals: list[str]
    evidence: list[EvidenceItem]
    affected_components: list[str]
    suspected_issue: str


class RCAResult(BaseModel):
    root_cause: str
    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )
    reasoning: str
    supporting_evidence: list[str]
    alternative_hypotheses: list[str]
    affected_component: str


class AgentStepResponse(BaseModel):
    id: str
    run_id: str
    step_number: int
    phase: str
    action: str
    status: str
    input_json: dict | None = None
    output_json: dict | None = None
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class AgentRunResponse(BaseModel):
    id: str
    incident_id: str
    state: str
    root_cause: str | None = None
    confidence: float | None = None
    recommendation: str | None = None
    risk_level: str | None = None
    created_at: datetime
    updated_at: datetime

    steps: list[AgentStepResponse] = []