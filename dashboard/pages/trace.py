import os

import requests
import streamlit as st

from dashboard.components.trace_viewer import (
    render_trace,
)


API_BASE_URL = os.getenv(
    "OPSPILOT_API_URL",
    "http://127.0.0.1:8000/api/v1",
)


st.set_page_config(
    page_title="Agent Trace | OpsPilot",
    page_icon="🔎",
    layout="wide",
)


st.title("Agent Trace")

st.caption(
    "Inspect the reasoning workflow and recorded agent steps."
)


run_id = st.text_input(
    "Run ID",
    value=st.session_state.get(
        "current_run",
        {}
    ).get("id", ""),
)


if st.button(
    "Load Trace",
    use_container_width=True,
):

    if not run_id:
        st.warning(
            "Enter a run ID."
        )

    else:

        try:
            response = requests.get(
                f"{API_BASE_URL}/runs/"
                f"{run_id}",
                timeout=30,
            )

            response.raise_for_status()

            run = response.json()

            st.session_state[
                "trace_run"
            ] = run

        except requests.RequestException as exc:
            st.error(
                f"Could not load run: {exc}"
            )


run = st.session_state.get(
    "trace_run"
)


if run:

    st.divider()

    # -----------------------------------------------------
    # Run metadata
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "State",
            run.get(
                "state",
                "UNKNOWN",
            ),
        )

    with col2:
        confidence = run.get(
            "confidence"
        )

        if confidence is not None:
            st.metric(
                "RCA Confidence",
                f"{confidence:.0%}",
            )
        else:
            st.metric(
                "RCA Confidence",
                "N/A",
            )

    with col3:
        st.metric(
            "Recommendation",
            run.get(
                "recommendation",
                "N/A",
            ),
        )

    with col4:
        st.metric(
            "Risk",
            run.get(
                "risk_level",
                "N/A",
            ),
        )

    st.divider()

    # -----------------------------------------------------
    # Root cause
    # -----------------------------------------------------

    st.subheader("Root Cause")

    st.info(
        run.get(
            "root_cause",
            "Root cause not available.",
        )
    )

    st.divider()

    # -----------------------------------------------------
    # Agent trace
    # -----------------------------------------------------

    render_trace(
        run.get(
            "steps",
            [],
        )
    )