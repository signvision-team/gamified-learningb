from fastapi import APIRouter
from app.config.database import get_db_connection

router = APIRouter(prefix="/user")

@router.post("/create")
def create_user(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (username, xp, level, streak, badges)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data["username"],
        0,
        1,
        0,
        "[]"
    ))

    conn.commit()

    user_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return {
        "message": "User created",
        "user_id": user_id
    }