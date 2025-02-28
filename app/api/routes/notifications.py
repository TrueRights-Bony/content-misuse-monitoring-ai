import requests
from app.config.settings import SLACK_WEBHOOK_URL

def send_slack_alert(message: str):
    payload = {"text": message}
    requests.post(SLACK_WEBHOOK_URL, json=payload)
