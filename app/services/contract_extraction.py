import anthropic
import base64
import os
import json
from app.services.check_available_models import get_latest_claude_model
from dotenv import load_dotenv
import json

# Load API Key
load_dotenv()
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

# Load prompt
PROMPT_FILE = "app/prompts/extract_contract_dates.txt"
with open(PROMPT_FILE, "r") as file:
    CLAUDE_PROMPT = file.read()

def encode_pdf(pdf_path):
    """Encodes a PDF file in base64 for sending to Claude API."""
    with open(pdf_path, "rb") as file:
        return base64.standard_b64encode(file.read()).decode("utf-8")

def format_claude_response(response):
    """Parses and structures Claude's response into the expected JSON format."""
    try:
        # ✅ Extract the text response from Claude (handling TextBlock properly)
        raw_text = response[0].text if isinstance(response, list) and response else ""

        # ✅ Find JSON block inside the text response
        json_start = raw_text.find("{")
        json_end = raw_text.rfind("}") + 1

        if json_start == -1 or json_end == 0:
            raise ValueError("No valid JSON found in Claude's response.")

        # ✅ Parse JSON response from extracted text
        extracted_data = json.loads(raw_text[json_start:json_end])

        # ✅ Return structured response
        return {
            "citations": None,
            "contract_name": extracted_data.get("contract_name", "Unknown Contract"),
            "parties_involved": extracted_data.get("parties_involved", "Not explicitly mentioned"),
            "extracted_data": {
                "startDate": extracted_data["extracted_data"].get("startDate", None),
                "endDate": extracted_data["extracted_data"].get("endDate", None),
                "usageDays": extracted_data["extracted_data"].get("usageDays", None),
                "confidenceScore": extracted_data["extracted_data"].get("confidenceScore", None)
            },
            "analysis": {
                "summary": extracted_data["analysis"].get("summary", "No summary available"),
                "campaign_details": extracted_data["analysis"].get("campaign_details", "No campaign details available"),
                "payment_terms": extracted_data["analysis"].get("payment_terms", "Not specified"),
                "obligations": extracted_data["analysis"].get("obligations", "Not specified"),
                "penalties": extracted_data["analysis"].get("penalties", "Not specified")
            },
            # "raw_response": extracted_data
        }

    except Exception as e:
        return {"error": f"Failed to format response: {str(e)}"}

def extract_contract_dates(pdf_path):
    """Send a contract PDF to Claude and extract usage period details."""
    try:
        pdf_data = encode_pdf(pdf_path)

        # Get latest Claude model dynamically
        latest_model = get_latest_claude_model()

        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

        response = client.messages.create(
            model=latest_model,  
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "document",
                            "source": {
                                "type": "base64",
                                "media_type": "application/pdf",
                                "data": pdf_data
                            },
                            "cache_control": {"type": "ephemeral"}
                        },
                        {
                            "type": "text",
                            "text": CLAUDE_PROMPT
                        }
                    ]
                }
            ],
        )

        # Format and return structured response
        # print(response)
        return format_claude_response(response.content)

    except anthropic.errors.RateLimitError:
        return {"error": "Rate limit exceeded. Try again later or optimize token usage."}
    except Exception as e:
        return {"error": f"Failed to process contract: {str(e)}"}
