"""
seed_data.py – Populate the database with a sample user and 14 days of meal history.
Run: python seed_data.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from database import SessionLocal, engine, Base
from models import User, MealLog, GoalEnum, DietPrefEnum, CategoryEnum
from datetime import datetime, timedelta
import random

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# ── Create user ────────────────────────────────────────────────
user = db.query(User).filter(User.name == "Priya Sharma").first()
if not user:
    user = User(
        name="Priya Sharma",
        age=28,
        weight_kg=62.5,
        goal=GoalEnum.lose,
        diet_pref=DietPrefEnum.veg,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"✅ Created user: {user.name} (id={user.id})")
else:
    print(f"ℹ️  User already exists: {user.name} (id={user.id})")

# ── Meal patterns (name, category, calories, hour_range) ──────
MEAL_PATTERNS = [
    ("Oats Porridge",   "healthy", 280,  (7, 9)),
    ("Banana Smoothie", "healthy", 220,  (7, 9)),
    ("Pizza",           "junk",    680,  (21, 23)),
    ("Chips",           "junk",    350,  (21, 23)),
    ("Dal Rice",        "healthy", 450,  (12, 14)),
    ("Veggie Wrap",     "healthy", 320,  (12, 14)),
    ("Burger",          "junk",    620,  (21, 23)),
    ("Noodles",         "junk",    540,  (21, 23)),
    ("Greek Yogurt",    "healthy", 180,  (15, 17)),
    ("Ice Cream",       "junk",    400,  (21, 23)),
]

now = datetime.utcnow()
for day_offset in range(14):
    day = now - timedelta(days=day_offset)
    # Pick 3–4 meals per day
    picks = random.sample(MEAL_PATTERNS, k=random.randint(3, 4))
    for food_name, cat, cals, (h_min, h_max) in picks:
        hour = random.randint(h_min, h_max)
        meal_time = day.replace(hour=hour, minute=random.randint(0, 59), second=0, microsecond=0)
        meal = MealLog(
            user_id=user.id,
            food_name=food_name,
            category=CategoryEnum(cat),
            calories=cals + random.randint(-30, 30),
            meal_time=meal_time,
            location_tag="home",
        )
        db.add(meal)

db.commit()
db.close()
print("✅ Seeded 14 days of meal data.")
print(f"\n👤 Test with user_id = {user.id}")
print("🔗  GET http://localhost:8000/predict?user_id=1")
print("🔗  GET http://localhost:8000/recommend?user_id=1&predicted_food=pizza&context=late_night")
print("🔗  GET http://localhost:8000/insights?user_id=1")
