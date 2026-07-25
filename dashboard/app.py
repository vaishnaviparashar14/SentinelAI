import streamlit as st
import pandas as pd

from charts import (
    attack_distribution,
    prediction_distribution,
    risk_distribution
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="SentinelAI",
    page_icon="🛡️",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

df = pd.read_csv("data/processed/predictions.csv")

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("🛡 SentinelAI")
st.sidebar.markdown("---")

attack_types = ["All"] + sorted(df["label"].unique().tolist())

selected_attack = st.sidebar.selectbox(
    "Attack Type",
    attack_types
)

prediction_types = ["All"] + sorted(df["prediction"].unique().tolist())

selected_prediction = st.sidebar.selectbox(
    "Prediction",
    prediction_types
)

min_risk = st.sidebar.slider(
    "Minimum Risk Score",
    min_value=0,
    max_value=100,
    value=0
)

# ==========================================================
# FILTER DATA
# ==========================================================

filtered_df = df.copy()

if selected_attack != "All":
    filtered_df = filtered_df[
        filtered_df["label"] == selected_attack
    ]

if selected_prediction != "All":
    filtered_df = filtered_df[
        filtered_df["prediction"] == selected_prediction
    ]

filtered_df = filtered_df[
    filtered_df["risk_score"] >= min_risk
]

# ==========================================================
# KPI VALUES (Always use FULL DATASET)
# ==========================================================

total_events = len(df)

total_attacks = len(
    df[df["label"] != "Normal"]
)

total_anomalies = len(
    df[df["prediction"] == "Anomaly"]
)

avg_risk = round(
    df["risk_score"].mean(),
    2
)

# ==========================================================
# HEADER
# ==========================================================

st.title("🛡 SentinelAI")

st.caption(
    "AI-Powered Behavioral Anomaly Detection Platform"
)

st.divider()

# ==========================================================
# KPI CARDS
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📊 Total Events",
        f"{total_events:,}"
    )

with col2:
    st.metric(
        "🚨 Injected Attacks",
        total_attacks
    )

with col3:
    st.metric(
        "🤖 AI Detected Anomalies",
        total_anomalies
    )

with col4:
    st.metric(
        "⚠️ Average Risk Score",
        avg_risk
    )

st.divider()

# ==========================================================
# CHARTS
# ==========================================================

st.subheader("📊 Security Analytics")

left, right = st.columns(2)

with left:

    st.plotly_chart(
        attack_distribution(filtered_df),
        use_container_width=True
    )

with right:

    st.plotly_chart(
        prediction_distribution(filtered_df),
        use_container_width=True
    )

st.plotly_chart(
    risk_distribution(filtered_df),
    use_container_width=True
)

st.divider()

# ==========================================================
# RECENT EVENTS
# ==========================================================

st.subheader("🚨 Recent Security Events")

st.dataframe(
    filtered_df.sort_values(
        by="risk_score",
        ascending=False
    ),
    use_container_width=True,
    height=450
)