import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# SentinelAI Professional Theme
# -----------------------------
BG_COLOR = "#0f172a"
CARD_COLOR = "#1e293b"
GRID_COLOR = "#334155"
TEXT_COLOR = "#f8fafc"


def apply_theme(fig, height=340):
    """Apply SentinelAI professional theme to plotly figure"""
    
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=CARD_COLOR,
        font=dict(
            family="Inter, Segoe UI",
            size=13,
            color=TEXT_COLOR
        ),
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(
            orientation="h",
            y=1.08,
            x=1,
            xanchor="right",
            bgcolor="rgba(0,0,0,0)"
        ),
        title={
            'text': "AI Prediction Distribution",
            'x': 0.03,
            'font': {'size': 20}
        }
    )

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRID_COLOR
    )

    return fig


# ===============================
# Attack Distribution
# ===============================
def attack_distribution(df):

    attack_df = df[df["label"] != "Normal"]

    # Get unique labels and their counts
    labels = attack_df["label"].value_counts().index.tolist()
    values = attack_df["label"].value_counts().values.tolist()
    
    # Create figure using go.Figure
    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            hole=0.68,
            textinfo="percent",
            textfont_size=16,
            textposition="inside",
            pull=[0.02] * len(labels),
            hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>",
            marker=dict(colors=px.colors.sequential.Blues_r)
        )
    ])

    fig.update_layout(
        height=360,
        margin=dict(l=25, r=25, t=60, b=20),
        legend=dict(
            orientation="h",
            y=1.08,
            x=0.5,
            xanchor="center",
            font=dict(size=13),
            itemwidth=70
        ),
        uniformtext_minsize=12,
        uniformtext_mode="hide",
        title={
            'text': "Attack Distribution",
            'x': 0.03,
            'font': {'size': 20}
        }
    )

    return apply_theme(fig, 360)


# ===============================
# AI Prediction Distribution
# ===============================
def prediction_distribution(df):

    # Get prediction counts
    pred_counts = df["prediction"].value_counts()
    labels = pred_counts.index.tolist()
    values = pred_counts.values.tolist()
    
    # Create figure using go.Figure
    fig = go.Figure(data=[
        go.Bar(
            x=labels,
            y=values,
            text=values,
            textposition="outside",
            marker=dict(
                color=values,
                colorscale="Blues",
                line_width=0
            ),
            hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>"
        )
    ])

    fig.update_layout(
        coloraxis_showscale=False,
        xaxis_title="",
        yaxis_title="Predictions",
        title={
            'text': "AI Prediction Distribution",
            'x': 0.03,
            'font': {'size': 20}
        }
    )

    return apply_theme(fig, 340)


# ===============================
# Risk Score Distribution
# ===============================
def risk_distribution(df):

    # Create figure using go.Figure
    fig = go.Figure(data=[
        go.Histogram(
            x=df["risk_score"],
            nbinsx=25,
            marker=dict(color="#3b82f6"),
            hovertemplate="Risk Score: %{x}<br>Count: %{y}<extra></extra>"
        )
    ])

    fig.update_layout(
        xaxis_title="Risk Score",
        yaxis_title="Events",
        title={
            'text': "Risk Score Distribution",
            'x': 0.03,
            'font': {'size': 20}
        }
    )

    return apply_theme(fig, 340)