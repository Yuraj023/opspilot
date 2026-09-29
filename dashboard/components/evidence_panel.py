import streamlit as st


def render_evidence_panel(
    investigation: dict,
):
    st.subheader("Investigation Evidence")

    summary = investigation.get(
        "summary",
        "No summary available.",
    )

    suspected_issue = investigation.get(
        "suspected_issue",
        "Not identified.",
    )

    st.markdown("### Summary")

    st.write(summary)

    st.markdown("### Suspected Issue")

    st.warning(suspected_issue)

    signals = investigation.get(
        "signals",
        [],
    )

    if signals:
        st.markdown("### Signals")

        for signal in signals:
            st.write(
                f"• {signal}"
            )

    evidence = investigation.get(
        "evidence",
        [],
    )

    if evidence:
        st.markdown("### Evidence")

        for item in evidence:
            source = item.get(
                "source",
                "unknown",
            )

            finding = item.get(
                "finding",
                "",
            )

            with st.expander(
                f"{source.upper()}"
            ):
                st.write(finding)

    components = investigation.get(
        "affected_components",
        [],
    )

    if components:
        st.markdown(
            "### Affected Components"
        )

        st.write(
            ", ".join(components)
        )