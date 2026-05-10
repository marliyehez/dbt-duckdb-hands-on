import polars as pl
from faker import Faker
import random
from datetime import datetime, timedelta
import json
import os

# Initialize Faker
fake = Faker()

# Configuration
NUM_USERS = 100
NUM_LOGS = 2000
START_DATE = datetime(2026, 1, 1)
OUTPUT_DIR = ".storage/sources"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Master Data: Exercises (25 items)
EXERCISES = [
    {"exercise_id": "ex001", "exercise_name": "Weighted Pull-up", "category": "Compound", "muscle_group": "Back"},
    {"exercise_id": "ex002", "exercise_name": "Weighted Dip", "category": "Compound", "muscle_group": "Chest/Triceps"},
    {"exercise_id": "ex003", "exercise_name": "Romanian Deadlift", "category": "Compound", "muscle_group": "Hamstrings"},
    {"exercise_id": "ex004", "exercise_name": "Squat", "category": "Compound", "muscle_group": "Quads"},
    {"exercise_id": "ex005", "exercise_name": "Lateral Raise", "category": "Isolation", "muscle_group": "Shoulders"},
    {"exercise_id": "ex006", "exercise_name": "Bench Press", "category": "Compound", "muscle_group": "Chest"},
    {"exercise_id": "ex007", "exercise_name": "Overhead Press", "category": "Compound", "muscle_group": "Shoulders"},
    {"exercise_id": "ex008", "exercise_name": "Barbell Row", "category": "Compound", "muscle_group": "Back"},
    {"exercise_id": "ex009", "exercise_name": "Deadlift", "category": "Compound", "muscle_group": "Full Body"},
    {"exercise_id": "ex010", "exercise_name": "Leg Press", "category": "Compound", "muscle_group": "Quads"},
    {"exercise_id": "ex011", "exercise_name": "Bicep Curl", "category": "Isolation", "muscle_group": "Arms"},
    {"exercise_id": "ex012", "exercise_name": "Tricep Extension", "category": "Isolation", "muscle_group": "Arms"},
    {"exercise_id": "ex013", "exercise_name": "Leg Curl", "category": "Isolation", "muscle_group": "Hamstrings"},
    {"exercise_id": "ex014", "exercise_name": "Face Pull", "category": "Isolation", "muscle_group": "Rear Delts"},
    {"exercise_id": "ex015", "exercise_name": "Calf Raise", "category": "Isolation", "muscle_group": "Calves"},
    {"exercise_id": "ex016", "exercise_name": "Hammer Curl", "category": "Isolation", "muscle_group": "Arms"},
    {"exercise_id": "ex017", "exercise_name": "Incline DB Press", "category": "Compound", "muscle_group": "Chest"},
    {"exercise_id": "ex018", "exercise_name": "Front Squat", "category": "Compound", "muscle_group": "Quads"},
    {"exercise_id": "ex019", "exercise_name": "Bulgarian Split Squat", "category": "Compound", "muscle_group": "Legs"},
    {"exercise_id": "ex020", "exercise_name": "Cable Crossover", "category": "Isolation", "muscle_group": "Chest"},
    {"exercise_id": "ex021", "exercise_name": "Lat Pulldown", "category": "Compound", "muscle_group": "Back"},
    {"exercise_id": "ex022", "exercise_name": "Preacher Curl", "category": "Isolation", "muscle_group": "Arms"},
    {"exercise_id": "ex023", "exercise_name": "Pec Deck", "category": "Isolation", "muscle_group": "Chest"},
    {"exercise_id": "ex024", "exercise_name": "Lunges", "category": "Compound", "muscle_group": "Legs"},
    {"exercise_id": "ex025", "exercise_name": "Plank", "category": "Isolation", "muscle_group": "Core"}
]

def generate_exercise_csv():
    """Generates the Exercise Master Data CSV for dbt seed"""
    df_exercises = pl.DataFrame(EXERCISES)
    path = f"{OUTPUT_DIR}/exercise_mapping.csv"
    df_exercises.write_csv(path)
    print(f"✅ Generated {len(EXERCISES)} exercises in {path}")

def generate_crm_parquet():
    """Generates User data (CRM) with consistent IDs"""
    users = []
    for i in range(NUM_USERS):
        user_id = f"user_{i:03d}" 
        users.append({
            "user_id": user_id,
            "user_name": fake.name(),
            "email": fake.email(),
            "country": "Indonesia" if random.random() > 0.5 else fake.country(),
            "membership_level": random.choice(["Basic", "Pro"]),
            "is_active": random.choice(['active', 'True', 'False']),
            "created_at": datetime(2026, 1, 1),
            "updated_at": datetime.now()
        })
    
    df_users = pl.DataFrame(users)
    path = f"{OUTPUT_DIR}/crm_users.parquet"
    df_users.write_parquet(path)
    print(f"✅ Generated {NUM_USERS} users in {path}")
    return users

def generate_workout_logs_json(user_list):
    """Generates Workout Logs with random time injection"""
    logs = []
    for _ in range(NUM_LOGS):
        user = random.choice(user_list)
        exercise = random.choice(EXERCISES)
        
        # Inject arbitrary timestamps
        random_days = random.randint(0, 120)
        random_seconds = random.randint(0, 86399) 
        log_time = START_DATE + timedelta(days=random_days, seconds=random_seconds)

        # Realistic weights logic
        if exercise["category"] == "Compound":
            weight = random.randint(20, 120)
        else:
            weight = random.randint(2, 20)
        
        log = {
            "log_id": str(fake.unique.uuid4()),
            "user_id": user["user_id"],
            "exercise_id": exercise["exercise_id"],
            "exercise_name": exercise["exercise_name"],
            "sets": [
                {"reps": random.randint(5, 12), "weight_kg": weight} for _ in range(3)
            ],
            "timestamp": log_time.isoformat()
        }
        logs.append(log)
    
    path = f"{OUTPUT_DIR}/workout_logs.json"
    with open(path, "w") as f:
        json.dump(logs, f, indent=2)
    print(f"✅ Generated {NUM_LOGS} workout logs in {path}")

if __name__ == "__main__":
    generate_exercise_csv()
    user_data = generate_crm_parquet()
    generate_workout_logs_json(user_data)