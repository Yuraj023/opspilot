import streamlit as st


def render_trace(
    steps: list[dict],
):
    st.subheader("Agent Trace")

    if not steps:
        st.info(
            "No trace steps available."
        )
        return

    for step in steps:
        step_number = step.get(
            "step_number",
            "?",
        )

        phase = step.get(
            "phase",
            "unknown",
        )

        action = step.get(
            "action",
            "unknown",
        )

        status = step.get(
            "status",
            "unknown",
        )

        created_at = step.get(
            "created_at",
            "",
        )

        with st.expander(
            f"Step {step_number} — "
            f"{phase.upper()} — "
            f"{status.upper()}"
        ):
            st.write(
                f"**Action:** {action}"
            )

            if created_at:
                st.caption(
                    f"Time: {created_at}"
                )

            output = step.get(
                "output_json"
            )

            if output:
                st.json(output)

            input_data = step.get(
                "input_json"
            )

            if input_data:
                with st.expander(
                    "Input"
                ):
                    st.json(input_data)