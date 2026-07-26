def generate_explanation(row):

    reasons = []
    actions = []

    # -------------------------
    # Risk Level
    # -------------------------

    if row["risk_score"] >= 90:
        risk_level = "🔴 Critical"

    elif row["risk_score"] >= 70:
        risk_level = "🟠 High"

    elif row["risk_score"] >= 50:
        risk_level = "🟡 Medium"

    else:
        risk_level = "🟢 Low"

    # -------------------------
    # Reasons
    # -------------------------

    if row["risk_score"] >= 90:
        reasons.append("Extremely high risk score")

    elif row["risk_score"] >= 70:
        reasons.append("High risk score")

    if row["prediction"] == "Anomaly":
        reasons.append("Isolation Forest detected abnormal behavior")

    if row["login_status"] != 1:
        reasons.append("Authentication failed")

    if row["session_duration"] < 60:
        reasons.append("Unusually short session")

    # -------------------------
    # Recommended Actions
    # -------------------------

    if row["prediction"] == "Anomaly":

        actions.append("Lock the affected account")

        actions.append("Notify SOC analyst")

        actions.append("Require MFA verification")

        actions.append("Review recent login activity")

    else:

        actions.append("Continue monitoring")

    return risk_level, reasons, actions