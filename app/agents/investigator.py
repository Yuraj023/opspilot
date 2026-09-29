import json

from agents import Agent, function_tool

from app.core.llm import run_json_agent
from app.schemas.agent import EvidenceItem
from app.services.incident_service import get_simulated_evidence


class InvestigationResultModel:
    """
    Lightweight schema description used for prompting.
    Actual validation happens in Pydantic schema classes.
    """


@function_tool
def search_logs(incident_id: str, query: str = "") -> str:
    """
    Search application logs for evidence related to an incident.

    Args:
        incident_id: Incident identifier.
        query: Optional keyword to filter log entries.
    """
    evidence = get_simulated_evidence(incident_id)
    logs = evidence["logs"]

    if query:
        filtered = [
            log for log in logs
            if query.lower() in log.lower()
        ]
    else:
        filtered = logs

    return json.dumps(filtered, indent=2)


@function_tool
def get_metrics(incident_id: str) -> str:
    """
    Return system metrics associated with an incident.

    Args:
        incident_id: Incident identifier.
    """
    evidence = get_simulated_evidence(incident_id)
    return json.dumps(evidence["metrics"], indent=2)


@function_tool
def get_deployment_history(incident_id: str) -> str:
    """
    Return recent deployment information.

    Args:
        incident_id: Incident identifier.
    """
    evidence = get_simulated_evidence(incident_id)
    return json.dumps(evidence["deployments"], indent=2)


@function_tool
def inspect_code(incident_id: str) -> str:
    """
    Inspect recent source-code changes associated with an incident.

    Args:
        incident_id: Incident identifier.
    """
    evidence = get_simulated_evidence(incident_id)
    return json.dumps(evidence["code_changes"], indent=2)


@function_tool
def search_runbook(incident_id: str) -> str:
    """
    Retrieve the operational runbook relevant to an incident.

    Args:
        incident_id: Incident identifier.
    """
    evidence = get_simulated_evidence(incident_id)
    return json.dumps(evidence["runbook"], indent=2)


def create_investigator_agent(model=None) -> Agent:
    return Agent(
        name="Investigation Agent",
        model=model,
        instructions="""
You are the Investigation Agent inside OpsPilot.

Your responsibility is to investigate a software incident using tools.

Rules:
1. Use evidence, never assumptions.
2. Call the available investigation tools before making a conclusion.
3. Check logs, metrics, deployment history, code changes and runbooks.
4. Identify correlations and anomalies.
5. Do not propose a destructive action.
6. Do not invent data.

Return ONLY valid JSON in this exact structure:

{
  "summary": "short investigation summary",
  "signals": ["signal 1", "signal 2"],
  "evidence": [
    {
      "source": "logs",
      "finding": "specific finding"
    }
  ],
  "affected_components": ["component"],
  "suspected_issue": "short issue description"
}
""",
        tools=[
            search_logs,
            get_metrics,
            get_deployment_history,
            inspect_code,
            search_runbook,
        ],
    )


async def run_investigation(
    incident_id: str,
    incident_context: str,
    model=None,
):
    agent = create_investigator_agent(model)

    prompt = f"""
Investigate the following incident.

Incident ID: {incident_id}

Incident context:
{incident_context}

You must inspect the available evidence before producing your conclusion.
"""

    from app.schemas.agent import InvestigationResult

    result, usage = await run_json_agent(
        agent=agent,
        prompt=prompt,
        schema=InvestigationResult,
        max_turns=8,
    )

    return result, usage