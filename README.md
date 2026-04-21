# RAEI – Real-Time Adaptive Eating Intelligence 🍏🧠

RAEI is a full-stack web application designed to predict a user's next meal based on past eating patterns and to intervene in real-time with healthier alternatives or improved portion suggestions. It uses an AI-inspired behavior and context engine to analyze habits and context (time of day, location) and nudges users toward better choices using a modern, interactive 3D UI.

## ✨ Core Features
- **Behavior Pattern Detection:** Analyzes the last 7 days to find specific patterns (e.g., late-night snacking, high junk food ratio).
- **Context Awareness:** Classifies meal timing (morning, work hours, late-night) to understand *why* and *when* you eat.
- **Micro-Interventions:** If the engine predicts an unhealthy food choice at a certain time slot, it intercepts with better suggestions (Healthier Alternative, Improved Version, Quick Prep).
- **Interactive 3D Experience (Three.js):** 
  - Floating 3D Food Orb that reacts (red for junk predictions, green for healthy).
  - 3D ring charts for the dashboard dashboard insights.
  - Interactive swipe cards wrapped in a slick glassmorphic UI.

---

## 🛠 Tech Stack
**Frontend:**
- React (Vite)
- Tailwind CSS v4 (Glassmorphism + Dark Mode)
- `@react-three/fiber` & `@react-three/drei` (3D rendering)
- Framer Motion & React Spring (Fluid animations)
- `@use-gesture/react` (Swipe interactions)

**Backend:**
- FastAPI (High-performance API)
- PostgreSQL (Database)
- SQLAlchemy + Alembic (ORM & Migrations)
- Pydantic (Validations)

---

## 🚀 How to Run Locally

### 1. Prerequisites
- **Python 3.10+**
- **Node.js 18+**
- **PostgreSQL** running on default port `5432` with a database named `raei_db` (or adapt the `.env`). Minimum password needed, e.g., user `postgres`, password `password`.

### 2. Backend Setup
1. Open a terminal and navigate to the `backend` directory.
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment.
   ```bash
   # Windows
   py -m venv venv
   .\venv\Scripts\Activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies.
   ```bash
   pip install -r requirements.txt
   ```
4. Define your Database URL inside `backend/.env` (see `.env.example`).
5. Seed the database with dummy user data and habits. (This creates tables automatically).
   ```bash
   python seed_data.py
   ```
6. Start the FastAPI development server.
   ```bash
   uvicorn main:app --reload
   ```
   > 📌 The backend will be running at [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI).

### 3. Frontend Setup
1. Open a *second* terminal and navigate to the `frontend` directory.
   ```bash
   cd frontend
   ```
2. Install npm packages.
   ```bash
   npm install
   ```
3. Start the Vite development server.
   ```bash
   npm run dev
   ```
   > 📌 The web app will be running at [http://localhost:5173](http://localhost:5173).

---

## 🧩 Project Structure
```text
Hack2Skill/
├── backend/
│   ├── main.py              # FastAPI app & routing
│   ├── database.py          # PostgreSQL + SQLAlchemy config
│   ├── models.py            # DB Schema (User, MealLog)
│   ├── schemas.py           # Pydantic Schemas
│   ├── seed_data.py         # Dummy 14-day history script
│   ├── engines/             # Core Logic
│   │   ├── behavior.py      # Pattern detection algorithms
│   │   ├── context.py       # Time + contextual mapping
│   │   ├── prediction.py    # Predicts next meal
│   │   └── recommendation.py# Recommends alternatives
│   └── routers/             # API Endpoints
└── frontend/
    ├── src/
    │   ├── api/client.js    # Axios wrapper
    │   ├── hooks/useRAEI.js # Dedicated data fetching hooks
    │   ├── pages/           # Home, LogMeal, Dashboard
    │   └── components/      # UI & 3D elements (FoodOrb, RingChart)
    ├── index.css            # Tailwind + Custom overrides
    └── tailwind.config.js
```

---

## 📡 API Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/user` | Register a new user |
| `POST` | `/meal` | Log a food entry |
| `GET` | `/predict` | Predict what the user will eat next based on time slot |
| `GET` | `/recommend` | Nudge the user with 3 healthy alternatives to the predicted food |
| `GET` | `/insights` | Calculate streaks, junk ratio, and at-risk time slots |

---

## 🎨 UI Interactions Breakdown
- **Ambient Glowing Orb:** Located on the Home page. It pulls your predicted next meal from the API. If the prediction is classified as `junk`, the orb glows red and pulses. Clicking it deploys intervention cards.
- **Intervention Cards:** A 3D layered cascade of cards giving you options to replace your bad habit.
- **Physical Swipes:** Drag a recommendation card right to *Accept* it, creating a positive reinforcement loop.
- **Dashboard Ring:** A React Three Fiber generated torus tracking your healthy vs. junk percentage in full 3D space. 

*Built for Hack2Skill.*
