from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import (
    user_routes,
    lesson_routes,
    leaderboard_routes,
    session_routes,
    gamification_routes,
    learning_routes
)

app = FastAPI()

# Static files
app.mount("/media", StaticFiles(directory="media"), name="media")

# Routes
app.include_router(user_routes.router, prefix="/user")
app.include_router(lesson_routes.router, prefix="/lesson")
app.include_router(leaderboard_routes.router, prefix="/leaderboard")
app.include_router(session_routes.router, prefix="/session")
app.include_router(gamification_routes.router, prefix="/game")
app.include_router(learning_routes.router, prefix="/learning")


@app.get("/")
def root():
    return {"message": "Backend running 🚀"}