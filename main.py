from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import user, meal, predict, recommend, insights

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RAEI – Real-Time Adaptive Eating Intelligence",
    description="Predict user's next meal and intervene with smarter choices in real time.",
    version="1.0.0",
)

# CORS – allow React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(user.router)
app.include_router(meal.router)
app.include_router(predict.router)
app.include_router(recommend.router)
app.include_router(insights.router)


@app.get("/", tags=["Health"])
def root():
    return {
        "status": "ok",
        "app": "RAEI",
        "docs": "/docs",
    }
