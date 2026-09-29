import json

from agents import Agent

from app.core.llm import run_json_agent
from app.schemas.remediation import RemediationPlan


def create_remediation_agent(model=None) -> Agent:
    return Agent(
        name="Remediation Planning Agent",
        model=model,
        instructions="""
You are the Remediation Planning Agent for OpsPilot.

Your job is to propose a controlled remediation based on an incident and root-cause analysis.

Available action types:

- rollback
- restart_service
- disable_feature
- no_action

Rules:
1. Never invent infrastructure capabilities.
2. Prefer the smallest reversible action.
3. Never propose destructive actions.
4. Explicitly state why the action should work.
5. Estimate risk as low, medium or high.
6. High-risk actions require human approval.

Return ONLY valid JSON:

{
  "action": "rollback",
  "target": "deployment",
  "parameters": {},
  "reason": "why this should solve the issue",
  "risk_level": "high",
  "rollback_possible": true
}
""",
    )


async def run_remediation(
    incident_context: str,
    rca: dict,
    model=None,
):
    agent = create_remediation_agent(model)

    prompt = f"""
Create a remediation plan for this incident.

Incident:
{incident_context}

Root cause analysis:
{json.dumps(rca, indent=2)}

Return the safest practical remediation.
"""

    result, usage = await run_json_agent(
        agent=agent,
        prompt=prompt,
        schema=RemediationPlan,
        max_turns=4,
    )

    return result, usage