import requests
import os
import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.base import SessionLocal
from app.models.ad_data import AdData

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Load API keys from environment variables
TIKTOK_ACCESS_TOKEN = os.getenv("TIKTOK_ACCESS_TOKEN")
TIKTOK_API_URL = "https://business-api.tiktok.com/open_api/v1.3/ad/"

# Configure logging
logging.basicConfig(level=logging.INFO)

def get_tiktok_ads(ad_account_id: str):
    """Fetch paid ads from TikTok Business API."""
    url = f"{TIKTOK_API_URL}ad_list/"
    headers = {"Authorization": f"Bearer {TIKTOK_ACCESS_TOKEN}"}
    params = {"advertiser_id": ad_account_id}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json().get("data", {}).get("list", [])
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching TikTok ads: {e}")
        return []

@router.get("/tiktok/ads/{ad_account_id}")
async def fetch_tiktok_ads(ad_account_id: str):
    ads = get_tiktok_ads(ad_account_id)
    return {"ad_account_id": ad_account_id, "ads": ads}

@router.get("/ads")
async def list_tiktok_ads(db: Session = Depends(get_db)):
    ads = db.query(AdData).filter(AdData.platform == "TikTok").all()
    return {"ads": [{"id": a.id, "content": a.content} for a in ads]}
