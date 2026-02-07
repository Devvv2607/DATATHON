"""Trend classification logic"""
from models import TrendMetrics, TrendClassification


class TrendClassifier:
    """Classifies trends as growing, stable, or declining"""
    
    def __init__(self, growth_threshold: float = 5.0, decline_threshold: float = -5.0):
        """
        Initialize classifier with thresholds.
        
        Args:
            growth_threshold: Minimum growth rate for "growing" classification (%)
            decline_threshold: Maximum growth rate for "declining" classification (%)
        """
        self.growth_threshold = growth_threshold
        self.decline_threshold = decline_threshold
    
    def classify(self, trend_metrics: TrendMetrics) -> TrendClassification:
        """
        Classify a trend based on its metrics.
        
        Args:
            trend_metrics: Calculated trend metrics
            
        Returns:
            TrendClassification with category and reasoning
        """
        growth_slope = trend_metrics.growth_slope
        
        # Classify based on thresholds
        if growth_slope > self.growth_threshold:
            category = "growing"
            confidence = min(0.95, 0.7 + (growth_slope / 100))
            reasoning = (
                f"Trend shows positive momentum with {growth_slope:.1f}% monthly growth. "
                f"Current interest at {trend_metrics.current_interest}, "
                f"peak was {trend_metrics.peak_interest}. "
                f"Strong upward trajectory indicates growing market demand."
            )
        elif growth_slope < self.decline_threshold:
            category = "declining"
            confidence = min(0.95, 0.7 + (abs(growth_slope) / 100))
            reasoning = (
                f"Trend shows negative momentum with {growth_slope:.1f}% monthly decline. "
                f"Current interest at {trend_metrics.current_interest}, "
                f"down from peak of {trend_metrics.peak_interest}. "
                f"Declining trajectory suggests waning market interest."
            )
        else:
            category = "stable"
            # Lower confidence for stable trends
            confidence = 0.6 + (0.2 * (1 - abs(growth_slope) / self.growth_threshold))
            reasoning = (
                f"Trend shows stable momentum with {growth_slope:.1f}% monthly change. "
                f"Current interest at {trend_metrics.current_interest}, "
                f"maintaining relatively consistent levels. "
                f"Stable trajectory indicates sustained but not growing demand."
            )
        
        return TrendClassification(
            category=category,
            confidence=float(confidence),
            growth_rate=growth_slope,
            reasoning=reasoning
        )
