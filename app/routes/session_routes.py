from fastapi import APIRouter
from app.config.database import get_db_connection

router = APIRouter(prefix="/session")

@router.post("/start")
def start_session(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # ✅ Create a new session (clean start)
        cursor.execute("""
            INSERT INTO sessions (user_id, sign_name, is_correct, confidence, xp_earned)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, None, None, 0.0, 0))

        conn.commit()

        # ✅ Get session ID (IMPORTANT for tracking)
        session_id = cursor.lastrowid

        return {
            "message": "Session started ✅",
            "session_id": session_id
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        cursor.close()
        conn.close()