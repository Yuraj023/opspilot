def generate_metrics(
    service_state,
) -> dict:
    """
    Convert a simulated service state into a standard
    metrics dictionary used by OpsPilot.
    """

    return service_state.metrics()