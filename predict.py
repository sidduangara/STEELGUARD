import sys
import joblib
import json
import pandas as pd
import warnings

# Suppress sklearn warnings
warnings.filterwarnings("ignore", category=UserWarning)

if len(sys.argv) < 10:
    print(json.dumps({"error": "Missing arguments"}))
    sys.exit(1)

try:
    # 9 features
    temperature = float(sys.argv[1])
    humidity = float(sys.argv[2])
    gas_level = float(sys.argv[3])
    fatigue_score = float(sys.argv[4])
    ppe_compliance = float(sys.argv[5])
    working_hours = float(sys.argv[6])
    hazard_distance = float(sys.argv[7])
    previous_incidents = int(float(sys.argv[8]))
    equipment_status = sys.argv[9]
    
    # Load model
    model = joblib.load("steel_safety_model.pkl")
    
    # Create DataFrame for prediction
    df = pd.DataFrame([{
        "temperature": temperature,
        "humidity": humidity,
        "gas_level": gas_level,
        "fatigue_score": fatigue_score,
        "ppe_compliance": ppe_compliance,
        "working_hours": working_hours,
        "hazard_distance": hazard_distance,
        "previous_incidents": previous_incidents,
        "equipment_status": equipment_status
    }])
    
    # Predict
    pred = model.predict(df)[0]
    
    # Return JSON
    print(json.dumps({"predicted_risk_level": pred}))
    
except Exception as e:
    print(json.dumps({"error": str(e)}))
    sys.exit(1)
