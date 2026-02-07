"""
Lifecycle Classification Model: Rule-based + AI Hybrid
Determines lifecycle stage using deterministic rules and computed signals
"""

import logging
from typing import Tuple

from .schemas import LifecycleStage, STAGE_NAMES, AggregatedSignals, GoogleTrendsSignals, TwitterSignals, RedditSignals

logger = logging.getLogger(__name__)


class LifecycleClassifier:
    """
    Deterministic rule engine for lifecycle stage detection
    """
    
    def __init__(self):
        # Thresholds for classification (tuned for hackathon demo)
        self.VIRAL_GROWTH_THRESHOLD = 50.0  # % growth rate
        self.HIGH_MOMENTUM_THRESHOLD = 30.0
        self.PLATEAU_RANGE = (-10.0, 10.0)  # Flat growth
        self.DECLINE_THRESHOLD = -15.0  # Negative growth
        self.DEATH_THRESHOLD = 5.0  # Interest score near zero
        self.DECAY_SIGNAL_THRESHOLD = 0.6  # Sustained decline
    
    def classify(
        self,
        google: GoogleTrendsSignals,
        twitter: TwitterSignals,
        reddit: RedditSignals,
        aggregated: AggregatedSignals
    ) -> Tuple[LifecycleStage, float]:
        """
        Classify lifecycle stage using rule-based logic
        
        Returns:
            (stage, base_confidence)
        """
        growth_rate = aggregated.growth_rate
        momentum = aggregated.momentum
        decay_signal = aggregated.decay_signal
        interest_score = google.interest_score
        engagement_saturation = aggregated.engagement_saturation
        
        # Extract key viral indicators
        comment_count = reddit.comment_count
        post_count = reddit.post_count
        comments_per_post = comment_count / post_count if post_count > 0 else 0
        
        logger.info(f"📊 Classification inputs: growth={growth_rate:.2f}, momentum={momentum:.2f}, decay={decay_signal:.2f}, interest={interest_score:.2f}")
        logger.info(f"📊 Engagement: {comment_count} comments, {post_count} posts, {comments_per_post:.1f} comments/post")
        
        # === Rule 0: VIRAL SPIKE DETECTION (Breaking News) ===
        # High engagement volume overrides growth calculations
        # This catches breaking news that growth_rate misses
        viral_indicators = 0
        
        # Indicator 1: Massive comment volume (>10k comments = major news)
        if comment_count > 10000:
            viral_indicators += 2  # Strong signal
            logger.info(f"   🔥 VIRAL SIGNAL: Massive comment volume ({comment_count:,})")
        elif comment_count > 5000:
            viral_indicators += 1
        
        # Indicator 2: High comments-per-post ratio (>500 = intense discussion)
        if comments_per_post > 500:
            viral_indicators += 2  # Very high engagement per post
            logger.info(f"   🔥 VIRAL SIGNAL: Intense engagement ({comments_per_post:.0f} comments/post)")
        elif comments_per_post > 200:
            viral_indicators += 1
        
        # Indicator 3: High Google Trends interest (>70 = major trend)
        if interest_score > 70:
            viral_indicators += 1
            logger.info(f"   🔥 VIRAL SIGNAL: High search interest ({interest_score:.0f})")
        
        # If 3+ viral indicators, it's VIRAL regardless of growth_rate
        if viral_indicators >= 3:
            logger.info(f"🚀 VIRAL EXPLOSION: {viral_indicators} viral indicators detected (breaking news/major event)")
            return LifecycleStage.VIRAL_EXPLOSION, 0.95
        
        # === Rule 1: Death ===
        # Google Trends dominance: If search interest is dead, the trend is dead
        # (Reddit nostalgia posts are misleading)
        # BUT: Only if engagement is also low (not a viral spike)
        if (interest_score < self.DEATH_THRESHOLD and 
            twitter.post_volume < 5 and
            comment_count < 1000):  # Low engagement confirms death
            logger.info(f"🪦 DEATH: Near-zero search interest (Google={interest_score:.1f}, Twitter={twitter.post_volume})")
            return LifecycleStage.DEATH, 0.95
        
        # === Rule 2: Decline ===
        # Sustained negative growth or high decay signal
        # BUT: Only if engagement is NOT viral (avoid misclassifying breaking news)
        if ((growth_rate < self.DECLINE_THRESHOLD or 
             decay_signal > self.DECAY_SIGNAL_THRESHOLD) and
            viral_indicators < 2):  # Allow 1 viral indicator, but not 2+
            logger.info("📉 DECLINE: Negative growth or sustained decay")
            return LifecycleStage.DECLINE, 0.85
        
        # === Rule 3: Viral Explosion ===
        # Rapid growth + rising momentum OR high engagement volume
        if (growth_rate > self.VIRAL_GROWTH_THRESHOLD and 
            momentum > self.HIGH_MOMENTUM_THRESHOLD) or \
           (viral_indicators >= 2):  # 2+ viral indicators = viral
            logger.info("🚀 VIRAL EXPLOSION: Rapid growth or high engagement detected")
            return LifecycleStage.VIRAL_EXPLOSION, 0.90
        
        # === Rule 3.5: Weak Engagement Decline ===
        # Dying trend with nostalgia posts (low engagement quality)
        if (growth_rate < 10 and  # Flat or slightly declining
            comments_per_post < 50 and  # Low engagement quality
            viral_indicators < 1 and  # Not viral
            comment_count > 500):  # Has some activity (not completely dead)
            logger.info(f"📉 DECLINE: Low engagement quality ({comments_per_post:.1f} comments/post - likely nostalgia/dead trend)")
            return LifecycleStage.DECLINE, 0.75
        
        # === Rule 4: Plateau ===
        # Flat growth but high volume/engagement AND high engagement quality
        if (self.PLATEAU_RANGE[0] < growth_rate < self.PLATEAU_RANGE[1] and
            (interest_score > 40 or twitter.post_volume > 50) and
            comments_per_post > 50):  # Require high engagement quality
            logger.info(f"📊 PLATEAU: Stable high engagement (quality: {comments_per_post:.1f} comments/post)")
            return LifecycleStage.PLATEAU, 0.80
        
        # === Rule 5: Emergence (Default) ===
        # Low-to-moderate activity, positive growth
        if growth_rate > 0:
            logger.info("🌱 EMERGENCE: Early growth detected")
            return LifecycleStage.EMERGENCE, 0.75
        
        # === Fallback: Emergence ===
        # When signals are ambiguous
        logger.info("🌱 EMERGENCE (fallback): Ambiguous signals")
        return LifecycleStage.EMERGENCE, 0.60
    
    def get_stage_name(self, stage: LifecycleStage) -> str:
        """Get human-readable stage name"""
        return STAGE_NAMES[stage]
    
    def calculate_confidence_score(
        self,
        base_confidence: float,
        aggregated: AggregatedSignals,
        google: GoogleTrendsSignals
    ) -> float:
        """
        Adjust confidence based on signal strength
        """
        # Check data quality
        has_google_data = google.interest_score > 0
        signal_strength = 1.0 if has_google_data else 0.5
        
        # Adjust for decay signal clarity
        if aggregated.decay_signal > 0.7 or aggregated.decay_signal < 0.3:
            signal_strength *= 1.1  # Clear signal (very high or very low decay)
        
        # Clamp confidence
        adjusted_confidence = base_confidence * signal_strength
        return max(0.0, min(1.0, adjusted_confidence))
