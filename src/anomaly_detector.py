import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report

# Load processed dataset
df = pd.read_csv("data/processed/features_dataset.csv")

print("Dataset Loaded Successfully!")

# Features for training
X = df.drop(
    columns=[
        "entity_id",
        "timestamp",
        "label",
        "source_ip"
    ]
)

# Train Isolation Forest
model = IsolationForest(
    contamination=0.03,
    random_state=42
)
print(X.dtypes)
model.fit(X)

# Predict
predictions = model.predict(X)

# Convert prediction labels
df["prediction"] = predictions

df["prediction"] = df["prediction"].map({
    1: "Normal",
    -1: "Anomaly"
})
df["is_attack"] = df["label"].apply(
    lambda x: "Normal" if x == "Normal" else "Anomaly"
)

print("\nPrediction Summary")
print(df["prediction"].value_counts())

print("\nActual Attack Distribution")
print(df["label"].value_counts())

# Save predictions
df.to_csv(
    "data/processed/predictions.csv",
    index=False
)

print("predictions.csv saved successfully!")
correct = (df["prediction"] == df["is_attack"]).sum()

accuracy = correct / len(df) * 100

print(f"\nDetection Accuracy: {accuracy:.2f}%")