from fastapi import APIRouter
from app.services.check_available_models import get_available_models, get_latest_claude_model

router = APIRouter()

@router.get("/check-models/")
async def check_models():
    """API Route to List Available Claude Models"""
    models = get_available_models()
    return models

@router.get("/latest-models/")
async def latest_models():
    """API Route to List Available Claude Models"""
    latest_models = get_latest_claude_model()
    return latest_models
