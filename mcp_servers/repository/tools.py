from typing import Any

from app.services.incident_service import get_simulated_evidence


def register_tools(mcp):
    @mcp.tool()
    def inspect_repository(
        incident_id: str,
    ) -> dict[str, Any]:
        """
        Inspect source-code changes related to an incident.

        Args:
            incident_id: Incident identifier.
        """

        evidence = get_simulated_evidence(incident_id)

        return {
            "incident_id": incident_id,
            "repository": {
                "name": "opspilot-simulated-services",
                "branch": "main",
            },
            "code_changes": evidence.get(
                "code_changes",
                [],
            ),
        }

    @mcp.tool()
    def search_code(
        incident_id: str,
        query: str,
    ) -> dict[str, Any]:
        """
        Search simulated source-code changes for a keyword.

        Args:
            incident_id: Incident identifier.
            query: Search keyword.
        """

        evidence = get_simulated_evidence(incident_id)

        changes = evidence.get(
            "code_changes",
            [],
        )

        query_lower = query.lower()

        matches = [
            change
            for change in changes
            if query_lower in str(change).lower()
        ]

        return {
            "incident_id": incident_id,
            "query": query,
            "matches": matches,
        }

    @mcp.tool()
    def get_recent_commits(
        incident_id: str,
        limit: int = 10,
    ) -> dict[str, Any]:
        """
        Return recent commits associated with the incident.

        Args:
            incident_id: Incident identifier.
            limit: Maximum number of commits to return.
        """

        evidence = get_simulated_evidence(incident_id)

        changes = evidence.get(
            "code_changes",
            [],
        )

        commits = []

        for change in changes[:limit]:
            commits.append(
                {
                    "commit": change.get("commit"),
                    "version": change.get("version"),
                    "file": change.get("file"),
                    "change": change.get("change"),
                }
            )

        return {
            "incident_id": incident_id,
            "commits": commits,
        }