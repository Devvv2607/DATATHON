from fastapi import FastAPI, HTTPException
from typing import Dict, List
from .models import User, Transaction, MonthlySummary
from .services import NotificationService
from .engine import BudgetEvaluationEngine
from . import config
from twilio.base.exceptions import TwilioRestException

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Smart Budget & Savings Notification Module"}

# In-memory data stores (for demonstration purposes)
users: Dict[str, User] = {}
transactions: Dict[str, List[Transaction]] = {}
summaries: Dict[str, MonthlySummary] = {}

# Initialize services
notification_service = NotificationService()
evaluation_engine = BudgetEvaluationEngine(notification_service)

# --- Example Data ---
# This would typically be in a database
# Replace with a real number for testing
users["user1"] = User(
    user_id="user1",
    phone_number="+919324862139",
    monthly_budget=30000,
    savings_goal=5000,
    alert_preferences={"enable_sms": True, "enable_whatsapp": False, "warning_threshold": 0.8}
)
transactions["user1"] = []
summaries["user1"] = MonthlySummary(user_id="user1")

@app.post("/transactions/add")
async def add_transaction(transaction: Transaction):
    """
    Adds a new transaction, updates the user's monthly summary,
    and triggers the budget evaluation engine.
    """
    if transaction.user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    if transaction.user_id not in transactions:
        transactions[transaction.user_id] = []
    transactions[transaction.user_id].append(transaction)

    summary = summaries.get(transaction.user_id, MonthlySummary(user_id=transaction.user_id))
    summary.total_spent += transaction.amount
    
    category_totals = {}
    for t in transactions[transaction.user_id]:
        category_totals[t.category] = category_totals.get(t.category, 0) + t.amount
    
    if category_totals:
        summary.top_category = max(category_totals, key=category_totals.get)

    summaries[transaction.user_id] = summary
    
    user = users[transaction.user_id]
    evaluation_engine.evaluate_and_notify(user, summary)
    
    return {"message": "Transaction added and evaluated", "summary": summary}

@app.get("/users/{user_id}/summary", response_model=MonthlySummary)
async def get_user_summary(user_id: str):
    """
    Returns the current monthly summary for a given user.
    """
    if user_id not in summaries:
        raise HTTPException(status_code=404, detail="Summary not found for user")
    return summaries[user_id]

@app.post("/evaluate/{user_id}")
async def evaluate_user_budget(user_id: str):
    """
    Manually triggers the budget evaluation for a user.
    """
    if user_id not in users or user_id not in summaries:
        raise HTTPException(status_code=404, detail="User or summary not found")

    user = users[user_id]
    summary = summaries[user_id]
    
    evaluation_engine.evaluate_and_notify(user, summary)
    
    return {"message": f"Evaluation triggered for user {user_id}"}

@app.get("/debug-sms")
async def debug_sms():
    """
    Sends a test SMS and returns debugging information.
    """
    debug_info = {
        "account_sid": config.TWILIO_ACCOUNT_SID,
        "messaging_service_sid": config.TWILIO_MESSAGING_SERVICE_SID,
        "to_number": users["user1"].phone_number,
        "status": "",
        "error": ""
    }

    try:
        message = notification_service.client.messages.create(
            body="This is a test message from the Smart Budget App.",
            messaging_service_sid=config.TWILIO_MESSAGING_SERVICE_SID,
            to=users["user1"].phone_number
        )
        debug_info["status"] = "Success"
        debug_info["message_sid"] = message.sid
    except TwilioRestException as e:
        debug_info["status"] = "Failed"
        debug_info["error"] = str(e)
    except Exception as e:
        debug_info["status"] = "Failed"
        debug_info["error"] = f"An unexpected error occurred: {str(e)}"
    
    return debug_info

# To run the app:
# uvicorn app.main:app --reload
#
# Example test transactions:
# curl -X POST "http://127.0.0.1:8000/transactions/add" -H "Content-Type: application/json" -d '{
#   "transaction_id": "t1", "user_id": "user1", "category": "Groceries", "amount": 2500
# }'
# curl -X POST "http://127.0.0.1:8000/transactions/add" -H "Content-Type: application/json" -d '{
#   "transaction_id": "t2", "user_id": "user1", "category": "Dining", "amount": 15000
# }'
# curl -X POST "http://127.0.0.1:8000/transactions/add" -H "Content-Type: application/json" -d '{
#   "transaction_id": "t3", "user_id": "user1", "category": "Shopping", "amount": 8000
# }' # This should trigger the near limit warning
# curl -X POST "http://127.0.0.1:8000/transactions/add" -H "Content-Type: application/json" -d '{
#   "transaction_id": "t4", "user_id": "user1", "category": "Travel", "amount": 5000
# }' # This should trigger the budget exceeded warning
