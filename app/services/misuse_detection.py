import os
import logging
from openai import OpenAI
from sqlalchemy.orm import Session
from app.models.ad_data import AdData
from app.models.contract import Contract

# Load AI API key
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

client = OpenAI(api_key=CLAUDE_API_KEY)

# Configure logging
logging.basicConfig(level=logging.INFO)

def analyze_content(ad_id: str, db: Session):
    """Check if an ad violates contract terms using AI."""
    ad = db.query(AdData).filter(AdData.ad_id == ad_id).first()
    contracts = db.query(Contract).all()
    
    if not ad or not contracts:
        return "No relevant data found."

    contract_texts = " ".join([c.filename for c in contracts])

    try:
        response = client.completions.create(
            model="claude-3.5",
            prompt=f"Check if this ad violates contract terms:\n\nAd: {ad.content}\n\nContracts: {contract_texts}",
            max_tokens=50
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logging.error(f"AI processing error: {e}")
        return "Error in AI compliance check."

def check_contract_violation(ad_id: str, db: Session):
    """Alternative compliance check (without AI)."""
    ad = db.query(AdData).filter(AdData.ad_id == ad_id).first()
    contracts = db.query(Contract).all()
    
    if not ad or not contracts:
        return "No contract reference found."

    for contract in contracts:
        if contract.filename.lower() in ad.content.lower():
            return "Possible contract violation detected."
    
    return "No violation detected."
