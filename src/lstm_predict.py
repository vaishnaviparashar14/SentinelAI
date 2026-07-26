import joblib
import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model(
    "models/lstm_anomaly_model.keras"
)

scaler = joblib.load(
    "models/lstm_scaler.pkl"
)

threshold = joblib.load(
    "models/lstm_threshold.pkl"
)


def predict_sequence(sequence):

    sequence = np.array(sequence)

    sequence = scaler.transform(sequence)

    sequence = sequence.reshape(1, 10, 16)

    probability = float(model.predict(sequence, verbose=0)[0][0])

    prediction = probability >= threshold

    return {
        "probability": probability,
        "prediction": "Anomaly" if prediction else "Normal",
        "confidence": round(probability * 100, 2)
    }