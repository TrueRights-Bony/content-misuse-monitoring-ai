import os
from openai import OpenAI
from sqlalchemy.orm import Session
from models.ad_data import AdData
from models.contract import Contract

# Load API key
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

def check_contract_violation(ad_id: str, db: Session):
    """Check if an ad violates contract terms."""
    ad = db.query(AdData).filter(AdData.ad_id == ad_id).first()
    contracts = db.query(Contract).all()
    
    if not ad or not contracts:
        return "No relevant data"

    # Prepare contract text for comparison
    contract_texts = " ".join([c.filename for c in contracts])

    client = OpenAI(api_key=CLAUDE_API_KEY)
    response = client.completions.create(
        model="claude-3.5",
        prompt=f"Check if the following ad violates any contract terms:\n\nAd Content: {ad.content}\n\nContract Terms: {contract_texts}",
        max_tokens=50
    )

    return response.choices[0].text.strip()
