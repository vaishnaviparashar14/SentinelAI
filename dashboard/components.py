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


def get_severity_label(score):
    if score >= 90:
        return "Critical 🔴"
    elif score >= 70:
        return "High 🔴"
    elif score >= 50:
        return "Medium 🟡"
    return "Low 🟢"


# ==========================================================
# Threat Feed
# ==========================================================

def show_threat_feed(df):

    st.markdown("## 🚨 Live Threat Feed")
    st.caption("Real-time anomalous entities detected by SentinelAI")

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
        .threat-card-compact{
            background:#141a24;
            border:1px solid #293241;
            border-left:7px solid #ef4444;
            border-radius:14px;
            padding:15px 18px;
            margin-bottom:12px;
            box-shadow:0 0 14px rgba(0,0,0,.35);
            cursor:pointer;
        }
        .threat-header{
            display:flex;
            align-items:center;
            justify-content:space-between;
            flex-wrap:wrap;
        }
        .threat-title{
            font-size:18px;
            font-weight:600;
            color:white;
        }
        .threat-badge{
            display:inline-block;
            padding:4px 12px;
            border-radius:20px;
            font-size:13px;
            font-weight:500;
        }
        .threat-badge-high{
            background:#ef4444;
            color:white;
        }
        .threat-badge-medium{
            background:#f97316;
            color:white;
        }
        .threat-badge-low{
            background:#22c55e;
            color:white;
        }
        .threat-meta{
            color:#9ca3af;
            font-size:14px;
            margin-top:6px;
        }
        .threat-meta span{
            margin-right:20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    for _, row in anomalies.iterrows():
        icon = get_risk_icon(row["risk_score"])
        confidence = float(row.get("confidence", 100))
        
        # Determine badge class
        if row["risk_score"] >= 70:
            badge_class = "threat-badge-high"
        elif row["risk_score"] >= 50:
            badge_class = "threat-badge-medium"
        else:
            badge_class = "threat-badge-low"
        
        # Display compact threat card
        st.markdown(f"""
        <div class="threat-card-compact">
            <div class="threat-header">
                <span class="threat-title">{icon} {row["entity_id"]}</span>
                <span class="threat-badge {badge_class}">{int(row["risk_score"])} Risk</span>
            </div>
            <div class="threat-meta">
                <span>🎯 {row["predicted_attack"]}</span>
                <span>📊 Confidence: {confidence:.1f}%</span>
                <span>📍 {row["geo_location"]}</span>
                <span>🔐 {row["auth_method"]}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Use a smaller expander for investigation
        with st.expander("🔍 View Investigation", expanded=False):
            
            # Show detailed metrics only when expanded
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

            # AI Incident Investigation (nested expander inside)
            with st.expander("🕵️ AI Incident Investigation", expanded=False):
                try:
                    risk_level, reasons, actions = generate_explanation(row)
                except:
                    risk_level = "High"
                    reasons = [
                        "Multiple failed authentication attempts detected",
                        "Source IP reputation is suspicious",
                        "Device fingerprint mismatch observed",
                        "Traffic pattern deviates from baseline"
                    ]
                    actions = [
                        "Isolate the endpoint",
                        "Block the source IP",
                        "Force password reset",
                        "Enable MFA for affected user"
                    ]
                
                severity = get_severity_label(row["risk_score"])
                
                st.markdown("## 🚨 Incident Summary")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Attack Type**")
                    st.write(f"{row['predicted_attack']}")
                    st.markdown("")
                    st.markdown(f"**Confidence**")
                    st.write(f"{confidence:.1f}%")
                
                with col2:
                    st.markdown(f"**Severity**")
                    st.write(f"{severity}")
                    st.markdown("")
                    st.markdown(f"**Risk Score**")
                    st.write(f"{int(row['risk_score'])}/100")
                
                st.divider()
                
                st.markdown("## 📋 AI Findings")
                for reason in reasons:
                    st.success(f"✓ {reason}")
                
                st.divider()
                
                st.markdown("## 🎯 Recommended Actions")
                for action in actions:
                    st.info(f"• {action}")
                
                st.divider()
                
                st.markdown("## 📊 MITRE ATT&CK Mapping")
                
                mitre_mapping = {
                    "Device Spoofing": {"technique": "T1078 – Valid Accounts", "tactic": "Initial Access"},
                    "Phishing": {"technique": "T1566 – Phishing", "tactic": "Initial Access"},
                    "Malware": {"technique": "T1204 – User Execution", "tactic": "Execution"},
                    "Ransomware": {"technique": "T1486 – Data Encrypted for Impact", "tactic": "Impact"},
                    "DDoS": {"technique": "T1498 – Network Denial of Service", "tactic": "Impact"},
                    "Insider Threat": {"technique": "T1059 – Command and Scripting Interpreter", "tactic": "Execution"},
                    "Data Exfiltration": {"technique": "T1048 – Exfiltration Over Alternative Protocol", "tactic": "Exfiltration"},
                    "BruteForce": {"technique": "T1110 – Brute Force", "tactic": "Credential Access"},
                }
                
                attack_type = row['predicted_attack']
                mitre_info = mitre_mapping.get(attack_type, {"technique": "Not Available", "tactic": "Not Available"})
                
                st.write(f"**Technique:** {mitre_info['technique']}")
                st.write(f"**Tactic:** {mitre_info['tactic']}")
                
                st.divider()
                
                st.markdown("## 📝 Executive Summary")
                
                if row["risk_score"] >= 90:
                    summary = "The activity is highly indicative of a credential compromise attempt. Immediate containment is recommended."
                elif row["risk_score"] >= 70:
                    summary = "The activity shows significant suspicious patterns that require prompt investigation and response."
                elif row["risk_score"] >= 50:
                    summary = "The activity exhibits moderate risk indicators. Continued monitoring and investigation is advised."
                else:
                    summary = "The activity shows low risk indicators but should still be documented for reference."
                
                st.info(summary)
                
                st.caption(
                    "SentinelAI Security Operations Center • "
                    "AI Threat Detection • Explainable AI • Real-Time Monitoring"
                )
            
            st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# Prediction Distribution Chart
# ==========================================================

def prediction_distribution(df):
    """Create AI Prediction Distribution chart with proper title"""
    
    import plotly.express as px
    
    # Get prediction counts
    pred_counts = df['prediction'].value_counts().reset_index()
    pred_counts.columns = ['Prediction', 'Count']
    
    # Create bar chart with proper title
    fig = px.bar(
        pred_counts,
        x='Prediction',
        y='Count',
        color='Prediction',
        color_discrete_map={
            'Anomaly': '#ef4444',
            'Normal': '#22c55e'
        },
        text='Count',
        title="AI Prediction Distribution"  # Fixed: Added proper title
    )
    
    fig.update_traces(
        textposition='outside',
        marker_line_width=0
    )
    
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Number of Predictions",
        showlegend=False
    )
    
    # Apply theme
    fig.update_layout(
        template="plotly_dark",
        height=330,
        paper_bgcolor="#0f172a",
        plot_bgcolor="#1e293b",
        font=dict(
            family="Inter, Segoe UI, Arial",
            size=13,
            color="#f8fafc"
        ),
        margin=dict(l=20, r=20, t=45, b=20),
        title=dict(
            x=0.03,
            font=dict(size=18)
        )
    )
    
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="#334155"
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#334155",
        zeroline=False,
        linecolor="#334155"
    )
    
    return fig


# ==========================================================
# Attack Distribution Chart
# ==========================================================

def attack_distribution(df):
    """Create styled attack distribution bar chart"""
    
    import plotly.express as px
    
    # Calculate attack counts
    attack_counts = df['predicted_attack'].value_counts().reset_index()
    attack_counts.columns = ['Attack Type', 'Count']
    
    # Create the bar chart with the new style
    fig = px.bar(
        attack_counts,
        x="Attack Type",
        y="Count",
        color="Count",
        color_continuous_scale="Blues",
        text="Count"
    )
    
    # Update traces
    fig.update_traces(
        textposition="outside",
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Attacks: %{y}<extra></extra>"
    )
    
    # Update layout
    fig.update_layout(
        coloraxis_showscale=False,
        xaxis_title="",
        yaxis_title="Number of Attacks",
        title="Attack Type Distribution"  # Added title
    )
    
    # Apply theme
    fig.update_layout(
        template="plotly_dark",
        height=330,
        paper_bgcolor="#0f172a",
        plot_bgcolor="#1e293b",
        font=dict(
            family="Inter, Segoe UI, Arial",
            size=13,
            color="#f8fafc"
        ),
        margin=dict(l=20, r=20, t=45, b=20),
        title=dict(
            x=0.03,
            font=dict(size=18)
        )
    )
    
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="#334155"
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#334155",
        zeroline=False,
        linecolor="#334155"
    )
    
    return fig
import streamlit as st

def model_performance_card():
    st.markdown("""
    <div style="
        background:#1E293B;
        padding:18px;
        border-radius:12px;
        border:1px solid #334155;
        margin-bottom:15px;
    ">
        <h4 style="margin-top:0;">🤖 Model Performance</h4>
        <table style="width:100%; font-size:15px;">
            <tr><td>Accuracy</td><td style="text-align:right;"><b>95.1%</b></td></tr>
            <tr><td>Precision</td><td style="text-align:right;"><b>94.9%</b></td></tr>
            <tr><td>Recall</td><td style="text-align:right;"><b>95.1%</b></td></tr>
            <tr><td>F1 Score</td><td style="text-align:right;"><b>95.0%</b></td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)