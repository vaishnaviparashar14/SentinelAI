import numpy as np
import pandas as pd
import joblib

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional, Input
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')

# ==========================================
# PART 1: LOAD DATA
# ==========================================

df = pd.read_csv("data/processed/features_dataset.csv")

print("Dataset Loaded Successfully!")
print(f"Shape: {df.shape}")

# Sort events chronologically by entity and timestamp
df = df.sort_values(["entity_id", "timestamp"])

# ==========================================
# PART 2: FEATURE SELECTION
# ==========================================

feature_columns = [
    col for col in df.columns
    if col not in [
        "entity_id",
        "timestamp",
        "source_ip",
        "label"
    ]
]

print(f"\nTotal features: {len(feature_columns)}")

# Prepare feature matrix and labels
X = df[feature_columns].values
y = (df["label"] != "Normal").astype(int).values

print(f"Anomaly Count: {sum(y)}")
print(f"Normal Count: {len(y) - sum(y)}")

# ==========================================
# PART 3: SCALE FEATURES
# ==========================================

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ==========================================
# PART 4: CREATE SEQUENCES WITH STRIDE
# ==========================================

SEQUENCE_LENGTH = 10
STRIDE = 2

X_sequences = []
y_sequences = []
entity_sequences = []

unique_entities = df["entity_id"].unique()
print(f"\nTotal unique entities: {len(unique_entities)}")

for entity in unique_entities:
    entity_df = df[df["entity_id"] == entity]
    
    entity_features = scaler.transform(
        entity_df[feature_columns].values
    )
    
    entity_labels = (
        entity_df["label"] != "Normal"
    ).astype(int).values
    
    for i in range(0, len(entity_df) - SEQUENCE_LENGTH, STRIDE):
        X_sequences.append(
            entity_features[i:i + SEQUENCE_LENGTH]
        )
        y_sequences.append(
            entity_labels[i + SEQUENCE_LENGTH]
        )
        entity_sequences.append(entity)

X_sequences = np.array(X_sequences)
y_sequences = np.array(y_sequences)

print(f"Sequences Shape: {X_sequences.shape}")
print(f"Anomaly sequences: {sum(y_sequences)}")
print(f"Normal sequences: {len(y_sequences) - sum(y_sequences)}")

# ==========================================
# PART 5: OVERSAMPLE ANOMALIES
# ==========================================

from sklearn.utils import resample

print("\n" + "="*50)
print("OVERSAMPLING ANOMALIES")
print("="*50)

anomaly_indices = np.where(y_sequences == 1)[0]
normal_indices = np.where(y_sequences == 0)[0]

X_anomalies = X_sequences[anomaly_indices]
y_anomalies = y_sequences[anomaly_indices]

X_normals = X_sequences[normal_indices]
y_normals = y_sequences[normal_indices]

print(f"Before oversampling:")
print(f"  Anomalies: {len(X_anomalies)}")
print(f"  Normals: {len(X_normals)}")

target_anomaly_count = int(len(X_normals) * 0.3)

if len(X_anomalies) < target_anomaly_count:
    X_anomalies_resampled, y_anomalies_resampled = resample(
        X_anomalies,
        y_anomalies,
        replace=True,
        n_samples=target_anomaly_count,
        random_state=42
    )
    
    X_balanced = np.vstack([X_normals, X_anomalies_resampled])
    y_balanced = np.hstack([y_normals, y_anomalies_resampled])
    
    print(f"\nAfter oversampling:")
    print(f"  Anomalies: {len(X_anomalies_resampled)}")
    print(f"  Normals: {len(X_normals)}")
    print(f"  Total: {len(X_balanced)}")

from sklearn.utils import shuffle
X_balanced, y_balanced = shuffle(X_balanced, y_balanced, random_state=42)

# ==========================================
# PART 6: TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X_balanced,
    y_balanced,
    test_size=0.2,
    random_state=42,
    stratify=y_balanced
)

print(f"\nTraining Data: {X_train.shape}")
print(f"Testing Data: {X_test.shape}")
print(f"Training Anomalies: {sum(y_train)}")
print(f"Testing Anomalies: {sum(y_test)}")

