import plotly.express as px


def attack_distribution(df):
    attack_df = df[df["label"] != "Normal"]

    fig = px.pie(
        attack_df,
        names="label",
        title="Attack Distribution",
        hole=0.5
    )

    fig.update_layout(height=400)

    return fig


def prediction_distribution(df):

    fig = px.bar(
        df["prediction"].value_counts().reset_index(),
        x="prediction",
        y="count",
        title="AI Prediction Distribution"
    )

    fig.update_layout(height=400)

    return fig


def risk_distribution(df):

    fig = px.histogram(
        df,
        x="risk_score",
        nbins=20,
        title="Risk Score Distribution"
    )

    fig.update_layout(height=400)

    return fig