"""
extract_model_info.py
---------------------
Extracts metadata, pipeline structure, feature importances, classes, 
and hyperparameters from the trained steel_safety_model.pkl file.
"""
import joblib
import pandas as pd
import numpy as np
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. Load the model pickle file
model_file = "steel_safety_model.pkl"
pipeline = joblib.load(model_file)

print("=" * 60)
print(f"  EXTRACTING ML MODEL: {model_file}")
print("=" * 60)

# 2. Extract Pipeline Architecture
print(f"\n1. MODEL PIPELINE STEPS:")
for name, step in pipeline.named_steps.items():
    print(f"   - Step '{name}': {step.__class__.__name__}")

# 3. Extract Classifier Hyperparameters
rf_classifier = pipeline.named_steps['model']
print(f"\n2. RANDOM FOREST HYPERPARAMETERS:")
print(f"   - Number of Trees (n_estimators): {rf_classifier.n_estimators}")
print(f"   - Criterion:                     {rf_classifier.criterion}")
print(f"   - Target Classes:                 {rf_classifier.classes_}")
print(f"   - Random State:                   {rf_classifier.random_state}")

# 4. Extract Preprocessor & Encoded Feature Names
preprocessor = pipeline.named_steps['preprocessing']
feature_names = list(preprocessor.get_feature_names_out())

print(f"\n3. PREPROCESSED FEATURES ({len(feature_names)} TOTAL):")
for i, fname in enumerate(feature_names, 1):
    print(f"   {i:2d}. {fname}")

# 5. Extract Feature Importances
importances = rf_classifier.feature_importances_
feature_importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance (%)': np.round(importances * 100, 2)
}).sort_values(by='Importance (%)', ascending=False)

print(f"\n4. FEATURE IMPORTANCE RANKING:")
print(feature_importance_df.to_string(index=False))

print(f"\n" + "=" * 60)
print("  EXTRACTION COMPLETE")
print("=" * 60)
