import json
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="Evaluations | OpsPilot",
    page_icon="📊",
    layout="wide",
)


st.title("Agent Evaluations")

st.caption(
    "Measure OpsPilot's investigation and remediation performance."
)


PROJECT_ROOT = Path(
    __file__
).resolve().parents[2]

REPORT_DIR = (
    PROJECT_ROOT
    / "evals"
    / "reports"
)


# ---------------------------------------------------------
# Find latest report
# ---------------------------------------------------------

reports = sorted(
    REPORT_DIR.glob("*.json"),
    key=lambda path: path.stat().st_mtime,
    reverse=True,
)


if not reports:

    st.info(
        """
        No evaluation reports exist yet.

        Evaluation reports will appear here after the
        OpsPilot evaluation benchmark is implemented.
        """
    )

    st.subheader(
        "Planned Evaluation Metrics"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Root Cause Accuracy",
            "N/A",
        )

    with col2:
        st.metric(
            "Tool Selection Accuracy",
            "N/A",
        )

    with col3:
        st.metric(
            "Remediation Success",
            "N/A",
        )

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric(
            "Unsafe Action Rate",
            "N/A",
        )

    with col5:
        st.metric(
            "Avg Latency",
            "N/A",
        )

    with col6:
        st.metric(
            "Avg Token Usage",
            "N/A",
        )

else:

    latest_report = reports[0]

    st.success(
        f"Loaded: {latest_report.name}"
    )

    try:

        with latest_report.open(
            "r",
            encoding="utf-8",
        ) as file:
            report = json.load(file)

        metrics = report.get(
            "metrics",
            {},
        )

        st.subheader(
            "Evaluation Metrics"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Root Cause Accuracy",
                f"{metrics.get(
                    'root_cause_accuracy',
                    0
                ):.1%}",
            )

        with col2:
            st.metric(
                "Tool Selection Accuracy",
                f"{metrics.get(
                    'tool_selection_accuracy',
                    0
                ):.1%}",
            )

        with col3:
            st.metric(
                "Remediation Success",
                f"{metrics.get(
                    'remediation_success_rate',
                    0
                ):.1%}",
            )

        col4, col5, col6 = st.columns(3)

        with col4:
            st.metric(
                "Unsafe Action Rate",
                f"{metrics.get(
                    'unsafe_action_rate',
                    0
                ):.1%}",
            )

        with col5:
            st.metric(
                "Average Latency",
                f"{metrics.get(
                    'average_latency_ms',
                    0
                ):,.0f} ms",
            )

        with col6:
            st.metric(
                "Average Tokens",
                f"{metrics.get(
                    'average_tokens',
                    0
                ):,.0f}",
            )

        st.divider()

        st.subheader(
            "Raw Evaluation Report"
        )

        st.json(report)

    except (
        OSError,
        json.JSONDecodeError,
    ) as exc:

        st.error(
            f"Could not read evaluation report: {exc}"
        )