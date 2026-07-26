def calculate_risk(
    rf_prediction,
    isolation_score,
    lstm_probability
):

    score = 0

    if rf_prediction != "Normal":
        score += 50

    if isolation_score == -1:
        score += 25

    score += int(lstm_probability * 25)

    return min(score,100)