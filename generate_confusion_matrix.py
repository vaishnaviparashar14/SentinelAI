import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay

# Your confusion matrix values
cm = np.array([
    [1344, 60],
    [5, 416]
])

# Labels
labels = ["Normal", "Attack"]

# Create figure
fig, ax = plt.subplots(figsize=(6, 5))

# Plot confusion matrix
disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=labels
)

disp.plot(
    cmap="Blues",
    values_format="d",
    colorbar=False,
    ax=ax
)

plt.title("Confusion Matrix - Bidirectional LSTM", fontsize=14)
plt.xlabel("Predicted Label")
plt.ylabel("True Label")

plt.tight_layout()

# Save image
plt.savefig("confusion_matrix.png", dpi=300)

plt.show()

print("Confusion matrix saved as confusion_matrix.png")