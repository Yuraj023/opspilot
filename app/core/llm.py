import json
import re
from typing import TypeVar

from agents import Agent, Runner
from pydantic import BaseModel, ValidationError

from app.core.config import get_settings

T = TypeVar("T", bound=BaseModel)


def _extract_json(text: str) -> dict:
    """
    Extract JSON from either plain JSON or a fenced code block.
    """

    cleaned = text.strip()

    fenced = re.search(
        r"```json\s*(.*?)\s*```",
        cleaned,
        flags=re.DOTALL | re.IGNORECASE,
    )

    if fenced:
        cleaned = fenced.group(1).strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError(
            "No JSON object found in agent response."
        )

    return json.loads(
        cleaned[start : end + 1]
    )


async def run_json_agent(
    agent: Agent,
    prompt: str,
    schema: type[T],
    max_turns: int = 6,
):
    """
    Run an agent and validate its response with Pydantic.

    We intentionally validate structured JSON in our application
    layer so the project remains compatible with OpenAI-compatible
    providers whose structured-output support differs.
    """

    settings = get_settings()

    if not settings.openrouter_api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not configured."
        )

    result = await Runner.run(
        agent,
        input=prompt,
        max_turns=max_turns,
    )

    raw_output = str(result.final_output)

    try:
        payload = _extract_json(raw_output)
        parsed = schema.model_validate(payload)
    except (ValueError, json.JSONDecodeError, ValidationError) as exc:
        raise RuntimeError(
            f"Agent returned invalid structured output: {exc}"
        ) from exc

    usage = {
        "requests": getattr(
            result.context_wrapper.usage,
            "requests",
            0,
        ),
        "input_tokens": getattr(
            result.context_wrapper.usage,
            "input_tokens",
            0,
        ),
        "output_tokens": getattr(
            result.context_wrapper.usage,
            "output_tokens",
            0,
        ),
        "total_tokens": getattr(
            result.context_wrapper.usage,
            "total_tokens",
            0,
        ),
    }

    return parsed, usage