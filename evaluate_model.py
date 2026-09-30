"""
evaluate_model.py
-----------------
Loads the EXISTING trained model (steel_safety_model.pkl) and the EXISTING
dataset (worker_data.csv), creates a proper 80/20 train/test split with the
SAME random_state=42 used during training, and computes evaluation metrics
plus feature importance rankings.

Outputs: model_metrics.json  (consumed by the backend API)
"""
import pandas as pd
import joblib
import json
import sys
import io
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 1. Load the EXISTING trained model (do NOT retrain)
model = joblib.load("steel_safety_model.pkl")
print("[OK] Loaded existing model: steel_safety_model.pkl")

# 2. Load the EXISTING dataset
df = pd.read_csv("worker_data.csv")
print(f"[OK] Loaded dataset: {len(df)} rows")

# 3. Same 9 features used during training
features = [
    "temperature",
    "humidity",
    "gas_level",
    "fatigue_score",
    "ppe_compliance",
    "working_hours",
    "hazard_distance",
    "previous_incidents",
    "equipment_status",
]
X = df[features]
y = df["risk_level"]

# 4. Recreate train/test split (80/20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"[OK] Train/test split: {len(X_train)} train, {len(X_test)} test")

# 5. Predict on X_test
y_pred = model.predict(X_test)

# 6. Compute metrics
labels = sorted(y.unique())  # ['HIGH', 'LOW', 'MEDIUM']

accuracy = float(accuracy_score(y_test, y_pred))
precision_macro = float(precision_score(y_test, y_pred, average="macro", zero_division=0))
recall_macro = float(recall_score(y_test, y_pred, average="macro", zero_division=0))
f1_macro = float(f1_score(y_test, y_pred, average="macro", zero_division=0))

per_class = []
precision_per = precision_score(y_test, y_pred, average=None, labels=labels, zero_division=0)
recall_per = recall_score(y_test, y_pred, average=None, labels=labels, zero_division=0)
f1_per = f1_score(y_test, y_pred, average=None, labels=labels, zero_division=0)

for i, label in enumerate(labels):
    support = int((y_test == label).sum())
    per_class.append({
        "label": label,
        "precision": round(float(precision_per[i]), 4),
        "recall": round(float(recall_per[i]), 4),
        "f1Score": round(float(f1_per[i]), 4),
        "support": support,
    })

cm = confusion_matrix(y_test, y_pred, labels=labels)
cm_list = cm.tolist()

# 7. Extract Feature Importances from Pipeline
preprocessor = model.named_steps['preprocessing']
rf_classifier = model.named_steps['model']
raw_feature_names = list(preprocessor.get_feature_names_out())
raw_importances = rf_classifier.feature_importances_

feature_importances = []
for fname, imp in zip(raw_feature_names, raw_importances):
    # Clean up feature name (remove num__ or cat__ prefix)
    clean_name = fname.replace("num__", "").replace("cat__", "")
    feature_importances.append({
        "feature": clean_name,
        "importance": round(float(imp * 100), 2)
    })

feature_importances = sorted(feature_importances, key=lambda x: x['importance'], reverse=True)

# 8. Build output JSON
metrics = {
    "accuracy": round(accuracy, 4),
    "precision": round(precision_macro, 4),
    "recall": round(recall_macro, 4),
    "f1Score": round(f1_macro, 4),
    "datasetSize": len(df),
    "trainSize": len(X_train),
    "testSize": len(X_test),
    "labels": labels,
    "perClass": per_class,
    "confusionMatrix": cm_list,
    "featureImportances": feature_importances,
    "modelFile": "steel_safety_model.pkl",
    "algorithm": "RandomForestClassifier (n_estimators=100)",
    "features": features,
    "evaluatedAt": pd.Timestamp.now().isoformat(),
}

# 9. Save to JSON
with open("model_metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)

print(f"\n[OK] Model evaluation and extraction metrics saved to model_metrics.json")
