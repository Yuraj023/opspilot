import streamlit as st


def render_incident_card(incident: dict):
    severity = incident.get(
        "severity",
        "unknown",
    ).upper()

    status = incident.get(
        "status",
        "UNKNOWN",
    ).upper()

    st.markdown(
        f"""
        <div style="
            border:1px solid rgba(128,128,128,0.25);
            border-radius:12px;
            padding:18px;
            margin-bottom:15px;
        ">
            <h3>{incident.get("title", "Untitled Incident")}</h3>

            <p>
                <strong>ID:</strong>
                {incident.get("id", "N/A")}
            </p>

            <p>
                <strong>Service:</strong>
                {incident.get("service", "N/A")}
            </p>

            <p>
                <strong>Severity:</strong>
                {severity}
            </p>

            <p>
                <strong>Status:</strong>
                {status}
            </p>

            <p>
                {incident.get("description", "")}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )