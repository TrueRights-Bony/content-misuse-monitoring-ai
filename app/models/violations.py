from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.models.base import Base

class Violations(Base):
    __tablename__ = "violations"

    id = Column(Integer, primary_key=True, index=True)
    ad_id = Column(String, ForeignKey("ad_data.ad_id"), nullable=False)
    violation_reason = Column(String, nullable=False)  # AI reason for misuse
    detected_at = Column(DateTime, default=datetime.utcnow)
