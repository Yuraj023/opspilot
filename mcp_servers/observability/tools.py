import json
from typing import Any

from app.services.incident_service import get_simulated_evidence


def register_tools(mcp):
    @mcp.tool()
    def search_logs(
        incident_id: str,
        query: str = "",
        limit: int = 20,
    ) -> dict[str, Any]:
        """
        Search application logs associated with an incident.

        Args:
            incident_id: Incident identifier.
            query: Optional keyword to search for.
            limit: Maximum number of log entries to return.
        """

        evidence = get_simulated_evidence(incident_id)

        logs = evidence.get("logs", [])

        if query:
            query_lower = query.lower()

            logs = [
                log
                for log in logs
                if query_lower in log.lower()
            ]

        logs = logs[:max(1, min(limit, 100))]

        return {
            "incident_id": incident_id,
            "query": query,
            "count": len(logs),
            "logs": logs,
        }

    @mcp.tool()
    def get_metrics(
        incident_id: str,
    ) -> dict[str, Any]:
        """
        Return current service metrics for an incident.

        Args:
            incident_id: Incident identifier.
        """

        evidence = get_simulated_evidence(incident_id)

        return {
            "incident_id": incident_id,
            "metrics": evidence.get("metrics", {}),
        }

    @mcp.tool()
    def get_service_health(
        incident_id: str,
    ) -> dict[str, Any]:
        """
        Calculate a simple service-health summary from available metrics.

        Args:
            incident_id: Incident identifier.
        """

        evidence = get_simulated_evidence(incident_id)

        metrics = evidence.get("metrics", {})

        p95_latency = metrics.get("p95_latency_ms", 0)
        error_rate = metrics.get("error_rate_percent", 0)
        db_pool = metrics.get("db_pool_percent", 0)

        unhealthy_signals = []

        if p95_latency > 1000:
            unhealthy_signals.append(
                "High request latency"
            )

        if error_rate > 5:
            unhealthy_signals.append(
                "High error rate"
            )

        if db_pool > 90:
            unhealthy_signals.append(
                "Database connection pool near exhaustion"
            )

        status = (
            "unhealthy"
            if unhealthy_signals
            else "healthy"
        )

        return {
            "incident_id": incident_id,
            "status": status,
            "signals": unhealthy_signals,
            "metrics": metrics,
        }

    @mcp.tool()
    def get_alert_summary(
        incident_id: str,
    ) -> dict[str, Any]:
        """
        Return a summary of alerts associated with an incident.

        Args:
            incident_id: Incident identifier.
        """

        evidence = get_simulated_evidence(incident_id)

        metrics = evidence.get("metrics", {})

        alerts = []

        if metrics.get("p95_latency_ms", 0) > 1000:
            alerts.append(
                {
                    "name": "high_latency",
                    "severity": "high",
                    "value": metrics.get(
                        "p95_latency_ms"
                    ),
                    "threshold": 1000,
                }
            )

        if metrics.get("error_rate_percent", 0) > 5:
            alerts.append(
                {
                    "name": "high_error_rate",
                    "severity": "high",
                    "value": metrics.get(
                        "error_rate_percent"
                    ),
                    "threshold": 5,
                }
            )

        return {
            "incident_id": incident_id,
            "alert_count": len(alerts),
            "alerts": alerts,
        }