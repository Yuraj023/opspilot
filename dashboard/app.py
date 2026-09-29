import os
from datetime import datetime

import requests
import streamlit as st


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

API_BASE_URL = os.getenv(
    "OPSPILOT_API_URL",
    "http://127.0.0.1:8000/api/v1",
)


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="OpsPilot",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# Custom styling
# ---------------------------------------------------------

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .status-card {
            border: 1px solid rgba(128, 128, 128, 0.25);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
        }

        .small-muted {
            color: #888;
            font-size: 0.85rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def check_api() -> bool:
    try:
        response = requests.get(
            f"{API_BASE_URL}/health",
            timeout=3,
        )

        return response.ok

    except requests.RequestException:
        return False


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:
    st.title("OpsPilot")

    st.caption(
        "AI Incident Response Engineer"
    )

    st.divider()

    api_online = check_api()

    if api_online:
        st.success("API Online")
    else:
        st.error("API Offline")

    st.divider()

    st.caption("Backend")

    st.code(
        API_BASE_URL,
        language="text",
    )


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("OpsPilot")
st.subheader(
    "AI-powered software incident investigation and remediation"
)

st.caption(
    f"Last dashboard refresh: "
    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)


# ---------------------------------------------------------
# System overview
# ---------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "System",
        "ONLINE" if api_online else "OFFLINE",
    )

with col2:
    st.metric(
        "Agent Runtime",
        "READY",
    )

with col3:
    st.metric(
        "MCP",
        "READY",
    )

with col4:
    st.metric(
        "Policy Engine",
        "ACTIVE",
    )


st.divider()


# ---------------------------------------------------------
# Quick actions
# ---------------------------------------------------------

st.subheader("Quick Start")

col1, col2 = st.columns(2)

with col1:
    st.info(
        """
        **Create an incident**

        Go to **Incidents** from the sidebar to create a
        simulated production incident and start an AI
        investigation.
        """
    )

with col2:
    st.info(
        """
        **Inspect an agent run**

        Use **Trace** to inspect individual investigation
        steps, tool calls, RCA and remediation planning.
        """
    )


# ---------------------------------------------------------
# Architecture
# ---------------------------------------------------------

st.subheader("System Architecture")

st.code(
    """
User
  │
  ▼
Streamlit Dashboard
  │
  ▼
FastAPI
  │
  ▼
Agent Runtime
  │
  ├── Investigation
  ├── Root Cause Analysis
  ├── Remediation Planning
  ├── Policy Engine
  └── Verification
          │
          ▼
      MCP Tools
    ┌─────┼─────┐
    │     │     │
  Logs  Code  Deployments
    │     │     │
    └─────┼─────┘
          │
          ▼
      PostgreSQL
    """,
    language="text",
)


st.divider()

st.caption(
    "OpsPilot | Agentic AI Incident Response System"
)