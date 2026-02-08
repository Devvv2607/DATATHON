import logging
import json
import os
from datetime import datetime, timedelta, timezone
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from typing import Optional
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from . import config

logging.basicConfig(level=logging.INFO)

class NotificationService:
    def __init__(self):
        self.client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)

    def _utcnow(self) -> datetime:
        return datetime.now(timezone.utc)

    def _append_alert_log(self, record: dict) -> None:
        try:
            with open(config.ALERT_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception as e:
            logging.error(f"Failed to write alert log: {e}")

    def _find_recent_event(self, event_key: str, within: timedelta) -> Optional[dict]:
        if not os.path.exists(config.ALERT_LOG_PATH):
            return None

        cutoff = self._utcnow() - within
        try:
            with open(config.ALERT_LOG_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                    except Exception:
                        continue
                    if rec.get("event_key") != event_key:
                        continue
                    ts = rec.get("timestamp")
                    if not ts:
                        continue
                    try:
                        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    except Exception:
                        continue
                    if dt >= cutoff:
                        return rec
        except Exception as e:
            logging.error(f"Failed to read alert log: {e}")
        return None

    def _send_sms(self, to: str, message: str):
        logging.info(f"Attempting to send SMS using SID: {config.TWILIO_MESSAGING_SERVICE_SID}")
        try:
            payload = {
                "body": message,
                "to": to,
            }
            if config.TWILIO_MESSAGING_SERVICE_SID:
                payload["messaging_service_sid"] = config.TWILIO_MESSAGING_SERVICE_SID
            elif config.TWILIO_PHONE_NUMBER:
                payload["from_"] = config.TWILIO_PHONE_NUMBER
            else:
                raise ValueError("Missing TWILIO_MESSAGING_SERVICE_SID or TWILIO_PHONE_NUMBER")

            self.client.messages.create(**payload)
            logging.info(f"SMS sent successfully to {to}: {message}")
        except TwilioRestException as e:
            logging.error(f"Twilio API Error: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

    def _send_sms_with_retry(self, to: str, message: str, max_attempts: int = 3) -> dict:
        last_error = ""
        for attempt in range(1, max_attempts + 1):
            try:
                if not config.TWILIO_ACCOUNT_SID or not config.TWILIO_AUTH_TOKEN:
                    raise ValueError("Missing TWILIO_ACCOUNT_SID or TWILIO_AUTH_TOKEN")

                payload = {
                    "body": message,
                    "to": to,
                }
                if config.TWILIO_MESSAGING_SERVICE_SID:
                    payload["messaging_service_sid"] = config.TWILIO_MESSAGING_SERVICE_SID
                elif config.TWILIO_PHONE_NUMBER:
                    payload["from_"] = config.TWILIO_PHONE_NUMBER
                else:
                    raise ValueError("Missing TWILIO_MESSAGING_SERVICE_SID or TWILIO_PHONE_NUMBER")

                msg = self.client.messages.create(**payload)
                return {"status": "sent", "attempts": attempt, "message_sid": getattr(msg, "sid", None)}
            except TwilioRestException as e:
                last_error = str(e)
                logging.error(f"Twilio API Error (attempt {attempt}/{max_attempts}): {e}")
            except Exception as e:
                last_error = str(e)
                logging.error(f"Unexpected SMS error (attempt {attempt}/{max_attempts}): {e}")
        return {"status": "failed", "attempts": max_attempts, "error": last_error}

    def _send_email_with_retry(self, to_email: str, subject: str, body: str, max_attempts: int = 3) -> dict:
        last_error = ""
        for attempt in range(1, max_attempts + 1):
            try:
                if not config.GMAIL_SMTP_USER or not config.GMAIL_SMTP_APP_PASSWORD:
                    raise ValueError("Missing GMAIL_SMTP_USER or GMAIL_SMTP_APP_PASSWORD")

                msg = MIMEText(body, _charset="utf-8")
                msg["From"] = config.GMAIL_SMTP_USER or ""
                msg["To"] = to_email
                msg["Date"] = formatdate(localtime=False)
                msg["Subject"] = subject

                with smtplib.SMTP(config.GMAIL_SMTP_HOST, config.GMAIL_SMTP_PORT, timeout=20) as server:
                    server.ehlo()
                    server.starttls()
                    server.ehlo()
                    server.login(config.GMAIL_SMTP_USER, config.GMAIL_SMTP_APP_PASSWORD)
                    server.sendmail(config.GMAIL_SMTP_USER, [to_email], msg.as_string())
                return {"status": "sent", "attempts": attempt}
            except Exception as e:
                last_error = str(e)
                logging.error(f"Email send error (attempt {attempt}/{max_attempts}): {e}")
        return {"status": "failed", "attempts": max_attempts, "error": last_error}

    def send_trent_decline_alert(
        self,
        *,
        predicted_trent_change: float,
        prediction_window_days: int,
        confidence: float,
        impact: str,
        to_phone_number: str,
        to_email: str,
    ) -> dict:
        """Sends SMS + email alerts when a decline is predicted within the window.

        This method does not fabricate inputs; callers must pass real model outputs.
        """
        event_key = f"trent_decline:{prediction_window_days}:{round(predicted_trent_change, 6)}"

        triggered = (predicted_trent_change < 0) and (prediction_window_days <= 7)
        if not triggered:
            return {
                "alert_triggered": False,
                "channels": [],
                "confidence": confidence,
                "prediction_window_days": prediction_window_days,
                "status": "not_triggered",
            }

        if confidence < 0.70:
            return {
                "alert_triggered": False,
                "channels": [],
                "confidence": confidence,
                "prediction_window_days": prediction_window_days,
                "status": "validation_failed",
                "reason": "confidence_below_threshold",
            }

        if abs(predicted_trent_change) < float(config.TRENT_DECLINE_THRESHOLD):
            return {
                "alert_triggered": False,
                "channels": [],
                "confidence": confidence,
                "prediction_window_days": prediction_window_days,
                "status": "validation_failed",
                "reason": "decline_below_threshold",
            }

        recent = self._find_recent_event(event_key, within=timedelta(hours=24))
        if recent is not None:
            return {
                "alert_triggered": False,
                "channels": [],
                "confidence": confidence,
                "prediction_window_days": prediction_window_days,
                "status": "suppressed",
                "reason": "dedupe_24h",
            }

        sms_body = (
            "Alert: Trent is predicted to decline within 7 days.\n\n"
            "Recommended Action:\n"
            "Review engagement metrics and activate retention strategies immediately."
        )

        email_subject = "⚠️ Trent Decline Alert – Action Required"
        email_body = (
            "Hello Team,\n\n"
            "Our predictive system indicates that Trent is expected to decline within the next 7 days.\n\n"
            f"Confidence Level: {int(round(confidence * 100))}%\n"
            f"Expected Impact: {impact}\n\n"
            "Recommended next steps:\n"
            "• Review recent engagement changes\n"
            "• Inspect acquisition funnel\n"
            "• Activate retention campaigns\n\n"
            "This alert was generated automatically by the Predictive Monitoring System.\n\n"
            "Regards,\n"
            "AI Monitoring Agent"
        )

        sms_result = self._send_sms_with_retry(to_phone_number, sms_body, max_attempts=3)
        email_result = self._send_email_with_retry(to_email, email_subject, email_body, max_attempts=3)

        overall_status = "sent"
        if sms_result.get("status") != "sent" or email_result.get("status") != "sent":
            overall_status = "failed"

        record = {
            "timestamp": self._utcnow().isoformat().replace("+00:00", "Z"),
            "event_key": event_key,
            "predicted_trent_change": predicted_trent_change,
            "prediction_window_days": prediction_window_days,
            "confidence": confidence,
            "channels": {
                "sms": {"to": to_phone_number, **sms_result},
                "email": {"to": to_email, **email_result},
            },
            "status": overall_status,
        }
        self._append_alert_log(record)

        return {
            "alert_triggered": True,
            "channels": ["sms", "email"],
            "confidence": confidence,
            "prediction_window_days": prediction_window_days,
            "status": overall_status,
        }
