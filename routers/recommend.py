from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from engines.recommendation import get_recommendations
import models, schemas

router = APIRouter(prefix="/recommend", tags=["Recommend"])


@router.get("", response_model=schemas.RecommendationResponse)
def recommend(
    user_id: int = Query(...),
    predicted_food: str = Query(...),
    context: str = Query("work_hours"),
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    options = get_recommendations(predicted_food, user.goal.value, context)

    return schemas.RecommendationResponse(
        predicted_food=predicted_food,
        context=context,
        options=options,
    )
