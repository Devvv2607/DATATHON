import os
from pathlib import Path

from dotenv import load_dotenv

_ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=_ENV_PATH)

GMAIL_SMTP_USER = os.getenv("GMAIL_SMTP_USER") or os.getenv("EMAIL_USER") or ""
GMAIL_SMTP_APP_PASSWORD = os.getenv("GMAIL_SMTP_APP_PASSWORD") or os.getenv("EMAIL_PASSWORD") or ""
GMAIL_SMTP_HOST = os.getenv("GMAIL_SMTP_HOST") or os.getenv("EMAIL_SMTP_SERVER") or "smtp.gmail.com"

try:
    GMAIL_SMTP_PORT = int(os.getenv("GMAIL_SMTP_PORT") or "587")
except Exception:
    GMAIL_SMTP_PORT = 587

DEFAULT_ALERT_TO_EMAIL = os.getenv("ALERT_TO_EMAIL") or os.getenv("DEFAULT_ALERT_TO_EMAIL") or ""
ALERT_FROM_NAME = os.getenv("ALERT_FROM_NAME") or "TrendLens"
