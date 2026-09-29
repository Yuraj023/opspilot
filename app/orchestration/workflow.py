from app.core.exceptions import InvalidStateTransition
from app.orchestration.state import RunState


VALID_TRANSITIONS = {
    RunState.RECEIVED: {
        RunState.TRIAGING,
        RunState.FAILED,
    },
    RunState.TRIAGING: {
        RunState.INVESTIGATING,
        RunState.FAILED,
    },
    RunState.INVESTIGATING: {
        RunState.RCA_READY,
        RunState.FAILED,
    },
    RunState.RCA_READY: {
        RunState.PLAN_READY,
        RunState.FAILED,
    },
    RunState.PLAN_READY: {
        RunState.AWAITING_APPROVAL,
        RunState.EXECUTING,
        RunState.FAILED,
    },
    RunState.AWAITING_APPROVAL: {
        RunState.EXECUTING,
        RunState.HUMAN_REVIEW,
        RunState.FAILED,
    },
    RunState.EXECUTING: {
        RunState.VERIFYING,
        RunState.FAILED,
    },
    RunState.VERIFYING: {
        RunState.RESOLVED,
        RunState.HUMAN_REVIEW,
        RunState.FAILED,
    },
    RunState.HUMAN_REVIEW: {
        RunState.EXECUTING,
        RunState.RESOLVED,
        RunState.FAILED,
    },
    RunState.RESOLVED: set(),
    RunState.FAILED: set(),
}


def transition(current: str, target: str) -> str:
    current_state = RunState(current)
    target_state = RunState(target)

    allowed = VALID_TRANSITIONS.get(current_state, set())

    if target_state not in allowed:
        raise InvalidStateTransition(
            f"Invalid transition: {current_state} -> {target_state}"
        )

    return target_state.value