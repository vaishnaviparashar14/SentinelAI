import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest

# ==========================================================
# LOAD DATA
# ==========================================================

# Encoded dataset (used for ML)
features_df = pd.read_csv(
    "data/processed/features_dataset.csv"
)

# Original dataset (used for dashboard)
original_df = pd.read_csv(
    "data/processed/cybersecurity_dataset.csv"
)

print("Datasets Loaded Successfully!")

# ==========================================================
# FEATURES FOR ISOLATION FOREST
# ==========================================================

feature_columns = [
    col for col in features_df.columns
    if col not in ["entity_id", "timestamp", "label", "source_ip"]
]

X = features_df[feature_columns]

# ==========================================================
# ISOLATION FOREST
# ==========================================================

iso_model = IsolationForest(
    contamination=0.03,
    random_state=42
)

iso_model.fit(X)

iso_predictions = iso_model.predict(X)

# ==========================================================
# STORE PREDICTIONS
# ==========================================================

original_df["prediction"] = pd.Series(iso_predictions).map({
    1: "Normal",
    -1: "Anomaly"
})

original_df["is_attack"] = original_df["label"].apply(
    lambda x: "Normal" if x == "Normal" else "Anomaly"
)

# ==========================================================
# LOAD RANDOM FOREST CLASSIFIER
# ==========================================================

classifier_bundle = joblib.load("models/attack_classifier.pkl")

rf_model = classifier_bundle["model"]
rf_features = classifier_bundle["features"]

# Default values
original_df["predicted_attack"] = "Normal"
original_df["confidence"] = 100.0

# ==========================================================
# CLASSIFY ONLY ANOMALIES
# ==========================================================

anomaly_indices = original_df[
    original_df["prediction"] == "Anomaly"
].index

if len(anomaly_indices) > 0:

    anomaly_features = features_df.loc[
        anomaly_indices,
        rf_features
    ]

    predicted_attack = rf_model.predict(anomaly_features)

    probabilities = rf_model.predict_proba(anomaly_features)

    confidence = probabilities.max(axis=1) * 100

    original_df.loc[
        anomaly_indices,
        "predicted_attack"
    ] = predicted_attack

    original_df.loc[
        anomaly_indices,
        "confidence"
    ] = confidence.round(2)

# ==========================================================
# SUMMARY
# ==========================================================

print("\nPrediction Summary")
print(original_df["prediction"].value_counts())

print("\nPredicted Attack Types")
print(original_df["predicted_attack"].value_counts())

print("\nActual Attack Distribution")
print(original_df["label"].value_counts())

# ==========================================================
# SAVE
# ==========================================================

original_df.to_csv(
    "data/processed/predictions.csv",
    index=False
)

print("\npredictions.csv saved successfully!")

# ==========================================================
# SIMPLE EVALUATION
# ==========================================================

correct = (
    original_df["prediction"]
    == original_df["is_attack"]
).sum()

accuracy = correct / len(original_df) * 100

print(f"\nDetection Accuracy: {accuracy:.2f}%")