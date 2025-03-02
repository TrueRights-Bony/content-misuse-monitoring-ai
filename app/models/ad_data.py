from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.models.base import engine, Base

class AdData(Base):
    __tablename__ = "ad_data"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, nullable=False)  # Facebook, TikTok
    ad_id = Column(String, unique=True, nullable=False)
    ad_type = Column(String, nullable=False)  # organic / paid
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)