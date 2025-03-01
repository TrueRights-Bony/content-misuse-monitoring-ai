from fastapi import APIRouter, Depends
from app.services.misuse_detection import analyze_content
from sqlalchemy.orm import Session
from app.services.misuse_detection import check_contract_violation
from app.models.base import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/check_misuse/")
async def check_misuse(post_id: str):
    result = analyze_content(post_id)
    return {"post_id": post_id, "misuse_detected": result}

@router.get("/monitor/{ad_id}")
async def monitor_ad(ad_id: str, db: Session = Depends(get_db)):
    result = check_contract_violation(ad_id, db)
    return {"ad_id": ad_id, "violation_detected": result}