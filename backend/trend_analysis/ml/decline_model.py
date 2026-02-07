"""
Decline Prediction Model Module

This module contains the ML models for predicting trend decline.
In production, this would include:
- Trained XGBoost/LightGBM classifiers
- LSTM/Transformer models for time series prediction
- Ensemble methods combining multiple signals

For hackathon: Mock predictions with realistic probabilities
"""

from typing import Dict, List, Tuple
import numpy as np
from datetime import datetime, timedelta
import random

class DeclinePredictor:
    """
    Predict trend decline probability and timing
    
    Future ML models:
    1. XGBoost Classifier (primary model)
       - Input: 20+ engineered features
       - Output: Decline probability + feature importances
       - Training: Historical trends with known outcomes
    
    2. LSTM Time Series Model (secondary)
       - Input: Sequence of engagement metrics
       - Output: Decline timing (days until peak ends)
       - Captures temporal dependencies
    
    3. Ensemble (production)
       - Combine XGBoost + LSTM + rule-based heuristics
       - Weighted voting for final prediction
    """
    
    def __init__(self):
        self.model_version = "1.0.0-mock"
        self.threshold = 0.65  # Probability threshold for "declining" label
        self.confidence_bands = ["very_low", "low", "medium", "high", "very_high"]
    
    def predict_decline(
        self, 
        features: Dict[str, float],
        historical_data: List[Dict] = None
    ) -> Dict[str, any]:
        """
        Predict if and when a trend will decline
        
        Args:
            features: Engineered features from FeatureEngineer
            historical_data: Time series data for temporal models
        
        Returns:
            Prediction dictionary with probability, timing, confidence
        """
        
        # Mock prediction logic (replace with actual model.predict())
        # Probability increases with saturation and decreases with novelty
        saturation = features.get("audience_saturation", 0.5)
        novelty = features.get("novelty_score", 0.5)
        diversity = features.get("content_diversity", 0.5)
        
        # Weighted formula mimicking model behavior
        decline_prob = (
            saturation * 0.5 +
            (1 - novelty) * 0.3 +
            (1 - diversity) * 0.2
        )
        
        # Add some noise for realism
        decline_prob += random.uniform(-0.1, 0.1)
        decline_prob = max(0, min(1, decline_prob))
        
        # Predict days until decline
        if decline_prob > 0.7:
            days_until_decline = random.randint(3, 14)
        elif decline_prob > 0.5:
            days_until_decline = random.randint(14, 30)
        else:
            days_until_decline = random.randint(30, 90)
        
        # Calculate confidence
        confidence = self._calculate_confidence(decline_prob, features)
        
        return {
            "decline_probability": round(decline_prob, 3),
            "is_declining": decline_prob > self.threshold,
            "days_until_decline": days_until_decline,
            "confidence_level": confidence,
            "prediction_date": datetime.now().isoformat(),
            "model_version": self.model_version
        }
    
    def predict_trajectory(
        self, 
        trend_id: str,
        forecast_days: int = 30
    ) -> List[Dict[str, any]]:
        """
        Predict future trend trajectory
        
        Returns daily predictions for next N days
        This would use LSTM/Prophet for time series forecasting
        """
        predictions = []
        base_value = random.uniform(60, 90)  # Current trend strength
        
        for day in range(forecast_days):
            # Simulate decline curve
            decay_rate = 0.02
            value = base_value * (1 - decay_rate * day)
            value = max(10, value + random.uniform(-5, 5))
            
            date = datetime.now() + timedelta(days=day)
            predictions.append({
                "date": date.strftime("%Y-%m-%d"),
                "predicted_value": round(value, 2),
                "confidence_lower": round(value * 0.85, 2),
                "confidence_upper": round(value * 1.15, 2)
            })
        
        return predictions
    
    def _calculate_confidence(self, probability: float, features: Dict) -> str:
        """
        Calculate prediction confidence based on model certainty
        
        In production:
        - Check prediction variance across ensemble models
        - Consider feature quality indicators
        - Use calibration metrics
        """
        # Mock confidence calculation
        if probability > 0.8 or probability < 0.2:
            return "very_high"  # Model is very certain
        elif probability > 0.7 or probability < 0.3:
            return "high"
        elif probability > 0.6 or probability < 0.4:
            return "medium"
        else:
            return "low"  # Probability near 0.5 = uncertain
    
    def get_risk_factors(self, features: Dict[str, float]) -> List[Dict[str, any]]:
        """
        Identify top risk factors contributing to decline
        
        This would use SHAP values in production
        """
        risk_factors = []
        
        # Check each feature against thresholds
        if features.get("audience_saturation", 0) > 0.7:
            risk_factors.append({
                "factor": "High Audience Saturation",
                "severity": "high",
                "impact": 0.28,
                "description": "Most of target audience has already seen this trend"
            })
        
        if features.get("novelty_score", 1) < 0.3:
            risk_factors.append({
                "factor": "Low Content Novelty",
                "severity": "medium",
                "impact": 0.18,
                "description": "Content is becoming repetitive and predictable"
            })
        
        if features.get("influencer_penetration", 0) > 0.8:
            risk_factors.append({
                "factor": "Influencer Dependency",
                "severity": "medium",
                "impact": 0.15,
                "description": "Trend heavily relies on influencer participation"
            })
        
        return risk_factors
