import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("data/processed/cybersecurity_dataset.csv")

print("Dataset Loaded Successfully")
print(df.head())

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Extract time features
df["hour"] = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.dayofweek

# Encode categorical columns
categorical_cols = [
    "entity_type",
    "geo_location",
    "resource_accessed",
    "auth_method",
    "device_fingerprint",
    "login_status"
]

encoders = {}

for col in categorical_cols:
    encoder = LabelEncoder()
    df[col] = encoder.fit_transform(df[col])
    encoders[col] = encoder

print("\nFeature Engineering Completed!")
print(df.head())

# Save processed dataset
df.to_csv(
    "data/processed/features_dataset.csv",
    index=False
)

print("features_dataset.csv saved successfully!")