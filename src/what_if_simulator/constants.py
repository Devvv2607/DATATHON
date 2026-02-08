"""Constants and configuration for the simulator."""

from typing import Dict, Set, Tuple

# Lifecycle stages
LIFECYCLE_STAGES = {"emerging", "growth", "peak", "decline", "dormant"}

# Campaign types
CAMPAIGN_TYPES = {"short_term_influencer", "long_term_paid", "organic_only", "mixed"}

# Creator tiers
CREATOR_TIERS = {"nano", "micro", "macro", "mixed"}

# Confidence levels
CONFIDENCE_LEVELS = {"low", "medium", "high"}

# Risk tolerance levels
RISK_TOLERANCE_LEVELS = {"low", "medium", "high"}

# Engagement trend assumptions
ENGAGEMENT_TRENDS = {"optimistic", "neutral", "pessimistic"}

# Creator participation assumptions
CREATOR_PARTICIPATION = {"increasing", "stable", "declining"}

# Market noise assumptions
MARKET_NOISE = {"low", "medium", "high"}

# Content intensity levels
CONTENT_INTENSITY = {"low", "medium", "high"}

# Budget ranges
BUDGET_RANGES = {"low", "medium", "high"}

# Recommended postures
RECOMMENDED_POSTURES = {"scale", "test_small", "monitor", "avoid"}

# Risk trends
RISK_TRENDS = {"improving", "stable", "worsening"}

# Overall outlooks
OVERALL_OUTLOOKS = {"favorable", "risky", "unfavorable"}

# Impact levels
IMPACT_LEVELS = {"low", "medium", "high"}

# Lifecycle-Campaign Type Compatibility Matrix
# Maps (lifecycle_stage, campaign_type) -> (is_compatible, is_high_risk)
COMPATIBILITY_MATRIX: Dict[Tuple[str, str], Tuple[bool, bool]] = {
    # Emerging stage
    ("emerging", "short_term_influencer"): (True, False),
    ("emerging", "long_term_paid"): (True, True),
    ("emerging", "organic_only"): (True, False),
    ("emerging", "mixed"): (True, False),
    # Growth stage
    ("growth", "short_term_influencer"): (True, False),
    ("growth", "long_term_paid"): (True, False),
    ("growth", "organic_only"): (True, False),
    ("growth", "mixed"): (True, False),
    # Peak stage
    ("peak", "short_term_influencer"): (True, False),
    ("peak", "long_term_paid"): (True, True),
    ("peak", "organic_only"): (True, False),
    ("peak", "mixed"): (True, True),
    # Decline stage
    ("decline", "short_term_influencer"): (True, True),
    ("decline", "long_term_paid"): (False, True),
    ("decline", "organic_only"): (True, True),
    ("decline", "mixed"): (True, True),  # Allow mixed but high-risk
    # Dormant stage
    ("dormant", "short_term_influencer"): (True, True),
    ("dormant", "long_term_paid"): (False, True),
    ("dormant", "organic_only"): (True, True),
    ("dormant", "mixed"): (True, True),  # Allow mixed but high-risk
}

# Default assumptions
DEFAULT_ASSUMPTIONS = {
    "engagement_trend": "neutral",
    "creator_participation": "stable",
    "market_noise": "medium",
}

# Multiplier ranges for campaign parameters
CAMPAIGN_BUDGET_MULTIPLIERS = {
    "low": (0.5, 0.8),
    "medium": (0.8, 1.2),
    "high": (1.2, 1.8),
}

CREATOR_TIER_REACH_MULTIPLIERS = {
    "nano": (0.3, 0.5),
    "micro": (0.5, 0.8),
    "macro": (0.8, 1.2),
    "mixed": (0.6, 0.9),
}

CONTENT_INTENSITY_MULTIPLIERS = {
    "low": (0.6, 0.8),
    "medium": (0.8, 1.1),
    "high": (1.1, 1.4),
}

# Assumption modifiers
ENGAGEMENT_TREND_MODIFIERS = {
    "optimistic": (1.1, 1.3),  # (min_multiplier, max_multiplier)
    "neutral": (0.9, 1.1),
    "pessimistic": (0.7, 0.9),
}

CREATOR_PARTICIPATION_MODIFIERS = {
    "increasing": (1.0, 1.2),
    "stable": (0.9, 1.1),
    "declining": (0.6, 0.8),
}

MARKET_NOISE_RANGE_WIDENING = {
    "low": 1.0,  # No widening
    "medium": 1.2,  # 20% wider
    "high": 1.5,  # 50% wider
}

# Confidence thresholds
CONFIDENCE_THRESHOLD_LOW = 50  # Below 50% triggers range widening

# Data coverage thresholds
DATA_COVERAGE_THRESHOLD_LOW = 50  # Below 50% triggers warning

# Campaign duration thresholds
DIMINISHING_RETURNS_THRESHOLD_DAYS = 90

# Risk score bounds
MIN_RISK_SCORE = 0
MAX_RISK_SCORE = 100

# Probability bounds
MIN_PROBABILITY = 0
MAX_PROBABILITY = 100

# Break-even probability thresholds for posture recommendations
BREAK_EVEN_AGGRESSIVE_THRESHOLD = 70
BREAK_EVEN_MODERATE_MIN = 40
BREAK_EVEN_MODERATE_MAX = 70
BREAK_EVEN_CONSERVATIVE_THRESHOLD = 40

# Loss probability threshold for "avoid" posture
LOSS_PROBABILITY_AVOID_THRESHOLD = 60

# Risk trend determination thresholds
RISK_TREND_STABLE_THRESHOLD = 2  # Within 2 points is considered stable
