import json

from agents import Agent

from app.core.llm import run_json_agent
from app.schemas.agent import RCAResult


def create_rca_agent(model=None) -> Agent:
    return Agent(
        name="Root Cause Analysis Agent",
        model=model,
        instructions="""
You are the Root Cause Analysis Agent in OpsPilot.

Your job is to determine the most likely root cause using only supplied evidence.

Rules:
1. Separate observations from conclusions.
2. Identify the strongest causal chain.
3. Consider alternative hypotheses.
4. Do not invent missing evidence.
5. Confidence must reflect evidence quality.
6. Never recommend an action here.

Return ONLY valid JSON:

{
  "root_cause": "specific root cause",
  "confidence": 0.0,
  "reasoning": "concise causal explanation",
  "supporting_evidence": ["evidence 1", "evidence 2"],
  "alternative_hypotheses": ["hypothesis 1"],
  "affected_component": "component"
}

confidence must be between 0 and 1.
""",
    )


async def run_rca(
    incident_context: str,
    investigation: dict,
    model=None,
):
    agent = create_rca_agent(model)

    prompt = f"""
Perform root-cause analysis for this incident.

Incident:
{incident_context}

Investigation:
{json.dumps(investigation, indent=2)}

Determine the most likely root cause from the evidence.
"""

    result, usage = await run_json_agent(
        agent=agent,
        prompt=prompt,
        schema=RCAResult,
        max_turns=4,
    )

    return result, usage