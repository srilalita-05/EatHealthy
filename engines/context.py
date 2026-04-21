from datetime import datetime


def get_context_tag(meal_time: datetime) -> str:
    """Convert meal datetime to a context tag."""
    hour = meal_time.hour

    if 5 <= hour < 9:
        return "morning"
    elif 9 <= hour < 12:
        return "work_hours_morning"
    elif 12 <= hour < 14:
        return "lunch"
    elif 14 <= hour < 18:
        return "work_hours_afternoon"
    elif 18 <= hour < 22:
        return "evening"
    else:
        return "late_night"


def get_time_slot(meal_time: datetime) -> str:
    """Coarser bucket for pattern matching."""
    hour = meal_time.hour
    if 5 <= hour < 11:
        return "morning"
    elif 11 <= hour < 15:
        return "midday"
    elif 15 <= hour < 20:
        return "evening"
    else:
        return "late_night"


def is_high_risk(context_tag: str) -> bool:
    return context_tag in ("late_night", "evening")
