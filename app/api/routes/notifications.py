from fastapi import APIRouter
from pydantic import BaseModel
from app.services.notifications import send_slack_alert

router = APIRouter()

# Define a request model
class AlertMessage(BaseModel):
    message: str

@router.post("/send_alert/")
async def trigger_alert(alert: AlertMessage):
    status = send_slack_alert(alert.message)
    return {"message": "Alert sent!", "status": status}