# ==========================================
# PART 7: COMPUTE CLASS WEIGHTS
# ==========================================

classes = np.unique(y_train)
weights = compute_class_weight(
    class_weight="balanced",
    classes=classes,
    y=y_train
)

class_weights = {
    0: weights[0],
    1: weights[1] * 1.5
}

print(f"\nClass weights: {class_weights}")

# ==========================================
# PART 8: BUILD IMPROVED LSTM MODEL WITH INPUT LAYER
# ==========================================

print("\n" + "="*50)
print("BUILDING IMPROVED LSTM MODEL")
print("="*50)

model = Sequential([
    # Input layer (removes warning)
    Input(shape=(SEQUENCE_LENGTH, X_train.shape[2])),
    
    # Bidirectional LSTM for better context
    Bidirectional(LSTM(64, return_sequences=True)),
    Dropout(0.3),
    
    # Second LSTM layer
    LSTM(32, return_sequences=False),
    Dropout(0.3),
    
    # Dense layers
    Dense(16, activation='relu'),
    Dropout(0.3),
    
    Dense(8, activation='relu'),
    Dropout(0.2),
    
    Dense(1, activation='sigmoid')
])

optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)

model.compile(
    optimizer=optimizer,
    loss='binary_crossentropy',
    metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
)

print(model.summary())

# ==========================================
# PART 9: TRAIN MODEL
# ==========================================

print("\n" + "="*50)
print("TRAINING MODEL")
print("="*50)

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True,
    verbose=1
)

reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=5,
    min_lr=0.00001,
    verbose=1
)

history = model.fit(
    X_train,
    y_train,
    validation_split=0.2,
    epochs=100,
    batch_size=64,
    callbacks=[early_stop, reduce_lr],
    class_weight=class_weights,
    verbose=1
)

# ==========================================
# PART 10: EVALUATE WITH DIFFERENT THRESHOLDS
# ==========================================

print("\n" + "="*50)
print("EVALUATING MODEL WITH DIFFERENT THRESHOLDS")
print("="*50)

# Evaluate on test data
test_loss, test_accuracy, test_precision, test_recall = model.evaluate(X_test, y_test, verbose=0)

print(f"Test Accuracy: {test_accuracy:.4f}")
print(f"Test Precision: {test_precision:.4f}")
print(f"Test Recall: {test_recall:.4f}")
print(f"Test Loss: {test_loss:.4f}")

# Make predictions
y_pred_prob = model.predict(X_test)

# ==========================================
# PART 11: THRESHOLD TUNING (0.7 and 0.8 options)
# ==========================================

from sklearn.metrics import f1_score, precision_score, recall_score

print("\n" + "="*50)
print("THRESHOLD COMPARISON")
print("="*50)

thresholds = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9]
results = []

for threshold in thresholds:
    y_pred = (y_pred_prob > threshold).astype(int)
    
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    results.append({
        'threshold': threshold,
        'precision': precision,
        'recall': recall,
        'f1': f1
    })
    
    print(f"Threshold {threshold:.2f}: Precision={precision:.4f}, Recall={recall:.4f}, F1={f1:.4f}")

# Find best threshold
best_result = max(results, key=lambda x: x['f1'])
best_threshold = best_result['threshold']

print(f"\nBest threshold: {best_threshold:.2f} (F1: {best_result['f1']:.4f})")

# ==========================================
# PART 12: RECOMMENDED THRESHOLDS
# ==========================================

print("\n" + "="*50)
print("RECOMMENDED THRESHOLDS")
print("="*50)

# Try threshold 0.7
y_pred_07 = (y_pred_prob > 0.7).astype(int)
precision_07 = precision_score(y_test, y_pred_07, zero_division=0)
recall_07 = recall_score(y_test, y_pred_07, zero_division=0)
f1_07 = f1_score(y_test, y_pred_07, zero_division=0)

print(f"\nThreshold 0.70:")
print(f"  Precision: {precision_07:.4f}")
print(f"  Recall: {recall_07:.4f}")
print(f"  F1: {f1_07:.4f}")

# Try threshold 0.8
y_pred_08 = (y_pred_prob > 0.8).astype(int)
precision_08 = precision_score(y_test, y_pred_08, zero_division=0)
recall_08 = recall_score(y_test, y_pred_08, zero_division=0)
f1_08 = f1_score(y_test, y_pred_08, zero_division=0)

