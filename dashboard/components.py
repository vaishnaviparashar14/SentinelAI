import streamlit as st
import sys
import os

sys.path.append(os.path.abspath("src"))

from explainability import generate_explanation


# ==========================================================
# Risk Indicator
# ==========================================================

def get_risk_icon(score):
    if score >= 90:
        return "🔴"
    elif score >= 70:
        return "🟠"
    elif score >= 50:
        return "🟡"
    return "🟢"


def get_risk_color(score):
    if score >= 90:
        return "#ef4444"
    elif score >= 70:
        return "#f97316"
    elif score >= 50:
        return "#facc15"
    return "#22c55e"


# ==========================================================
# Threat Feed
# ==========================================================

def show_threat_feed(df):

    st.subheader("🚨 Live Threat Feed")

    anomalies = (
        df[df["prediction"] == "Anomaly"]
        .sort_values("risk_score", ascending=False)
        .head(10)
    )

    if anomalies.empty:
        st.success("✅ No active threats detected.")
        return

    st.markdown(
        """
        <style>

        .threat-card{
            background:#141a24;
            border:1px solid #293241;
            border-left:7px solid #ef4444;
            border-radius:14px;
            padding:18px;
            margin-bottom:18px;
            box-shadow:0 0 14px rgba(0,0,0,.35);
        }

        .section-title{
            color:#9ca3af;
            font-size:13px;
            margin-bottom:4px;
        }

        .value{
            font-size:18px;
            font-weight:600;
            color:white;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
    for _, row in anomalies.iterrows():

        icon = get_risk_icon(row["risk_score"])
        color = get_risk_color(row["risk_score"])
        confidence = float(row.get("confidence", 100))

        if confidence >= 95:
            confidence_badge = "🟢 High Confidence"
        elif confidence >= 80:
            confidence_badge = "🟡 Medium Confidence"
        else:
            confidence_badge = "🔴 Low Confidence"

        st.markdown(
            f"""
            <div class="threat-card">

            <h3 style="margin-bottom:10px;">
            {icon} {row["entity_id"]}
            </h3>

            </div>
            """,
            unsafe_allow_html=True,
        )

        top1, top2, top3, top4 = st.columns(4)

        with top1:
            st.metric(
                "Risk Score",
                int(row["risk_score"])
            )

        with top2:
            st.metric(
                "Prediction",
                row["prediction"]
            )

        with top3:
            st.metric(
                "Attack Type",
                row["predicted_attack"]
            )

        with top4:
            st.metric(
                "Confidence",
                f"{confidence:.1f}%"
            )

        st.progress(
            confidence / 100,
            text=f"AI Confidence : {confidence:.2f}%"
        )

        info1, info2 = st.columns(2)

        with info1:

            st.markdown("### 🌐 Network Information")

            st.write(f"**Source IP:** {row['source_ip']}")
            st.write(f"**Geo Location:** {row['geo_location']}")
            st.write(f"**Authentication:** {row['auth_method']}")

        with info2:

            st.markdown("### 💻 Device Information")

            st.write(f"**Device Fingerprint:** {row['device_fingerprint']}")
            st.write(f"**Session Duration:** {row['session_duration']} minutes")
            st.write(f"**Command Sequence:** {row['command_sequence']}")

        st.success(confidence_badge)

        st.caption(
            "Detection Pipeline : Isolation Forest ➜ Random Forest ➜ Explainable AI"
        )

        with st.expander(
            "🕵 Incident Investigation",
            expanded=False
        ):
            risk_level, reasons, actions = generate_explanation(row)

            st.markdown("## 🚨 Executive Incident Summary")

            summary1, summary2 = st.columns([2, 1])

            with summary1:

                st.markdown(
                    f"""
### Threat Overview

- **Entity ID:** `{row['entity_id']}`
- **Risk Level:** **{risk_level}**
- **Predicted Attack:** **{row['predicted_attack']}**
- **Detection Result:** **{row['prediction']}**
- **Confidence:** **{confidence:.2f}%**
                    """
                )

            with summary2:

                st.metric(
                    "Risk Score",
                    int(row["risk_score"])
                )

                st.metric(
                    "Location",
                    row["geo_location"]
                )

            st.divider()

            st.markdown("## 🤖 AI Investigation")

            for reason in reasons:
                st.success(reason)

            st.divider()

            left, right = st.columns(2)

            with left:

                st.markdown("### 🌐 Network Details")

                st.write(f"**Source IP:** {row['source_ip']}")
                st.write(f"**Authentication:** {row['auth_method']}")
                st.write(f"**Geo Location:** {row['geo_location']}")

                st.write(f"**Session Duration:** {row['session_duration']} min")

            with right:

                st.markdown("### 💻 Endpoint Details")

                st.write(f"**Device Fingerprint:** {row['device_fingerprint']}")
                st.write(f"**Command Sequence:** {row['command_sequence']}")
                st.write(f"**Predicted Attack:** {row['predicted_attack']}")
                st.write(f"**Detection:** {row['prediction']}")

            st.divider()

            st.markdown("## ⚠ Indicators of Compromise")

            indicators = []

            if row["risk_score"] >= 90:
                indicators.append("Critical risk score detected.")

            if confidence >= 95:
                indicators.append("Very high model confidence.")

            if row["prediction"] == "Anomaly":
                indicators.append("Behavior deviates significantly from historical baseline.")

            if row["auth_method"] != "Password":
                indicators.append(f"Authentication method: {row['auth_method']}")

            for indicator in indicators:
                st.warning(indicator)

            st.divider()

            st.markdown("## 🛡 Recommended Response")

            for action in actions:
                st.info(action)

            st.divider()

            analyst1, analyst2 = st.columns(2)

            with analyst1:

                st.metric(
                    "Final Verdict",
                    risk_level
                )

            with analyst2:

                st.metric(
                    "Threat Type",
                    row["predicted_attack"]
                )

            st.divider()

            st.markdown("## 📊 Incident Timeline")

            timeline = [
                "🟢 Login session initiated",
                "🟡 Unusual behavioural pattern detected",
                "🟠 Isolation Forest flagged anomaly",
                "🔴 Random Forest classified attack",
                "🔵 Explainable AI generated recommendations",
            ]

            for event in timeline:
                st.write(event)

            st.divider()

            if row["risk_score"] >= 90:
                st.error(
                    "🚨 Critical Severity Incident\n\n"
                    "Immediate analyst intervention is recommended."
                )

            elif row["risk_score"] >= 70:
                st.warning(
                    "⚠ High Severity Incident\n\n"
                    "Investigate this activity as soon as possible."
                )

            elif row["risk_score"] >= 50:
                st.info(
                    "ℹ Medium Severity Incident\n\n"
                    "Continue monitoring this entity."
                )

            else:
                st.success(
                    "✅ Low Severity Incident\n\n"
                    "No immediate action required."
                )

            st.divider()

            st.caption(
                "SentinelAI Security Operations Center • "
                "AI Threat Detection • Explainable AI • Real-Time Monitoring"
            )

        st.markdown("<br>", unsafe_allow_html=True)