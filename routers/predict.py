from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from engines.prediction import predict_next_meal
from engines.context import get_context_tag
import models, schemas

router = APIRouter(prefix="/predict", tags=["Predict"])


@router.get("", response_model=schemas.PredictionResponse)
def predict(
    user_id: int = Query(...),
    current_time: str = Query(None, description="ISO datetime, defaults to now"),
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    now = datetime.fromisoformat(current_time) if current_time else datetime.utcnow()
    meals = db.query(models.MealLog).filter(models.MealLog.user_id == user_id).all()

    result = predict_next_meal(meals, now)
    context_tag = get_context_tag(now)

    return schemas.PredictionResponse(
        predicted_food=result["predicted_food"],
        category=result["category"],
        context_tag=context_tag,
        confidence=result["confidence"],
        time_slot=result["time_slot"],
    )
