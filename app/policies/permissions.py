from enum import StrEnum


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKED = "blocked"


class Permission(StrEnum):
    READ = "read"
    SAFE_WRITE = "safe_write"
    HIGH_RISK = "high_risk"
    BLOCKED = "blocked"


ACTION_PERMISSIONS = {
    "search_logs": Permission.READ,
    "get_metrics": Permission.READ,
    "get_deployment_history": Permission.READ,
    "inspect_code": Permission.READ,
    "search_runbook": Permission.READ,

    "no_action": Permission.READ,

    "create_patch": Permission.SAFE_WRITE,
    "create_incident": Permission.SAFE_WRITE,

    "disable_feature": Permission.HIGH_RISK,
    "restart_service": Permission.HIGH_RISK,
    "rollback": Permission.HIGH_RISK,

    "delete_resource": Permission.BLOCKED,
}