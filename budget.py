import json
import os

BUDGET_FILE = "budget.json"

def load_budgets():
    if not os.path.exists(BUDGET_FILE):
        return{}
    
    with open(BUDGET_FILE, "r", encoding = "utf-8") as file:
        return json.load(file)
    
def save_budgets(budgets):
    with open(BUDGET_FILE, "w", encoding="utf-8") as file:
        json.dump(budgets, file, indent = 4)

budgets = load_budgets()

def set_budget(user_id: int, amount: float):
    user_id = str(user_id)
    budgets[user_id] = amount
    save_budgets(budgets)
    return budgets[user_id]

def get_balance(user_id: int):
    user_id = str(user_id)
    return budgets.get(user_id)

def spend_money(user_id: int, amount: float):
    user_id = str(user_id)

    if user_id not in budgets:
        return None
    
    budgets[user_id] -= amount
    save_budgets(budgets)

    return budgets[user_id]


def reset_budget(user_id: int):
    user_id = str(user_id)

    if user_id in budgets:
        del budgets[user_id]
        save_budgets(budgets)

    return None