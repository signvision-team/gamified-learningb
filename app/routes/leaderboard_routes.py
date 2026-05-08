from fastapi import APIRouter
from app.config.database import get_db_connection

router = APIRouter(prefix="/leaderboard")

@router.get("/")
def leaderboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # returns data as dict

    try:
        # ✅ Fetch top 10 users by XP
        cursor.execute("""
            SELECT id, username, xp, level
            FROM users
            ORDER BY xp DESC
            LIMIT 10
        """)

        users = cursor.fetchall()

        return users

    except Exception as e:
        return {"error": str(e)}

    finally:
        cursor.close()
        conn.close()