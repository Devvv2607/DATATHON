from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict

class User(BaseModel):
    user_id: str
    phone_number: str
    monthly_budget: float
    savings_goal: float
    alert_preferences: Dict = Field(default_factory=lambda: {
        "enable_sms": True,
        "enable_whatsapp": False,
        "warning_threshold": 0.8
    })

class Transaction(BaseModel):
    transaction_id: str
    user_id: str
    category: str
    amount: float
    date: datetime = Field(default_factory=datetime.utcnow)

class MonthlySummary(BaseModel):
    user_id: str
    total_spent: float = 0.0
    total_saved: float = 0.0
    overspend_amount: float = 0.0
    top_category: str = "N/A"
