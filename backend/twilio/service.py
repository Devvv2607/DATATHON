import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

from . import config


class EmailNotificationService:
    def send_email(self, *, to_email: str, subject: str, body: str) -> dict:
        if not to_email:
            return {"status": "skipped", "reason": "missing_to_email"}
        if not config.GMAIL_SMTP_USER or not config.GMAIL_SMTP_APP_PASSWORD:
            return {"status": "skipped", "reason": "missing_smtp_credentials"}

        msg = MIMEText(body, _charset="utf-8")
        msg["From"] = config.GMAIL_SMTP_USER
        msg["To"] = to_email
        msg["Date"] = formatdate(localtime=False)
        msg["Subject"] = subject

        with smtplib.SMTP(config.GMAIL_SMTP_HOST, config.GMAIL_SMTP_PORT, timeout=20) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(config.GMAIL_SMTP_USER, config.GMAIL_SMTP_APP_PASSWORD)
            server.sendmail(config.GMAIL_SMTP_USER, [to_email], msg.as_string())

        return {"status": "sent"}

    def send_decline_days_alert(self, *, to_email: str, trend_name: str, days_to_critical: int) -> dict:
        subject = "⚠️ Trend Decline Alert – Action Required"
        body = (
            f"Hello,\n\n"
            f"Trend '{trend_name}' is predicted to reach a critical decline state within {days_to_critical} days.\n\n"
            "Recommended next steps:\n"
            "• Review engagement changes\n"
            "• Identify contributing signals\n"
            "• Activate retention / comeback strategy\n\n"
            "Regards,\n"
            f"{config.ALERT_FROM_NAME}"
        )
        return self.send_email(to_email=to_email, subject=subject, body=body)
