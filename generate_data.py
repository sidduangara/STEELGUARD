import pandas as pd
import numpy as np
import random
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

random.seed(42)
np.random.seed(42)

# Worker names pool
first_names = [
    "Priya", "Kavita", "Ganesh", "Suresh", "Ravi", "Amit", "Deepak", "Rajesh",
    "Vikram", "Anil", "Manoj", "Sanjay", "Ramesh", "Ashok", "Vinod", "Prakash",
    "Ajay", "Kiran", "Mohan", "Sunil", "Nitin", "Sachin", "Rahul", "Rohit",
    "Arjun", "Bharat", "Chandan", "Dilip", "Gaurav", "Harish", "Jagdish",
    "Kamal", "Lakshmi", "Meena", "Nirmala", "Pooja", "Rekha", "Savita",
    "Tanuja", "Uma", "Vandana", "Yogesh", "Zeenat", "Anand", "Balaji",
    "Chitra", "Dinesh", "Gopal", "Hemant", "Indira", "Jaya", "Krishna",
    "Leela", "Mukesh", "Naresh", "Omkar", "Pankaj", "Raghav", "Shanti", "Tushar"
]
last_names = [
    "Singh", "Menon", "Yadav", "Gupta", "Sharma", "Patel", "Kumar", "Reddy",
    "Verma", "Joshi", "Mishra", "Chauhan", "Thakur", "Pillai", "Nair", "Das",
    "Roy", "Bhat", "Patil", "Kulkarni", "Deshmukh", "Jadhav", "More", "Pawar",
    "Shinde", "Gaikwad", "Chavan", "Sawant", "Bhosale", "Mane"
]

departments = ["Blast Furnace", "Rolling Mill", "Casting", "Crane Operations",
               "Storage", "Coke Oven", "Steel Melting Shop", "Maintenance",
               "Quality Control", "Logistics"]

job_roles = {
    "Blast Furnace": ["Furnace Operator", "Furnace Helper", "Slag Handler"],
    "Rolling Mill": ["Rolling Mill Operator", "Mill Helper", "Roll Turner"],
    "Casting": ["Casting Operator", "Ladle Operator", "Mould Handler"],
    "Crane Operations": ["Crane Operator", "Rigger", "Signal Man"],
    "Storage": ["Warehouse Handler", "Forklift Operator", "Material Checker"],
    "Coke Oven": ["Coke Oven Operator", "Oven Helper", "Gas Handler"],
    "Steel Melting Shop": ["SMS Operator", "Melter", "Tapper"],
    "Maintenance": ["Fitter", "Electrician", "Welder"],
    "Quality Control": ["QC Inspector", "Lab Technician", "Sampler"],
    "Logistics": ["Driver", "Loader", "Dispatcher"]
}

zones = {
    "Blast Furnace": "Blast Furnace",
    "Rolling Mill": "Rolling Mill",
    "Casting": "Casting Bay",
    "Crane Operations": "Crane Area",
    "Storage": "Storage Area",
    "Coke Oven": "Coke Oven",
    "Steel Melting Shop": "SMS Area",
    "Maintenance": "Maintenance Bay",
    "Quality Control": "QC Lab",
    "Logistics": "Loading Yard"
}

shifts = ["Morning", "Afternoon", "Night"]
weather_options = ["Clear", "Hot", "Rainy", "Humid", "Windy"]
hazard_types_high = ["Gas Leak", "Fire Hazard", "Equipment Failure", "Structural Risk",
                     "Chemical Spill", "Multiple Hazards", "Explosion Risk"]
hazard_types_medium = ["Heat Stress", "Noise Hazard", "Slip Hazard", "Minor Gas Leak",
                       "Equipment Wear", "Dust Exposure"]
equipment_statuses = ["Normal", "Needs Maintenance", "Malfunction"]

rows = []
worker_id = 2001  # Start after existing W1001-W1150

# Target: 800 total rows -> ~270 LOW, ~270 MEDIUM, ~260 HIGH (balanced)
targets = {
    "LOW": 270,
    "MEDIUM": 270,
    "HIGH": 260
}

