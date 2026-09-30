import joblib
import pandas as pd
import sys
import io

# Handle Windows UTF-8 stdout encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# 1. Load dataset
data = pd.read_csv("worker_data.csv")

# 2. Select model features and target
features = [
    "temperature",
    "humidity",
    "gas_level",
    "fatigue_score",
    "ppe_compliance",
    "working_hours",
    "hazard_distance",
    "previous_incidents",
    "equipment_status"
]
X = data[features]
y = data["risk_level"]

# 3. Split test data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# 4. Load your trained model
model = joblib.load("steel_safety_model.pkl")

# 5. Predict test data
y_pred = model.predict(X_test)

# 6. Calculate metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average="weighted")
recall = recall_score(y_test, y_pred, average="weighted")
f1 = f1_score(y_test, y_pred, average="weighted")

# 7. Display results
print("\n========== MODEL PERFORMANCE ==========")
print(f"Accuracy  : {accuracy * 100:.2f}%")
print(f"Precision : {precision * 100:.2f}%")
print(f"Recall    : {recall * 100:.2f}%")
print(f"F1 Score  : {f1 * 100:.2f}%")

print("\n========== CLASSIFICATION REPORT ==========")
print(classification_report(y_test, y_pred))

print("\n========== CONFUSION MATRIX ==========")
labels = sorted(y.unique())
print(f"Labels order: {labels}")
print(confusion_matrix(y_test, y_pred, labels=labels))
