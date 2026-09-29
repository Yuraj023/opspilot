from datetime import datetime, timezone


def generate_logs(
    service: str,
    failure_type: str,
) -> list[str]:
    timestamp = datetime.now(
        timezone.utc
    ).isoformat()

    base_logs = [
        (
            f"{timestamp} {service} "
            "INFO request_received"
        ),
        (
            f"{timestamp} {service} "
            "INFO request_processing"
        ),
    ]

    failure_logs = {
        "slow_query": [
            (
                f"{timestamp} {service} "
                "WARN database query took 2380ms"
            ),
            (
                f"{timestamp} {service} "
                "WARN connection pool utilization=98%"
            ),
            (
                f"{timestamp} {service} "
                "ERROR request timeout"
            ),
        ],
        "cpu_saturation": [
            (
                f"{timestamp} {service} "
                "WARN CPU utilization=98%"
            ),
            (
                f"{timestamp} {service} "
                "WARN request latency increased"
            ),
            (
                f"{timestamp} {service} "
                "ERROR request processing timeout"
            ),
        ],
        "memory_leak": [
            (
                f"{timestamp} {service} "
                "WARN memory utilization=96%"
            ),
            (
                f"{timestamp} {service} "
                "WARN garbage collection pressure increased"
            ),
            (
                f"{timestamp} {service} "
                "ERROR request latency threshold exceeded"
            ),
        ],
        "redis_failure": [
            (
                f"{timestamp} {service} "
                "ERROR redis connection refused"
            ),
            (
                f"{timestamp} {service} "
                "WARN cache unavailable"
            ),
            (
                f"{timestamp} {service} "
                "ERROR dependency request failed"
            ),
        ],
        "database_exhaustion": [
            (
                f"{timestamp} {service} "
                "WARN database pool utilization=99%"
            ),
            (
                f"{timestamp} {service} "
                "ERROR database connection timeout"
            ),
            (
                f"{timestamp} {service} "
                "ERROR request timeout"
            ),
        ],
        "bad_deployment": [
            (
                f"{timestamp} {service} "
                "WARN queue depth=1840"
            ),
            (
                f"{timestamp} {service} "
                "WARN worker processing latency=4200ms"
            ),
            (
                f"{timestamp} {service} "
                "ERROR worker processing failed"
            ),
        ],
    }

    return base_logs + failure_logs.get(
        failure_type,
        [],
    )