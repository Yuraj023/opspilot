import os

import requests
import streamlit as st

from dashboard.components.approval_panel import (
    render_approval_panel,
)


API_BASE_URL = os.getenv(
    "OPSPILOT_API_URL",
    "http://127.0.0.1:8000/api/v1",
)


st.set_page_config(
    page_title="Approvals | OpsPilot",
    page_icon="✅",
    layout="wide",
)


st.title("Human Approvals")

st.caption(
    "Review and authorize high-risk remediation actions."
)


approval_id = st.text_input(
    "Approval ID"
)


if st.button(
    "Load Approval",
    use_container_width=True,
):

    if not approval_id.strip():
        st.warning(
            "Enter an approval ID."
        )

    else:

        try:
            response = requests.get(
                f"{API_BASE_URL}/approvals/"
                f"{approval_id}",
                timeout=30,
            )

            response.raise_for_status()

            approval = response.json()

            st.session_state[
                "current_approval"
            ] = approval

        except requests.RequestException as exc:
            st.error(
                f"Could not load approval: {exc}"
            )


approval = st.session_state.get(
    "current_approval"
)


if approval:

    st.divider()

    render_approval_panel(
        approval=approval,
        api_base_url=API_BASE_URL,
    )