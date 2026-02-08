import os
from pathlib import Path
from dotenv import load_dotenv

_ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=_ENV_PATH)

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
TWILIO_MESSAGING_SERVICE_SID = os.getenv("TWILIO_MESSAGING_SERVICE_SID")

GMAIL_SMTP_HOST = os.getenv("GMAIL_SMTP_HOST") or os.getenv("EMAIL_SMTP_SERVER") or "smtp.gmail.com"
GMAIL_SMTP_PORT = int(os.getenv("GMAIL_SMTP_PORT", "587"))
GMAIL_SMTP_USER = os.getenv("GMAIL_SMTP_USER") or os.getenv("EMAIL_USER")
GMAIL_SMTP_APP_PASSWORD = os.getenv("GMAIL_SMTP_APP_PASSWORD") or os.getenv("EMAIL_PASSWORD")
GMAIL_TO_EMAIL = os.getenv("GMAIL_TO_EMAIL")

TRENT_DECLINE_THRESHOLD = float(os.getenv("TRENT_DECLINE_THRESHOLD", "0"))
ALERT_LOG_PATH = os.getenv("ALERT_LOG_PATH", "alert_events.jsonl")
