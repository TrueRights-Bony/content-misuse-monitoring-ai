from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.api.routes import contracts, notifications, facebook_api, tiktok_api, monitoring, claude_ai

app = FastAPI(
    title="Content Misuse Monitoring API",
    description="🚀 API for detecting and monitoring content misuse across social media platforms.",
    version="2.0.0"
)

# Include all API routes
app.include_router(contracts.router, prefix="/contracts", tags=["Contracts"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
app.include_router(facebook_api.router, prefix="/facebook", tags=["Facebook API"])
app.include_router(tiktok_api.router, prefix="/tiktok", tags=["TikTok API"])
app.include_router(monitoring.router, prefix="/monitoring", tags=["Misuse Detection"])
app.include_router(claude_ai.router, prefix="/models", tags=["Claude Models"]) 

@app.get("/", tags=["Health Check"])
def read_root():
    return {"message": "✅ Content Misuse Monitoring API is running!"}
