import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# 1. Load dataset
df = pd.read_csv("f288dc41-c539-419f-b716-115aa032d3bf.csv")

# 2. Features
X = df[
    [
        "worker_count",
        "avg_temperature",
        "avg_gas_level",
        "avg_risk_score",
        "high_risk_workers",
        "equipment_status"
    ]
]

# 3. Target
y = df["zone_risk_level"]

# 4. Categorical columns
categorical_features = ["equipment_status"]

# 5. Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ],
    remainder="passthrough"
)

# 6. ML model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# 7. Complete pipeline
pipeline = Pipeline(
    steps=[
        ("preprocessing", preprocessor),
        ("model", model)
    ]
)

# 8. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 9. Train
pipeline.fit(X_train, y_train)

# 10. Predict
y_pred = pipeline.predict(X_test)

# 11. Evaluate
accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)
print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

# 12. Save model
joblib.dump(pipeline, "steel_safety_model.pkl")

print("\nModel saved as steel_safety_model.pkl")
