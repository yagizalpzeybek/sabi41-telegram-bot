import json
import os
from database import supabase

def set_budget(user_id: int, amount: float):
    user_id = str(user_id)

    data = {
        "user_id": user_id,
        "initial_budget" : amount,
        "current_balance" : amount

    }

    supabase.table("budgets").upsert(data).execute()

    return data

def get_balance(user_id: int):
    user_id = str(user_id)

    response = (
        supabase.table("budgets")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]


def spend_money(user_id: int, amount: float):
    user_id = str(user_id)

    budget = get_balance(user_id)

    if budget is None:
        return None

    new_balance = budget["current_balance"] - amount

    (
        supabase.table("budgets")
        .update({"current_balance": new_balance})
        .eq("user_id", user_id)
        .execute()
    )

    budget["current_balance"] = new_balance

    return budget


def reset_budget(user_id: int):
    user_id = str(user_id)

    (
        supabase.table("budgets")
        .delete()
        .eq("user_id", user_id)
        .execute()
    )
