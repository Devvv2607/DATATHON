import logging
from .models import User, MonthlySummary
from .services import NotificationService

class BudgetEvaluationEngine:
    def __init__(self, notification_service: NotificationService):
        self.notification_service = notification_service

    def evaluate_and_notify(self, user: User, summary: MonthlySummary):
        # Rule 1: Budget Exceeded
        if summary.total_spent > user.monthly_budget:
            overspend = summary.total_spent - user.monthly_budget
            logging.info(f"[ALERT_TRIGGERED] BUDGET_EXCEEDED | Spent={summary.total_spent} | Budget={user.monthly_budget}")
            self.notification_service.send_notification(
                user,
                "BUDGET_EXCEEDED",
                {"budget": user.monthly_budget, "overspend": round(overspend, 2), "category": summary.top_category}
            )
            return

        # Rule 2: Near Budget Limit
        warning_threshold = user.alert_preferences.get("warning_threshold", 0.8)
        if summary.total_spent >= user.monthly_budget * warning_threshold:
            percent_spent = (summary.total_spent / user.monthly_budget) * 100
            logging.info(f"[ALERT_TRIGGERED] NEAR_LIMIT | Spent={summary.total_spent} | Budget={user.monthly_budget} | Threshold={warning_threshold}")
            self.notification_service.send_notification(
                user,
                "NEAR_LIMIT",
                {"percent": round(percent_spent)}
            )

        # Rule 3: Savings Achieved
        saved_amount = user.monthly_budget - summary.total_spent
        if saved_amount >= user.savings_goal:
            logging.info(f"[ALERT_TRIGGERED] SAVINGS_ACHIEVED | Saved={saved_amount} | Goal={user.savings_goal}")
            self.notification_service.send_notification(
                user,
                "SAVINGS_ACHIEVED",
                {"saved": round(saved_amount, 2)}
            )
