import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# Initialize Faker
fake = Faker()

# For reproducible results
random.seed(42)
np.random.seed(42)
Faker.seed(42)
# -------------------------------
# Configuration
# -------------------------------

NUM_USERS = 50
NUM_DEVICES = 100
NUM_EVENTS = 15000

COUNTRIES = [
    "India",
    "USA",
    "Germany",
    "UK",
    "Canada",
    "Australia",
    "Japan"
]

AUTH_METHODS = [
    "Password",
    "Token",
    "Certificate",
    "Biometric"
]

RESOURCES = [
    "Employee Portal",
    "Payroll",
    "Database",
    "HR System",
    "Cloud Storage",
    "Admin Panel",
    "VPN",
    "Finance Server",
    "Source Code Repo"
]

ENTITY_TYPES = [
    "User",
    "Service Account",
    "Edge Device"
]
# -------------------------------
# Generate Users
# -------------------------------

users = []

for i in range(NUM_USERS):
    users.append({
        "entity_id": f"USER_{i+1:03}",
        "entity_type": "User",
        "home_country": random.choice(COUNTRIES),
        "preferred_auth": random.choice(AUTH_METHODS)
    })

print(f"Generated {len(users)} users.")
# -------------------------------
# Generate Devices
# -------------------------------

devices = []

for i in range(NUM_DEVICES):
    devices.append({
        "device_id": f"DEVICE_{i+1:03}",
        "device_fingerprint": fake.uuid4()
    })

print(f"Generated {len(devices)} devices.")
# -------------------------------
# Generate Normal Login Events
# -------------------------------

events = []

start_time = datetime.now() - timedelta(days=30)

for _ in range(NUM_EVENTS):

    user = random.choice(users)
    device = random.choice(devices)

    login_time = start_time + timedelta(
        minutes=random.randint(0, 30 * 24 * 60)
    )

    event = {
    "entity_id": user["entity_id"],
    "entity_type": user["entity_type"],
    "timestamp": login_time,
    "source_ip": fake.ipv4_public(),
    "geo_location": user["home_country"],
    "resource_accessed": random.choice(RESOURCES),
    "auth_method": user["preferred_auth"],
    "session_duration": random.randint(5, 240),
    "command_sequence": random.randint(1, 25),
    "device_fingerprint": device["device_fingerprint"],

    # New Fields
    "login_status": "Success",
    "risk_score": 0,

    "label": "Normal"
}

    events.append(event)

print(f"Generated {len(events)} normal login events.")
# -------------------------------
# Convert to DataFrame
# -------------------------------

df = pd.DataFrame(events)

print(df.head())
# -------------------------------
# Save Dataset
# -------------------------------

os.makedirs("data/raw", exist_ok=True)

output_path = "data/raw/normal_login_events.csv"

df.to_csv(output_path, index=False)

print(f"\nDataset saved successfully at: {output_path}")
