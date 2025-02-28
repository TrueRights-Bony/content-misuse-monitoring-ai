from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.models.base import Base

class SocialPosts(Base):
    __tablename__ = "social_posts"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, nullable=False)  # TikTok, Facebook, Instagram
    post_id = Column(String, unique=True, nullable=False)
    creator_id = Column(String, nullable=False)
    content = Column(String, nullable=False)
    detected_misuse = Column(String, default="unknown")  # flagged, clean
    checked_at = Column(DateTime, default=datetime.utcnow)
