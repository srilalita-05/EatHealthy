from collections import defaultdict
from datetime import datetime, timedelta
from engines.context import get_time_slot


def detect_patterns(meals: list) -> dict:
    """
    Analyze last 7 days of meals.
    Returns: { time_slot: { food_name: count, category_counts: {junk: N, healthy: N} } }
    """
    cutoff = datetime.utcnow() - timedelta(days=7)
    recent = [m for m in meals if m.meal_time >= cutoff]

    slot_data: dict = defaultdict(lambda: {"foods": defaultdict(int), "junk": 0, "healthy": 0})

    for meal in recent:
        slot = get_time_slot(meal.meal_time)
        slot_data[slot]["foods"][meal.food_name] += 1
        slot_data[slot][meal.category.value] += 1

    return slot_data


def get_risk_slots(slot_data: dict) -> list[str]:
    """Return time slots with ≥2 junk meals."""
    return [slot for slot, data in slot_data.items() if data["junk"] >= 2]
