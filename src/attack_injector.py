import pandas as pd
import random

COUNTRIES = [
    "India",
    "USA",
    "Germany",
    "Japan",
    "Australia",
    "Singapore",
    "Canada",
    "Brazil"
]

df = pd.read_csv("data/raw/normal_login_events.csv")

print(f"Loaded {len(df)} events.")


def inject_brute_force(df):

    NUM_ATTACK_USERS = 15

    selected_users = random.sample(
        list(df["entity_id"].unique()),
        NUM_ATTACK_USERS
    )

    for user in selected_users:

        user_events = df[df["entity_id"] == user]

        if len(user_events) < 6:
            continue

        attack_events = user_events.sample(6).sort_values("timestamp")

        attack_indices = attack_events.index.tolist()

        for idx in attack_indices[:-1]:
            df.loc[idx, "login_status"] = "Failed"
            df.loc[idx, "risk_score"] = random.randint(90, 100)
            df.loc[idx, "label"] = "Brute Force"

        final_idx = attack_indices[-1]

        df.loc[final_idx, "login_status"] = "Success"
        df.loc[final_idx, "risk_score"] = random.randint(94, 100)
        df.loc[final_idx, "label"] = "Brute Force"

    print("Brute Force attacks injected successfully!")
    return df


def inject_impossible_travel(df):

    NUM_IMPOSSIBLE_USERS = 10

    selected_users = random.sample(
        list(df["entity_id"].unique()),
        NUM_IMPOSSIBLE_USERS
    )

    for user in selected_users:

        user_events = df[df["entity_id"] == user]

        if len(user_events) < 2:
            continue

        attack_events = user_events.sample(2).sort_values("timestamp")

        first_idx = attack_events.index[0]
        second_idx = attack_events.index[1]

        country1 = random.choice(COUNTRIES)
        country2 = random.choice(
            [c for c in COUNTRIES if c != country1]
        )

        df.loc[first_idx, "geo_location"] = country1
        df.loc[second_idx, "geo_location"] = country2

        df.loc[first_idx, "risk_score"] = random.randint(80, 88)
        df.loc[second_idx, "risk_score"] = random.randint(90, 98)

       

        df.loc[first_idx, "label"] = "Impossible Travel"
        df.loc[second_idx, "label"] = "Impossible Travel"

    print("Impossible Travel attacks injected successfully!")
    return df

def inject_device_spoofing(df):

    NUM_DEVICE_USERS = 10

    selected_users = random.sample(
        list(df["entity_id"].unique()),
        NUM_DEVICE_USERS
    )

    for user in selected_users:

        user_events = df[df["entity_id"] == user]

        if len(user_events) < 3:
            continue

        attack_events = user_events.sample(3)

        for idx in attack_events.index:

            fake_device = (
                "UNKNOWN-"
                + "".join(
                    random.choices(
                        "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
                        k=8
                    )
                )
            )

            df.loc[idx, "device_fingerprint"] = fake_device
            df.loc[idx, "risk_score"] = random.randint(70, 90)
            df.loc[idx, "label"] = "Device Spoofing"

    print("Device Spoofing attacks injected successfully!")

    return df

def inject_credential_stuffing(df):

    NUM_EVENTS = 25

    attack_indices = random.sample(
        list(df.index),
        NUM_EVENTS
    )

    attacker_ip = "185.201.10.5"

    for i, idx in enumerate(attack_indices):

        df.loc[idx, "source_ip"] = attacker_ip
        df.loc[idx, "risk_score"] = random.randint(90, 99)
        df.loc[idx, "label"] = "Credential Stuffing"

        if i < NUM_EVENTS - 1:
            df.loc[idx, "login_status"] = "Failed"
        else:
            df.loc[idx, "login_status"] = "Success"

    print("Credential Stuffing attacks injected successfully!")

    return df

df = inject_brute_force(df)
df = inject_impossible_travel(df)
df = inject_device_spoofing(df)
df = inject_credential_stuffing(df)

df.to_csv(
    "data/processed/cybersecurity_dataset.csv",
    index=False
)

print("Cybersecurity dataset saved successfully!")
