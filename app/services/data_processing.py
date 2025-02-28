from sqlalchemy.orm import Session
from models.ad_data import AdData

def store_ad_data(db: Session, platform: str, ad_id: str, content: str):
    """Save fetched ad data to the database."""
    ad_entry = AdData(platform=platform, ad_id=ad_id, content=content)
    db.add(ad_entry)
    db.commit()
    return ad_entry
