from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
import models, schemas

router = APIRouter(prefix="/meal", tags=["Meal"])


@router.post("", response_model=schemas.MealResponse, status_code=201)
def log_meal(payload: schemas.MealCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    meal_data = payload.model_dump()
    if not meal_data.get("meal_time"):
        meal_data["meal_time"] = datetime.utcnow()

    meal = models.MealLog(**meal_data)
    db.add(meal)
    db.commit()
    db.refresh(meal)
    return meal


@router.get("/history/{user_id}")
def get_meal_history(user_id: int, limit: int = 20, db: Session = Depends(get_db)):
    meals = (
        db.query(models.MealLog)
        .filter(models.MealLog.user_id == user_id)
        .order_by(models.MealLog.meal_time.desc())
        .limit(limit)
        .all()
    )
    return meals
