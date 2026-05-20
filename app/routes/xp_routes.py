from fastapi import APIRouter
from app.config.database import get_db_connection

router = APIRouter()

@router.post("/add-xp/{user_id}")
def add_xp(user_id: int, earned_xp: int):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET xp = xp + %s
        WHERE id = %s
    """, (earned_xp, user_id))

    conn.commit()

    return {
        "message": "XP added successfully",
        "xp_added": earned_xp
    }