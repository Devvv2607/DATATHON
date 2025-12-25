import logging
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from . import config

logging.basicConfig(level=logging.INFO)

class NotificationService:
    def __init__(self):
        self.client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)

    def _send_sms(self, to: str, message: str):
        logging.info(f"Attempting to send SMS using SID: {config.TWILIO_MESSAGING_SERVICE_SID}")
        try:
            self.client.messages.create(
                body=message,
                messaging_service_sid=config.TWILIO_MESSAGING_SERVICE_SID,
                to=to
            )
            logging.info(f"SMS sent successfully to {to}: {message}")
        except TwilioRestException as e:
            logging.error(f"Twilio API Error: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

    def send_notification(self, user, template_id: str, context: dict):
        message_templates = {
            "BUDGET_EXCEEDED": "⚠️ Budget Alert: You've exceeded your ₹{budget} budget by ₹{overspend}. Top spending category: {category}.",
            "NEAR_LIMIT": "Heads up! You've used {percent}% of your monthly budget. Consider reducing discretionary spending.",
            "SAVINGS_ACHIEVED": "🎉 Congratulations! You've saved ₹{saved} this month. Great financial discipline!",
            "MONTHLY_SUMMARY": "📊 Monthly Summary: Budget: ₹{budget}, Spent: ₹{spent}, Saved: ₹{saved}, Top category: {category}"
        }

        message = message_templates.get(template_id, "").format(**context)
        if not message:
            logging.warning(f"Invalid template ID: {template_id}")
            return

        if user.alert_preferences.get("enable_sms"):
            self._send_sms(user.phone_number, message)
