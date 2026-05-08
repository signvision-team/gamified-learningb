from fastapi import APIRouter, HTTPException
from app.services.learning_service import get_levels, get_level_content

router = APIRouter(prefix="/learning", tags=["Learning"])

# ===============================
# GET ALL LEVELS
# ===============================
@router.get("/levels")
def fetch_levels(user_id: int):
    try:
        return {
            "success": True,
            "levels": get_levels(user_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===============================
# GET LEVEL CONTENT
# ===============================
@router.get("/level/{level_id}")
def fetch_level_content(level_id: int):
    try:
        return {
            "success": True,
            "content": get_level_content(level_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))