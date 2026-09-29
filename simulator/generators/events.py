from datetime import datetime, timezone


def generate_deployment_events(
    current_version: str,
    previous_version: str,
) -> list[dict]:
    now = datetime.now(
        timezone.utc
    ).isoformat()

    return [
        {
            "event": "deployment",
            "version": current_version,
            "status": "success",
            "timestamp": now,
        },
        {
            "event": "deployment",
            "version": previous_version,
            "status": "success",
            "timestamp": now,
        },
    ]


def generate_code_change_event(
    version: str,
    failure_type: str,
) -> dict:
    changes = {
        "slow_query": (
            "Added unindexed customer-history query."
        ),
        "cpu_saturation": (
            "Introduced new authentication "
            "processing path."
        ),
        "memory_leak": (
            "Added in-memory request cache."
        ),
        "redis_failure": (
            "Changed cache connection handling."
        ),
        "database_exhaustion": (
            "Changed database session lifecycle."
        ),
        "bad_deployment": (
            "Changed worker processing loop."
        ),
    }

    return {
        "commit": "simulated-commit-001",
        "version": version,
        "file": "simulated/service.py",
        "change": changes.get(
            failure_type,
            "Unknown change.",
        ),
    }