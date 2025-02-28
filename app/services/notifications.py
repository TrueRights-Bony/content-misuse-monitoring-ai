import requests
import os

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_alert(message: str):
    payload = {"text": message}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    return response.status_code
