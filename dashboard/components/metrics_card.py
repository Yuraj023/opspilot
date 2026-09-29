import streamlit as st


def render_metrics_card(metrics: dict):
    st.subheader("Service Metrics")

    p95_latency = metrics.get(
        "p95_latency_ms",
        0,
    )

    error_rate = metrics.get(
        "error_rate_percent",
        0,
    )

    cpu = metrics.get(
        "cpu_percent",
        0,
    )

    memory = metrics.get(
        "memory_percent",
        0,
    )

    db_pool = metrics.get(
        "db_pool_percent",
        0,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "P95 Latency",
            f"{p95_latency} ms",
        )

    with col2:
        st.metric(
            "Error Rate",
            f"{error_rate}%",
        )

    with col3:
        st.metric(
            "CPU",
            f"{cpu}%",
        )

    col4, col5 = st.columns(2)

    with col4:
        st.metric(
            "Memory",
            f"{memory}%",
        )

    with col5:
        st.metric(
            "DB Pool",
            f"{db_pool}%",
        )