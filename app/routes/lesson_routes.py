from fastapi import APIRouter
from app.services.gamification_service import process_prediction
from app.services.ai_service import detect_gesture
from app.config.database import get_db_connection

router = APIRouter(prefix="/lesson")


@router.post("/submit")
def submit(data: dict):

    user_id = data["user_id"]
    expected_sign = data["expected_sign"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ✅ Get user
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    if not user:
        return {"error": "User not found"}

    # ✅ AI prediction
    detected = detect_gesture(data.get("image"))

    # =========================================
    # ✅ CALL GAMIFICATION ENGINE (ONLY ONCE)
    # =========================================
    result = process_prediction({
        "user_id": user_id,
        "sign_name": expected_sign,
        "predicted": detected,
        "confidence": data.get("confidence", 0.8)
    })

    # result already contains xp + correctness

    return {
        "detected": detected,
        "correct": result["correct"],
        "xp_gained": result["xp_earned"]
    }