import pandas as pd
import joblib
import numpy as np
import sys
import io
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("   SteelGuard ML Model - Test & Accuracy Report")
print("=" * 60)

# 1. Load the trained model
model = joblib.load("steel_safety_model.pkl")
print("\n[OK] Model loaded: steel_safety_model.pkl")

# 2. Load the dataset
df = pd.read_csv("worker_data.csv")
print(f"[OK] Dataset loaded: {len(df)} rows")

# 3. Features
features = [
    "temperature", "humidity", "gas_level", "fatigue_score",
    "ppe_compliance", "working_hours", "hazard_distance",
    "previous_incidents", "equipment_status"
]
X = df[features]
y = df["risk_level"]

print(f"\n[DATA] Dataset Distribution:")
print("-" * 40)
for label in sorted(y.unique()):
    count = (y == label).sum()
    pct = count / len(y) * 100
    print(f"   {label:10s} -> {count:4d} samples ({pct:.1f}%)")

# 4. Split same way as training (80/20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n   Training set: {len(X_train)} samples")
print(f"   Test set:     {len(X_test)} samples")

# 5. Predictions on test set
y_pred = model.predict(X_test)

# 6. Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"\n{'=' * 60}")
print(f"   >>> MODEL ACCURACY: {accuracy * 100:.2f}% <<<")
print(f"{'=' * 60}")

# 7. Classification Report (Precision, Recall, F1-Score)
print(f"\n[REPORT] Classification Report:")
print("-" * 60)
print(classification_report(y_test, y_pred, zero_division=0))

# 8. Confusion Matrix
print(f"[MATRIX] Confusion Matrix:")
print("-" * 40)
labels = sorted(y.unique())
cm = confusion_matrix(y_test, y_pred, labels=labels)
# Header
print(f"{'Predicted ->':>15}", end="")
for lbl in labels:
    print(f" {lbl:>8}", end="")
print("\n" + " " * 15 + "-" * (9 * len(labels)))
# Rows
for i, lbl in enumerate(labels):
    print(f"Actual {lbl:>8} |", end="")
    for j in range(len(labels)):
        print(f" {cm[i][j]:>7}", end="")
    print()

# 9. Cross-Validation (5-fold)
print(f"\n[CV] 5-Fold Cross-Validation:")
print("-" * 40)
cv_scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
for i, score in enumerate(cv_scores):
    print(f"   Fold {i+1}: {score * 100:.2f}%")
print(f"\n   >>> Mean CV Accuracy: {cv_scores.mean() * 100:.2f}% (+/-{cv_scores.std() * 100:.2f}%) <<<")

# 10. Test with sample inputs
print(f"\n{'=' * 60}")
print("   [TEST] Sample Predictions")
print(f"{'=' * 60}")

test_cases = [
    {
        "label": "HIGH RISK Worker (hot zone, fatigued, poor PPE)",
        "data": {"temperature": 48, "humidity": 75, "gas_level": 28,
                 "fatigue_score": 9, "ppe_compliance": 0.3,
                 "working_hours": 12, "hazard_distance": 2,
                 "previous_incidents": 3, "equipment_status": "Malfunction"}
    },
    {
        "label": "MEDIUM RISK Worker (moderate conditions)",
        "data": {"temperature": 38, "humidity": 60, "gas_level": 15,
                 "fatigue_score": 5, "ppe_compliance": 0.7,
                 "working_hours": 8, "hazard_distance": 7,
                 "previous_incidents": 1, "equipment_status": "Needs Maintenance"}
    },
    {
        "label": "LOW RISK Worker (safe zone, fresh, good PPE)",
        "data": {"temperature": 28, "humidity": 45, "gas_level": 3,
                 "fatigue_score": 2, "ppe_compliance": 0.95,
                 "working_hours": 4, "hazard_distance": 20,
                 "previous_incidents": 0, "equipment_status": "Normal"}
    },
]

for tc in test_cases:
    input_df = pd.DataFrame([tc["data"]])
    prediction = model.predict(input_df)[0]
    proba = model.predict_proba(input_df)[0]
    classes = model.classes_

    print(f"\n   [*] {tc['label']}")
    print(f"      Input: temp={tc['data']['temperature']}C, gas={tc['data']['gas_level']}, "
          f"fatigue={tc['data']['fatigue_score']}, PPE={tc['data']['ppe_compliance']}, "
          f"equip={tc['data']['equipment_status']}")
    print(f"      >> Prediction: {prediction}")
    print(f"      Confidence: ", end="")
    for cls, prob in zip(classes, proba):
        print(f"{cls}={prob*100:.1f}% ", end="")
    print()

print(f"\n{'=' * 60}")
print("   Test Complete!")
print(f"{'=' * 60}\n")
