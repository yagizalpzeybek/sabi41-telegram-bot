from database import supabase


def set_calories(user_id: int, amount: float):
    user_id = str(user_id)

    data = {
        "user_id": user_id,
        "initial_calories": amount,
        "current_calories": amount
    }

    supabase.table("calories").upsert(data).execute()

    return data


def get_calories(user_id: int):
    user_id = str(user_id)

    response = (
        supabase.table("calories")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]


def take_calories(user_id: int, amount: float):
    user_id = str(user_id)

    calories = get_calories(user_id)

    if calories is None:
        return None

    new_calories = calories["current_calories"] - amount

    (
        supabase.table("calories")
        .update({"current_calories": new_calories})
        .eq("user_id", user_id)
        .execute()
    )

    calories["current_calories"] = new_calories

    return calories


def reset_to_initial_calories(user_id: int):
    user_id = str(user_id)

    calories = get_calories(user_id)

    if calories is None:
        return None

    new_calories = calories["initial_calories"]

    (
        supabase.table("calories")
        .update({"current_calories": new_calories})
        .eq("user_id", user_id)
        .execute()
    )

    calories["current_calories"] = new_calories

    return calories


def reset_calories(user_id: int):
    user_id = str(user_id)

    (
        supabase.table("calories")
        .delete()
        .eq("user_id", user_id)
        .execute()
    )

    return None