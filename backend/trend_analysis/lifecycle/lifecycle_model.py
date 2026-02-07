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
        
        logger.info(f"📊 Classification inputs: growth={growth_rate:.2f}, momentum={momentum:.2f}, decay={decay_signal:.2f}, interest={interest_score:.2f}")
        
        # === Rule 1: Death ===
        # Near-zero activity across all platforms
        if (interest_score < self.DEATH_THRESHOLD and 
            twitter.post_volume < 5 and 
            reddit.post_count < 3):
            logger.info("🪦 DEATH: Near-zero activity detected")
            return LifecycleStage.DEATH, 0.95
        
        # === Rule 2: Decline ===
        # Sustained negative growth or high decay signal
        if (growth_rate < self.DECLINE_THRESHOLD or 
            decay_signal > self.DECAY_SIGNAL_THRESHOLD):
            logger.info("📉 DECLINE: Negative growth or sustained decay")
            return LifecycleStage.DECLINE, 0.85
        
        # === Rule 3: Viral Explosion ===
        # Rapid growth + rising momentum
        if (growth_rate > self.VIRAL_GROWTH_THRESHOLD and 
            momentum > self.HIGH_MOMENTUM_THRESHOLD):
            logger.info("🚀 VIRAL EXPLOSION: Rapid growth detected")
            return LifecycleStage.VIRAL_EXPLOSION, 0.90
        
        # === Rule 4: Plateau ===
        # Flat growth but high volume/engagement
        if (self.PLATEAU_RANGE[0] < growth_rate < self.PLATEAU_RANGE[1] and
            (interest_score > 40 or twitter.post_volume > 50)):
            logger.info("📊 PLATEAU: Stable high engagement")
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
