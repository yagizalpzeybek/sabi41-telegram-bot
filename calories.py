import json
import os 

CALORIES_FILE = "calories.json"


def load_calories():
    if not os.path.exists(CALORIES_FILE):
        return{}
    
    with open(CALORIES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
    
def save_calories(calories):
    with open(CALORIES_FILE, "w", encoding="utf-8") as file:
        json.dump(calories, file, indent=4)


calories = load_calories()


def set_calories(user_id: int, amount: float):
    user_id = str(user_id)

    calories[user_id] = {
        "initial_calories": amount,
        "current_calories": amount
    }

    save_calories(calories)
    return calories[user_id]


def get_calories(user_id: int):
    user_id = str(user_id)
    return calories.get(user_id)

def take_calories(user_id: int, amount: float):
    user_id = str(user_id)

    if user_id not in calories:
        return None

    calories[user_id]["current_calories"] -= amount
    save_calories(calories)

    return calories[user_id]

def reset_to_initial_calories(user_id: int):
    user_id = str(user_id)

    if user_id not in calories:
        return None
    
    calories[user_id]["current_calories"] = calories[user_id]["initial_calories"]
    save_calories(calories)

    return calories[user_id]

def reset_calories(user_id: int):
    user_id = str(user_id)

    if user_id in calories:
        del calories[user_id]
        save_calories(calories)

    return None


    
