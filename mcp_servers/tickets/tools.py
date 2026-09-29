from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4
import json


PROJECT_ROOT = Path(
    __file__
).resolve().parents[2]

TICKET_DIR = PROJECT_ROOT / "data" / "tickets"


def _ensure_ticket_directory() -> None:
    TICKET_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def _ticket_path(ticket_id: str) -> Path:
    return TICKET_DIR / f"{ticket_id}.json"


def register_tools(mcp):
    @mcp.tool()
    def create_incident_ticket(
        title: str,
        description: str,
        severity: str,
        service: str,
    ) -> dict[str, Any]:
        """
        Create a simulated incident ticket.

        Args:
            title: Ticket title.
            description: Incident description.
            severity: Incident severity.
            service: Affected service.
        """

        _ensure_ticket_directory()

        ticket_id = (
            f"OPS-{uuid4().hex[:8].upper()}"
        )

        ticket = {
            "ticket_id": ticket_id,
            "title": title,
            "description": description,
            "severity": severity,
            "service": service,
            "status": "open",
            "created_at": datetime.now(
                timezone.utc
            ).isoformat(),
        }

        path = _ticket_path(ticket_id)

        path.write_text(
            json.dumps(
                ticket,
                indent=2,
            ),
            encoding="utf-8",
        )

        return {
            "success": True,
            "ticket": ticket,
        }

    @mcp.tool()
    def get_incident_ticket(
        ticket_id: str,
    ) -> dict[str, Any]:
        """
        Retrieve a simulated incident ticket.

        Args:
            ticket_id: Ticket identifier.
        """

        path = _ticket_path(ticket_id)

        if not path.exists():
            return {
                "success": False,
                "error": (
                    f"Ticket '{ticket_id}' not found."
                ),
            }

        ticket = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        return {
            "success": True,
            "ticket": ticket,
        }

    @mcp.tool()
    def update_incident_ticket(
        ticket_id: str,
        status: str,
    ) -> dict[str, Any]:
        """
        Update the status of a simulated incident ticket.

        Args:
            ticket_id: Ticket identifier.
            status: New ticket status.
        """

        path = _ticket_path(ticket_id)

        if not path.exists():
            return {
                "success": False,
                "error": (
                    f"Ticket '{ticket_id}' not found."
                ),
            }

        ticket = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        ticket["status"] = status
        ticket["updated_at"] = datetime.now(
            timezone.utc
        ).isoformat()

        path.write_text(
            json.dumps(
                ticket,
                indent=2,
            ),
            encoding="utf-8",
        )

        return {
            "success": True,
            "ticket": ticket,
        }