from fastapi import APIRouter, HTTPException
from app.services.gamification_service import process_prediction
from app.config.database import get_db_connection

router = APIRouter(prefix="/session")

@router.post("/submit-prediction")
def submit_prediction(data: dict):
    try:
        # ✅ 1. Validate input
        user_id = data.get("user_id")
        expected_sign = data.get("expected_sign")
        detected_sign = data.get("detected_sign")
        confidence = data.get("confidence", 0)

        if not user_id or not expected_sign or not detected_sign:
            raise HTTPException(status_code=400, detail="Missing required fields")

        # ✅ 2. Process gamification (XP, level, streak, badges)
        result = process_prediction({
            "user_id": user_id,
            "expected_sign": expected_sign,
            "detected_sign": detected_sign,
            "confidence": confidence
        })

        # result contains:
        # xp_gained, new_xp, level, streak, badges, is_correct

        # ✅ 3. Save session in DB
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO sessions 
            (user_id, sign_name, is_correct, confidence, xp_earned)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            user_id,
            expected_sign,
            result["is_correct"],
            confidence,
            result["xp_gained"]
        ))

        conn.commit()

        cursor.close()
        conn.close()

        # ✅ 4. Return response to frontend
        return {
            "message": "Prediction processed successfully",
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))