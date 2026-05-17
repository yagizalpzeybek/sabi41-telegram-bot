import json
import os
from datetime import datetime

FITNESS_FILE = "fitness.json"

def load_workouts():
    if not os.path.exists(FITNESS_FILE):
        return{}
    
    with open(FITNESS_FILE, "r", encoding = "utf-8") as file:
        return json.load(file)
    

def save_workouts(workouts):
    with open(FITNESS_FILE, "w", encoding="utf-8") as file:
        json.dump(workouts, file, indent=4)

workouts = load_workouts()

def log_workout(user_id: int, exercise: str, sets: int, reps: int, weight: float):
    user_id = str(user_id)
    exercise = exercise.lower().strip()
    volume = sets * reps* weight

    if user_id not in workouts:
        workouts[user_id] = []

    previous = get_last_exercise(user_id, exercise)

    workout = {
        "exercise" : exercise,
        "sets" : sets,
        "reps" : reps,
        "weight" : weight,
        "volume" : volume,
        "date" : datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    workouts[user_id].append(workout)
    save_workouts(workouts)

    return workout, previous

def get_last_exercise(user_id: int, exercise: str):
    user_id = str(user_id)
    exercise = exercise.lower().strip()

    if user_id not in workouts:
        return None
    
    exercise_logs = [
        workout for workout in workouts[user_id]
        if workout["exercise"] == exercise
    ]

    if not exercise_logs:
        return None
    
    return exercise_logs[-1]

def get_exercise_history(user_id: int, exercise: str, limit: int = 10):
    user_id = str(user_id)
    exercise = exercise.lower().strip()

    if user_id not in workouts:
        return []
    
    exercise_logs = [
        workout for workout in workouts[user_id]
        if workout["exercise"] == exercise
    ]

    return exercise_logs[-limit:]


def get_all_workouts(user_id: int):
    user_id = str(user_id)
    return workouts.get(user_id, [])