print(f"\nThreshold 0.80:")
print(f"  Precision: {precision_08:.4f}")
print(f"  Recall: {recall_08:.4f}")
print(f"  F1: {f1_08:.4f}")

# Use best threshold
y_pred = (y_pred_prob > best_threshold).astype(int)

# ==========================================
# PART 13: CLASSIFICATION METRICS
# ==========================================

from sklearn.metrics import classification_report, confusion_matrix

print("\n" + "="*50)
print(f"CLASSIFICATION REPORT (Threshold: {best_threshold:.2f})")
print("="*50)

print(classification_report(y_test, y_pred, target_names=['Normal', 'Anomaly']))

print("\n" + "="*50)
print("CONFUSION MATRIX")
print("="*50)

cm = confusion_matrix(y_test, y_pred)
print(cm)

# ==========================================
# PART 14: SAVE MODEL AND THRESHOLD
# ==========================================

import os
os.makedirs("models", exist_ok=True)

model.save("models/lstm_anomaly_model.keras")
joblib.dump(scaler, "models/lstm_scaler.pkl")
joblib.dump(best_threshold, "models/lstm_threshold.pkl")

print("\n" + "="*50)
print("MODEL SAVED")
print("="*50)
print("Model saved as: models/lstm_anomaly_model.keras")
print("Scaler saved as: models/lstm_scaler.pkl")
print(f"Threshold saved as: models/lstm_threshold.pkl (value: {best_threshold:.2f})")

# ==========================================
# PART 15: PLOT TRAINING HISTORY
# ==========================================

try:
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Accuracy
    axes[0, 0].plot(history.history['accuracy'], label='Training Accuracy')
    axes[0, 0].plot(history.history['val_accuracy'], label='Validation Accuracy')
    axes[0, 0].set_title('Model Accuracy')
    axes[0, 0].set_xlabel('Epoch')
    axes[0, 0].set_ylabel('Accuracy')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Loss
    axes[0, 1].plot(history.history['loss'], label='Training Loss')
    axes[0, 1].plot(history.history['val_loss'], label='Validation Loss')
    axes[0, 1].set_title('Model Loss')
    axes[0, 1].set_xlabel('Epoch')
    axes[0, 1].set_ylabel('Loss')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Precision
    if 'precision' in history.history:
        axes[1, 0].plot(history.history['precision'], label='Training Precision')
        axes[1, 0].plot(history.history['val_precision'], label='Validation Precision')
        axes[1, 0].set_title('Model Precision')
        axes[1, 0].set_xlabel('Epoch')
        axes[1, 0].set_ylabel('Precision')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
    
    # Recall
    if 'recall' in history.history:
        axes[1, 1].plot(history.history['recall'], label='Training Recall')
        axes[1, 1].plot(history.history['val_recall'], label='Validation Recall')
        axes[1, 1].set_title('Model Recall')
        axes[1, 1].set_xlabel('Epoch')
        axes[1, 1].set_ylabel('Recall')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('models/lstm_training_history.png', dpi=150)
    print("\nTraining history plot saved as: models/lstm_training_history.png")
    
except Exception as e:
    print(f"\nCould not save plot: {e}")

# ==========================================
# PART 16: PREDICTION EXAMPLE
# ==========================================

print("\n" + "="*50)
print("PREDICTION EXAMPLE")
print("="*50)

sample_idx = np.random.randint(0, len(X_test))
sample_sequence = X_test[sample_idx:sample_idx+1]
sample_label = y_test[sample_idx]

pred_prob = model.predict(sample_sequence, verbose=0)
pred_class = (pred_prob > best_threshold).astype(int)[0][0]

print(f"True Label: {'Anomaly' if sample_label == 1 else 'Normal'}")
print(f"Predicted: {'Anomaly' if pred_class == 1 else 'Normal'}")
print(f"Confidence: {pred_prob[0][0]:.4f}")
print(f"Threshold used: {best_threshold:.2f}")

print("\n" + "="*50)
print("LSTM TRAINING COMPLETE!")
print("="*50)