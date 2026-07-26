import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

# ===========================
# Load Dataset
# ===========================

df = pd.read_csv("data/processed/features_dataset.csv")

# Keep only attack records
df = df[df["label"] != "Normal"]

# Drop columns not used for training
drop_cols = [
    "label",
    "entity_id",
    "timestamp",
    "source_ip",
    "command_sequence"
]

X = df.drop(columns=drop_cols)
y = df["label"]

# ===========================
# Train Test Split
# ===========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ===========================
# Parameter Search
# ===========================

param_grid = {

    "n_estimators":[200,300,500,700,1000],

    "max_depth":[
        None,
        10,
        15,
        20,
        30
    ],

    "min_samples_split":[
        2,
        4,
        6,
        8
    ],

    "min_samples_leaf":[
        1,
        2,
        3
    ],

    "max_features":[
        "sqrt",
        "log2"
    ],

    "bootstrap":[
        True,
        False
    ],

    "class_weight":[
        "balanced",
        "balanced_subsample"
    ]
}

rf = RandomForestClassifier(
    random_state=42,
    n_jobs=-1
)

search = RandomizedSearchCV(

    estimator=rf,

    param_distributions=param_grid,

    n_iter=30,

    cv=5,

    scoring="f1_weighted",

    random_state=42,

    verbose=2,

    n_jobs=-1

)

print("Starting Hyperparameter Search...\n")

search.fit(X_train,y_train)

best_model = search.best_estimator_

print("\nBest Parameters\n")
print(search.best_params_)

# ===========================
# Evaluation
# ===========================

pred = best_model.predict(X_test)

print("\nClassification Report\n")
print(classification_report(y_test,pred))

print("\nConfusion Matrix\n")
print(confusion_matrix(y_test,pred))

print("\nMetrics\n")

print(
    "Accuracy :",
    round(accuracy_score(y_test,pred)*100,2)
)

print(
    "Precision:",
    round(
        precision_score(
            y_test,
            pred,
            average="weighted"
        )*100,
        2
    )
)

print(
    "Recall   :",
    round(
        recall_score(
            y_test,
            pred,
            average="weighted"
        )*100,
        2
    )
)

print(
    "F1 Score :",
    round(
        f1_score(
            y_test,
            pred,
            average="weighted"
        )*100,
        2
    )
)

joblib.dump(
    best_model,
    "models/attack_classifier.pkl"
)

print("\nBest model saved successfully!")