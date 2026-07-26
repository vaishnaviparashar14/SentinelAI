# 🛡️ SentinelAI

## AI-Powered Behavioral Threat Detection Platform

SentinelAI is an AI-driven cybersecurity platform that detects known attacks, identifies anomalous user behavior, and provides explainable threat intelligence through an interactive Security Operations Center (SOC) dashboard.

The platform combines Machine Learning, Deep Learning, and Explainable AI to improve cyber threat detection and assist security analysts in making informed decisions.

---

## Features

- Known attack detection using Random Forest
- Anomaly detection using Isolation Forest
- Behavioral analysis using Bidirectional LSTM
- AI Threat Fusion Engine for unified risk scoring
- Explainable AI with MITRE ATT&CK mapping
- Interactive Streamlit dashboard
- Real-time security analytics
- Actionable incident response recommendations

---

## System Architecture

```
User Login Events
        │
        ▼
Synthetic Cybersecurity Dataset
        │
        ▼
Feature Engineering
        │
        ▼
 ┌──────────┬──────────────┬──────────────┐
 │          │              │
 ▼          ▼              ▼
Random   Isolation    Bidirectional
Forest    Forest          LSTM
 │          │              │
 └──────────┴──────────────┘
            │
            ▼
 AI Threat Fusion Engine
            │
            ▼
   Explainable AI Module
            │
            ▼
 Streamlit SOC Dashboard
```

---

## Technology Stack

- Python
- Scikit-learn
- TensorFlow / Keras
- Streamlit
- Plotly
- Pandas
- NumPy
- Joblib

---

## Project Structure

```
SentinelAI/
│
├── dashboard/
├── data/
├── models/
├── reports/
├── src/
├── requirements.txt
├── README.md
```

---

## Dataset

- 15,000 Synthetic Security Events
- 506 Simulated Attack Scenarios
- Authentication Logs
- Network Activity
- Device Events
- Behavioral Features

---

## AI Models

### Random Forest
Classifies known cyberattack patterns.

### Isolation Forest
Detects anomalous and previously unseen behavior.

### Bidirectional LSTM
Analyzes sequential user behavior and predicts threat probability.

---

## Performance

| Metric | Value |
|---------|------:|
| Accuracy | **95.89%** |
| Precision | **85.60%** |
| Recall | **98.81%** |
| F1-Score | **92.75%** |

---

## Dashboard

The Streamlit dashboard provides:

- AI Detection Engine
- Threat Severity Analysis
- Overall Risk Score
- Recommended Actions
- Security Analytics
- Incident Investigation

---

## Future Enhancements

- Real-time SIEM integration
- Cloud deployment
- Threat Intelligence APIs
- Email and SMS alerts
- Live network monitoring

---

## Author

**Vaishnavi Parashar**

Hackathon Project – SentinelAI