import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# ==========================================================
# LOAD DATA
# ==========================================================

df = pd.read_csv("data/processed/features_dataset.csv")

# Only attack samples
attack_df = df[df["label"] != "Normal"].copy()

print(f"Attack Samples: {len(attack_df)}")

# ==========================================================
# FEATURES
# ==========================================================

X = attack_df.drop(
    columns=[
        "entity_id",
        "timestamp",
        "source_ip",
        "label"
    ]
)

y = attack_df["label"]

# ==========================================================
# TRAIN TEST SPLIT
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ==========================================================
# MODEL
# ==========================================================

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train, y_train)

# ==========================================================
# EVALUATION
# ==========================================================

predictions = model.predict(X_test)

print("\nClassification Report\n")

print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)

# ==========================================================
# SAVE MODEL
# ==========================================================

joblib.dump(
    {
        "model": model,
        "features": X.columns.tolist()
    },
    "models/attack_classifier.pkl"
)

print("\nModel saved successfully!")