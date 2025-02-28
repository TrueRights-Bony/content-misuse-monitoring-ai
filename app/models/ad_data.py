from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from models.base import Base

class AdData(Base):
    __tablename__ = "ad_data"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, nullable=False)  # Facebook, TikTok
    ad_id = Column(String, unique=True, nullable=False)
    content = Column(String, nullable=False)
    posted_at = Column(DateTime, default=datetime.utcnow)