for risk_level, count in targets.items():
    for _ in range(count):
        dept = random.choice(departments)
        role = random.choice(job_roles[dept])
        zone = zones[dept]
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        age = random.randint(20, 58)
        exp = round(random.uniform(0.5, min(age - 18, 35)), 1)
        shift = random.choice(shifts)
        weather = random.choice(weather_options)

        if risk_level == "HIGH":
            temperature = round(np.random.uniform(40, 55), 1)
            humidity = round(np.random.uniform(60, 90), 1)
            gas_level = round(np.random.uniform(18, 40), 1)
            noise_level = round(np.random.uniform(85, 110), 1)
            fatigue_score = random.randint(7, 10)
            ppe_compliance = round(np.random.uniform(0.1, 0.55), 2)
            working_hours = round(np.random.uniform(10, 16), 1)
            hazard_distance = round(np.random.uniform(0.5, 5), 1)
            previous_incidents = random.randint(2, 6)
            equipment_status = random.choices(
                ["Malfunction", "Needs Maintenance", "Normal"],
                weights=[0.6, 0.3, 0.1]
            )[0]
            heat_stress = random.choices(["Yes", "No"], weights=[0.75, 0.25])[0]
            risk_score = random.randint(70, 100)
            hazard_type = random.choice(hazard_types_high)

        elif risk_level == "MEDIUM":
            temperature = round(np.random.uniform(32, 45), 1)
            humidity = round(np.random.uniform(45, 72), 1)
            gas_level = round(np.random.uniform(8, 22), 1)
            noise_level = round(np.random.uniform(70, 92), 1)
            fatigue_score = random.randint(4, 7)
            ppe_compliance = round(np.random.uniform(0.5, 0.8), 2)
            working_hours = round(np.random.uniform(7, 11), 1)
            hazard_distance = round(np.random.uniform(4, 12), 1)
            previous_incidents = random.randint(0, 3)
            equipment_status = random.choices(
                ["Needs Maintenance", "Normal", "Malfunction"],
                weights=[0.5, 0.35, 0.15]
            )[0]
            heat_stress = random.choices(["Yes", "No"], weights=[0.4, 0.6])[0]
            risk_score = random.randint(40, 69)
            hazard_type = random.choice(hazard_types_medium + ["None"])

        else:  # LOW
            temperature = round(np.random.uniform(22, 35), 1)
            humidity = round(np.random.uniform(30, 58), 1)
            gas_level = round(np.random.uniform(0, 10), 1)
            noise_level = round(np.random.uniform(50, 75), 1)
            fatigue_score = random.randint(1, 4)
            ppe_compliance = round(np.random.uniform(0.75, 1.0), 2)
            working_hours = round(np.random.uniform(4, 8), 1)
            hazard_distance = round(np.random.uniform(10, 30), 1)
            previous_incidents = random.randint(0, 1)
            equipment_status = random.choices(
                ["Normal", "Needs Maintenance", "Malfunction"],
                weights=[0.75, 0.2, 0.05]
            )[0]
            heat_stress = random.choices(["No", "Yes"], weights=[0.9, 0.1])[0]
            risk_score = random.randint(10, 39)
            hazard_type = random.choices(["None", "Noise Hazard"], weights=[0.85, 0.15])[0]

        rows.append({
            "worker_id": f"W{worker_id}",
            "worker_name": name,
            "age": age,
            "experience_years": exp,
            "department": dept,
            "job_role": role,
            "shift": shift,
            "zone": zone,
            "temperature": temperature,
            "humidity": humidity,
            "gas_level": gas_level,
            "noise_level": noise_level,
            "fatigue_score": fatigue_score,
            "ppe_compliance": ppe_compliance,
            "working_hours": working_hours,
            "hazard_distance": hazard_distance,
            "previous_incidents": previous_incidents,
            "equipment_status": equipment_status,
            "weather": weather,
            "heat_stress": heat_stress,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "hazard_type": hazard_type
        })
        worker_id += 1

# Shuffle the rows
random.shuffle(rows)
df_new = pd.DataFrame(rows)

# Load existing data and combine
df_old = pd.read_csv("worker_data.csv")
df_combined = pd.concat([df_old, df_new], ignore_index=True)

# Save
df_combined.to_csv("worker_data.csv", index=False)

print("=" * 60)
print("   Dataset Generation Complete!")
print("=" * 60)
print(f"\n   Old dataset:      {len(df_old)} rows")
print(f"   New rows added:   {len(df_new)} rows")
print(f"   Total dataset:    {len(df_combined)} rows")
print(f"\n   Distribution:")
print("-" * 40)
for label in sorted(df_combined["risk_level"].unique()):
    count = (df_combined["risk_level"] == label).sum()
    pct = count / len(df_combined) * 100
    print(f"   {label:10s} -> {count:4d} samples ({pct:.1f}%)")
print(f"\n   Saved to: worker_data.csv")
