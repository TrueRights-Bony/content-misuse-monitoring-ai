from fastapi import APIRouter
from app.services.misuse_detection import analyze_content

router = APIRouter()

@router.get("/check_misuse/")
async def check_misuse(post_id: str):
    result = analyze_content(post_id)
    return {"post_id": post_id, "misuse_detected": result}
