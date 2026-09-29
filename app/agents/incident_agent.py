from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel, set_tracing_disabled

from app.agents.investigator import run_investigation
from app.agents.rca import run_rca
from app.agents.remediation import run_remediation
from app.core.config import get_settings


def build_model():
    """
    Create an OpenAI-compatible model client.

    This currently targets OpenRouter by default.
    The project can later be switched to OpenAI or another
    OpenAI-compatible provider through environment variables.
    """

    settings = get_settings()

    if not settings.openrouter_api_key:
        return None

    if settings.disable_sdk_tracing:
        set_tracing_disabled(True)

    client = AsyncOpenAI(
        api_key=settings.openrouter_api_key,
        base_url=settings.llm_base_url,
    )

    return OpenAIChatCompletionsModel(
        model=settings.llm_model,
        openai_client=client,
    )


async def run_full_analysis(incident):
    model = build_model()

    incident_context = f"""
Incident ID: {incident.id}
Title: {incident.title}
Description: {incident.description}
Service: {incident.service}
Severity: {incident.severity}
Environment: {incident.environment}
"""

    investigation, investigation_usage = await run_investigation(
        incident_id=incident.id,
        incident_context=incident_context,
        model=model,
    )

    rca, rca_usage = await run_rca(
        incident_context=incident_context,
        investigation=investigation.model_dump(),
        model=model,
    )

    remediation, remediation_usage = await run_remediation(
        incident_context=incident_context,
        rca=rca.model_dump(),
        model=model,
    )

    return {
        "investigation": investigation,
        "rca": rca,
        "remediation": remediation,
        "usage": {
            "investigation": investigation_usage,
            "rca": rca_usage,
            "remediation": remediation_usage,
        },
    }