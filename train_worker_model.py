import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# 1. Load dataset
df = pd.read_csv("worker_data.csv")

# 2. Features matching the worker data
X = df[
    [
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
]

# 3. Target
y = df["risk_level"]

# 4. Categorical columns
categorical_features = ["equipment_status"]
numeric_features = ["temperature", "humidity", "gas_level", "fatigue_score", "ppe_compliance", "working_hours", "hazard_distance", "previous_incidents"]

# 5. Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ]
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
