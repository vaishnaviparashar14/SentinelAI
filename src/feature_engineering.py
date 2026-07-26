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

# ==========================
# Binary Features (KEEP THESE)
# ==========================

# Failed login
df["is_failed_login"] = (
    df["login_status"] == "Failed"
).astype(int)

# High Risk
df["is_high_risk"] = (
    df["risk_score"] >= 80
).astype(int)

# ==========================
# Device Intelligence (KEEP THESE)
# ==========================

df["is_unknown_device"] = (
    df["device_fingerprint"]
    .str.startswith("UNKNOWN")
).fillna(False).astype(int)

df["is_bot_device"] = (
    df["device_fingerprint"]
    .str.startswith("BOT")
).fillna(False).astype(int)

# ==========================
# Country Intelligence (KEEP THIS)
# ==========================

suspicious_countries = [
    "Russia",
    "China",
    "Brazil"
]

df["is_suspicious_country"] = (
    df["geo_location"]
    .isin(suspicious_countries)
).astype(int)

# ==========================
# REMOVED FEATURES:
# - risk_bucket (duplicates risk_score)
# - hour_bucket (duplicates hour)
# - is_office_hours (duplicates hour)
# - is_night_login (duplicates hour)
# - is_weekend (duplicates day_of_week)
# - is_critical_risk (duplicates risk_score)
# ==========================

# ==========================
# Label Encoding
# ==========================

# Categorical columns to encode
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

# Display features created
print("\n=== Features Created (KEPT) ===")
print("✅ is_failed_login - Failed login attempts")
print("✅ is_high_risk - Risk score >= 80")
print("✅ is_unknown_device - Device starts with UNKNOWN")
print("✅ is_bot_device - Device starts with BOT")
print("✅ is_suspicious_country - Country is Russia, China, or Brazil")
print("\n❌ REMOVED: risk_bucket, hour_bucket, is_office_hours, is_night_login, is_weekend, is_critical_risk")

print(f"\nTotal features: {len(df.columns)}")

# Show column names
print(f"\nAll columns: {df.columns.tolist()}")

# Save processed dataset
df.to_csv(
    "data/processed/features_dataset.csv",
    index=False
)

print("\nfeatures_dataset.csv saved successfully!")

# Save encoders for later use
import joblib
joblib.dump(encoders, "models/encoders.pkl")
print("Encoders saved successfully!")