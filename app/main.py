from fastapi import FastAPI
from .services import NotificationService
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Predictive Monitoring & Alert Service"}

notification_service = NotificationService()

class TrentPrediction(BaseModel):
    predicted_trent_change: float
    prediction_window_days: int
    confidence: float
    impact: str
    to_phone_number: str
    to_email: str

@app.post("/monitor/trent")
async def monitor_trent(prediction: TrentPrediction):
    result = notification_service.send_trent_decline_alert(
        predicted_trent_change=prediction.predicted_trent_change,
        prediction_window_days=prediction.prediction_window_days,
        confidence=prediction.confidence,
        impact=prediction.impact,
        to_phone_number=prediction.to_phone_number,
        to_email=prediction.to_email,
    )
    return result
