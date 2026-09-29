import os

import requests
import streamlit as st

from dashboard.components.incident_card import (
    render_incident_card,
)


API_BASE_URL = os.getenv(
    "OPSPILOT_API_URL",
    "http://127.0.0.1:8000/api/v1",
)


st.set_page_config(
    page_title="Incidents | OpsPilot",
    page_icon="🚨",
    layout="wide",
)


st.title("Incident Center")
st.caption(
    "Create, investigate and inspect OpsPilot incidents."
)


# ---------------------------------------------------------
# Create incident
# ---------------------------------------------------------

st.subheader("Create Incident")

with st.form("incident_form"):

    title = st.text_input(
        "Incident title",
        value="API latency spike",
    )

    description = st.text_area(
        "Description",
        value=(
            "Payments API latency increased "
            "significantly after a recent deployment."
        ),
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        service = st.text_input(
            "Service",
            value="payments-api",
        )

    with col2:
        severity = st.selectbox(
            "Severity",
            [
                "low",
                "medium",
                "high",
                "critical",
            ],
            index=2,
        )

    with col3:
        environment = st.selectbox(
            "Environment",
            [
                "development",
                "staging",
                "production",
            ],
            index=2,
        )

    submitted = st.form_submit_button(
        "Create Incident",
        use_container_width=True,
    )


if submitted:

    payload = {
        "title": title,
        "description": description,
        "service": service,
        "severity": severity,
        "environment": environment,
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/incidents",
            json=payload,
            timeout=30,
        )

        response.raise_for_status()

        incident = response.json()

        st.session_state[
            "current_incident"
        ] = incident

        st.success(
            "Incident created successfully."
        )

    except requests.RequestException as exc:
        st.error(
            f"Could not create incident: {exc}"
        )


# ---------------------------------------------------------
# Current incident
# ---------------------------------------------------------

incident = st.session_state.get(
    "current_incident"
)


if incident:

    st.divider()

    render_incident_card(
        incident
    )

    incident_id = incident["id"]

    if st.button(
        "Start AI Investigation",
        type="primary",
        use_container_width=True,
    ):

        with st.spinner(
            "OpsPilot is investigating the incident..."
        ):

            try:
                response = requests.post(
                    f"{API_BASE_URL}/runs/"
                    f"incident/{incident_id}",
                    timeout=180,
                )

                response.raise_for_status()

                run = response.json()

                st.session_state[
                    "current_run"
                ] = run

                st.success(
                    "Agent investigation completed."
                )

            except requests.RequestException as exc:
                st.error(
                    f"Agent run failed: {exc}"
                )


# ---------------------------------------------------------
# Load existing incident
# ---------------------------------------------------------

st.divider()

st.subheader(
    "Load Existing Incident"
)

existing_incident_id = st.text_input(
    "Incident ID"
)

if st.button(
    "Load Incident",
    use_container_width=True,
):

    if not existing_incident_id.strip():
        st.warning(
            "Enter an incident ID."
        )

    else:

        try:
            response = requests.get(
                f"{API_BASE_URL}/incidents/"
                f"{existing_incident_id}",
                timeout=30,
            )

            response.raise_for_status()

            incident = response.json()

            st.session_state[
                "current_incident"
            ] = incident

            st.success(
                "Incident loaded."
            )

            st.rerun()

        except requests.RequestException as exc:
            st.error(
                f"Could not load incident: {exc}"
            )