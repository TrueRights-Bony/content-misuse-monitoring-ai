import anthropic
import os
from dotenv import load_dotenv
import datetime


# Load API Key
load_dotenv()
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

def get_available_models():
    """Fetch and return available Claude models"""
    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
    
    try:
        models = client.models.list()
        return models  # Returns the model list as JSON
    except Exception as e:
        return {"error": str(e)}


def get_latest_claude_model():
    """Fetch the latest available Claude model dynamically from Anthropic API."""
    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

    try:
        response = client.models.list()

        # 🔍 Debug: Print response type and content
        #print(f"Claude Model List Response Type: {type(response)}")
        #print(f"Claude Model List Response: {response}")

        # Extract data correctly from SyncPage[ModelInfo]
        models = response.data  # `data` is a list of `ModelInfo` objects

        if not models:
            raise ValueError("No Claude models found in API response.")

        # Sort models by `created_at` to get the latest model
        latest_model = max(models, key=lambda x: x.created_at)

        return latest_model.id  # ✅ Correctly return latest model ID

    except Exception as e:
        raise RuntimeError(f"Failed to fetch latest Claude model: {str(e)}")