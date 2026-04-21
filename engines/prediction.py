from datetime import datetime
from engines.behavior import detect_patterns
from engines.context import get_time_slot


def predict_next_meal(meals: list, current_time: datetime) -> dict:
    """
    Rule: most frequently eaten food in the current time slot = predicted next meal.
    Returns: { predicted_food, category, confidence, time_slot }
    """
    slot = get_time_slot(current_time)
    slot_data = detect_patterns(meals)

    if slot not in slot_data or not slot_data[slot]["foods"]:
        return {
            "predicted_food": "Unknown",
            "category": "unknown",
            "confidence": 0.0,
            "time_slot": slot,
        }

    foods = slot_data[slot]["foods"]
    top_food = max(foods, key=foods.get)
    total = sum(foods.values())
    confidence = round(foods[top_food] / total, 2)

    # Find category for top food from recent meals
    category = "unknown"
    for meal in meals:
        if meal.food_name == top_food:
            category = meal.category.value
            break

    return {
        "predicted_food": top_food,
        "category": category,
        "confidence": confidence,
        "time_slot": slot,
    }
