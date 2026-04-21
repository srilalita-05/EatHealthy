from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import get_db
from engines.behavior import detect_patterns, get_risk_slots
import models, schemas

router = APIRouter(prefix="/insights", tags=["Insights"])


@router.get("", response_model=schemas.InsightResponse)
def get_insights(user_id: int = Query(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    meals = db.query(models.MealLog).filter(models.MealLog.user_id == user_id).all()

    total = len(meals)
    junk = sum(1 for m in meals if m.category.value == "junk")
    healthy = total - junk

    slot_data = detect_patterns(meals)
    risk_slots = get_risk_slots(slot_data)

    # Weekly calorie sum (last 7 days)
    cutoff = datetime.utcnow() - timedelta(days=7)
    weekly_cals = sum(m.calories for m in meals if m.meal_time >= cutoff)

    # Streak: consecutive days with ≥1 healthy meal
    streak = _calculate_healthy_streak(meals)

    return schemas.InsightResponse(
        total_meals=total,
        junk_count=junk,
        healthy_count=healthy,
        junk_ratio=round(junk / total, 2) if total else 0.0,
        healthy_ratio=round(healthy / total, 2) if total else 0.0,
        risk_time_slots=risk_slots,
        current_streak_days=streak,
        weekly_calories=weekly_cals,
    )


def _calculate_healthy_streak(meals: list) -> int:
    if not meals:
        return 0

    # Get unique dates with at least one healthy meal
    healthy_days = set()
    for m in meals:
        if m.category.value == "healthy":
            healthy_days.add(m.meal_time.date())

    streak = 0
    today = datetime.utcnow().date()
    check = today

    while check in healthy_days:
        streak += 1
        check -= timedelta(days=1)

    return streak
