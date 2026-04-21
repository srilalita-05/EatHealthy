from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class GoalEnum(str, Enum):
    lose = "lose"
    maintain = "maintain"
    gain = "gain"


class DietPrefEnum(str, Enum):
    veg = "veg"
    non_veg = "non_veg"
    vegan = "vegan"


class CategoryEnum(str, Enum):
    junk = "junk"
    healthy = "healthy"


# ── User schemas ──────────────────────────────────────────────
class UserCreate(BaseModel):
    name: str
    age: int
    weight_kg: float
    goal: GoalEnum = GoalEnum.maintain
    diet_pref: DietPrefEnum = DietPrefEnum.veg


class UserResponse(UserCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ── Meal schemas ──────────────────────────────────────────────
class MealCreate(BaseModel):
    user_id: int
    food_name: str
    category: CategoryEnum
    calories: int
    meal_time: Optional[datetime] = None
    location_tag: Optional[str] = "home"


class MealResponse(MealCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ── Prediction / Recommendation schemas ───────────────────────
class PredictionResponse(BaseModel):
    predicted_food: str
    category: str
    context_tag: str
    confidence: float
    time_slot: str


class RecommendationOption(BaseModel):
    type: str          # "healthier_alternative" | "improved_version" | "quick_prep"
    name: str
    description: str
    calories_approx: int
    emoji: str


class RecommendationResponse(BaseModel):
    predicted_food: str
    context: str
    options: list[RecommendationOption]


class InsightResponse(BaseModel):
    total_meals: int
    junk_count: int
    healthy_count: int
    junk_ratio: float
    healthy_ratio: float
    risk_time_slots: list[str]
    current_streak_days: int
    weekly_calories: int
