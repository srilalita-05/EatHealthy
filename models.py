from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base


class GoalEnum(str, enum.Enum):
    lose = "lose"
    maintain = "maintain"
    gain = "gain"


class DietPrefEnum(str, enum.Enum):
    veg = "veg"
    non_veg = "non_veg"
    vegan = "vegan"


class CategoryEnum(str, enum.Enum):
    junk = "junk"
    healthy = "healthy"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    weight_kg = Column(Float, nullable=False)
    goal = Column(Enum(GoalEnum), nullable=False, default=GoalEnum.maintain)
    diet_pref = Column(Enum(DietPrefEnum), nullable=False, default=DietPrefEnum.veg)
    created_at = Column(DateTime, default=datetime.utcnow)

    meals = relationship("MealLog", back_populates="user")


class MealLog(Base):
    __tablename__ = "meal_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    food_name = Column(String(200), nullable=False)
    category = Column(Enum(CategoryEnum), nullable=False)
    calories = Column(Integer, nullable=False)
    meal_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    location_tag = Column(String(50), nullable=True, default="home")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="meals")
