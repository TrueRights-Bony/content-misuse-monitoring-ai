import requests
import os
import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.base import SessionLocal
from app.models.ad_data import AdData

router = APIRouter()

# Load API keys from environment variables
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
FACEBOOK_GRAPH_API_URL = "https://graph.facebook.com/v18.0"

# Configure logging
logging.basicConfig(level=logging.INFO)

def get_facebook_posts(page_id: str):
    """Fetch organic posts from a Facebook Page using Graph API."""
    url = f"{FACEBOOK_GRAPH_API_URL}/{page_id}/posts"
    params = {"access_token": FACEBOOK_ACCESS_TOKEN}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("data", [])
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching Facebook posts: {e}")
        return []

@router.get("/facebook/posts/{page_id}")
async def fetch_facebook_posts(page_id: str):
    posts = get_facebook_posts(page_id)
    return {"page_id": page_id, "posts": posts}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/posts")
async def list_facebook_posts(db: Session = Depends(get_db)):
    posts = db.query(AdData).filter(AdData.platform == "Facebook").all()
    return {"posts": [{"id": p.id, "content": p.content} for p in posts]}