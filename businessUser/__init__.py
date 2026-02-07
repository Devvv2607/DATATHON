"""
Business User Module - Marketing & Engagement Decision Intelligence System
Transforms technical outputs into actionable business decisions
"""

from .trend_context import get_trend_context
from .risk_decision_summary import get_risk_decision_summary
from .engagement_health import get_engagement_health
from .roi_attribution import analyze_roi
from .investment_decision import get_investment_decision
from .decision_explanation import get_decision_explanation
from .campaign_timing import get_campaign_timing
from .decline_window import get_decline_window
from .risk_reversal_engine import get_decision_levers
from .executive_takeaway import get_executive_takeaway
from .pivot_strategy import get_pivot_strategy
from .alternative_trends import get_alternative_trends

__all__ = [
    "get_trend_context",
    "get_risk_decision_summary",
    "get_engagement_health",
    "analyze_roi",
    "get_investment_decision",
    "get_decision_explanation",
    "get_campaign_timing",
    "get_decline_window",
    "get_decision_levers",
    "get_executive_takeaway",
    "get_pivot_strategy",
    "get_alternative_trends"
]
