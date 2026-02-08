from fastapi import APIRouter
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool

from .service import EmailNotificationService
from . import config


router = APIRouter(prefix="/api/notifications", tags=["Notifications"])
service = EmailNotificationService()


class SendTestEmailRequest(BaseModel):
    to_email: str | None = None
    subject: str = "Test Email"
    body: str = "This is a test notification from TrendLens."


@router.post("/email/test")
async def send_test_email(request: SendTestEmailRequest):
    to_email = request.to_email or config.DEFAULT_ALERT_TO_EMAIL
    result = await run_in_threadpool(
        service.send_email,
        to_email=to_email,
        subject=request.subject,
        body=request.body,
    )
    return {"success": True, "to_email": to_email, "result": result}
