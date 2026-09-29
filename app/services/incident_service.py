from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.repositories import (
    create_incident_record,
    get_incident_record,
    update_incident_record,
)
from app.schemas.incident import IncidentCreate


def create_incident(
    db: Session,
    payload: IncidentCreate,
):
    return create_incident_record(
        db=db,
        title=payload.title,
        description=payload.description,
        service=payload.service,
        severity=payload.severity,
        environment=payload.environment,
    )


def get_incident(
    db: Session,
    incident_id: str,
):
    return get_incident_record(db, incident_id)


def update_incident_status(
    db: Session,
    incident_id: str,
    status: str,
):
    incident = get_incident_record(db, incident_id)

    if incident is None:
        return None

    incident.status = status

    if status == "RESOLVED":
        incident.resolved_at = datetime.now(timezone.utc)

    return update_incident_record(db, incident)


def get_simulated_evidence(incident_id: str) -> dict:
    """
    Temporary deterministic evidence source.

    This will later be replaced by:
      simulator/
      MCP observability tools
      repository tools
      deployment tools
      runbook tools
    """

    return {
        "logs": [
            "2026-09-29T18:00:02Z payments-api INFO request_received",
            "2026-09-29T18:00:03Z payments-api WARN database query took 2380ms",
            "2026-09-29T18:00:04Z payments-api WARN connection pool utilization=98%",
            "2026-09-29T18:00:05Z payments-api ERROR request timeout",
        ],
        "metrics": {
            "p95_latency_ms": 2800,
            "error_rate_percent": 7.2,
            "cpu_percent": 61,
            "memory_percent": 68,
            "db_pool_percent": 98,
        },
        "deployments": [
            {
                "version": "v1.8.2",
                "time": "2026-09-29T17:55:00Z",
                "service": "payments-api",
                "status": "success",
            },
            {
                "version": "v1.8.1",
                "time": "2026-09-27T11:20:00Z",
                "service": "payments-api",
                "status": "success",
            },
        ],
        "code_changes": [
            {
                "commit": "a82e91f",
                "version": "v1.8.2",
                "file": "payments/repository.py",
                "change": "Added unindexed customer-history query.",
            }
        ],
        "runbook": {
            "title": "High API Latency",
            "steps": [
                "Check database latency.",
                "Check connection pool utilization.",
                "Inspect recent deployment.",
                "Rollback if regression is confirmed.",
            ],
            "approval_required": True,
        },
    }