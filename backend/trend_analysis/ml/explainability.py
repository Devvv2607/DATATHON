"""
Explainability Module (XAI - Explainable AI)

This module provides human-readable explanations for model predictions.
Uses SHAP (SHapley Additive exPlanations) values and counterfactual reasoning.

Key capabilities:
- Feature attribution (which factors caused the prediction?)
- Counterfactual explanations (what would change the prediction?)
- Natural language generation for non-technical users
"""

from typing import Dict, List, Any
import random

class ExplainabilityEngine:
    """
    Generate explanations for trend decline predictions
    
    Future ML integration:
    - SHAP library for feature attribution
    - LIME for local interpretability
    - GPT-4 for natural language explanation generation
    - Counterfactual generation with DiCE library
    """
    
    def __init__(self):
        self.explanation_templates = {
            "high_saturation": "The trend has reached {saturation}% of its target audience, indicating market saturation.",
            "low_novelty": "Content novelty has dropped to {novelty}%, suggesting creative exhaustion.",
            "influencer_dependent": "Over {influence}% of engagement comes from influencers, creating dependency risk.",
            "sentiment_decline": "Sentiment scores show {sentiment}% positive feedback, down from peak levels."
        }
    
    def explain_prediction(
        self,
        prediction: Dict[str, Any],
        features: Dict[str, float],
        shap_values: Dict[str, float] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive explanation for decline prediction
        
        Args:
            prediction: Model prediction output
            features: Input features used
            shap_values: SHAP importance scores (mock if None)
        
        Returns:
            Explanation dictionary with multiple formats
        """
        
        # Mock SHAP values if not provided
        if shap_values is None:
            shap_values = self._generate_mock_shap(features)
        
        # Generate natural language explanation
        narrative = self._generate_narrative(prediction, features, shap_values)
        
        # Create feature attribution breakdown
        attributions = self._create_attribution_chart(shap_values)
        
        # Generate counterfactuals
        counterfactuals = self._generate_counterfactuals(features, prediction)
        
        return {
            "summary": narrative["summary"],
            "detailed_explanation": narrative["detailed"],
            "feature_attributions": attributions,
            "counterfactuals": counterfactuals,
            "confidence": narrative["confidence"],
            "recommendations": self._generate_recommendations(features, shap_values)
        }
    
    def _generate_mock_shap(self, features: Dict[str, float]) -> Dict[str, float]:
        """
        Generate mock SHAP values for demonstration
        
        In production: shap_values = explainer.shap_values(features)
        """
        # Higher values = stronger push toward "decline"
        return {
            "audience_saturation": features.get("audience_saturation", 0.5) * 0.35,
            "novelty_score": -(1 - features.get("novelty_score", 0.5)) * 0.25,
            "content_diversity": features.get("content_diversity", 0.5) * 0.15,
            "influencer_penetration": features.get("influencer_penetration", 0.5) * 0.12,
            "engagement_rate": -features.get("engagement_rate", 5) * 0.01,
            "sentiment_score": -features.get("sentiment_score", 0.7) * 0.08,
            "viral_coefficient": -features.get("viral_coefficient", 1.5) * 0.03,
            "platform_cross_pollination": -features.get("platform_cross_pollination", 0.5) * 0.02
        }
    
    def _generate_narrative(
        self,
        prediction: Dict,
        features: Dict,
        shap_values: Dict
    ) -> Dict[str, str]:
        """
        Generate natural language explanation
        
        Future: Use GPT-4 API for more sophisticated narratives
        """
        decline_prob = prediction.get("decline_probability", 0.5)
        
        # Summary sentence
        if decline_prob > 0.75:
            summary = f"This trend shows strong signs of decline ({decline_prob*100:.0f}% probability)."
        elif decline_prob > 0.5:
            summary = f"This trend is at moderate risk of decline ({decline_prob*100:.0f}% probability)."
        else:
            summary = f"This trend appears stable with low decline risk ({decline_prob*100:.0f}% probability)."
        
        # Detailed explanation
        top_factors = sorted(shap_values.items(), key=lambda x: abs(x[1]), reverse=True)[:3]
        
        detailed_parts = []
        for factor_name, impact in top_factors:
            factor_readable = factor_name.replace("_", " ").title()
            direction = "increasing" if impact > 0 else "decreasing"
            detailed_parts.append(
                f"{factor_readable} is {direction} decline risk by {abs(impact)*100:.1f} percentage points."
            )
        
        detailed = " ".join(detailed_parts)
        
        confidence_level = prediction.get("confidence_level", "medium")
        confidence = f"Prediction confidence: {confidence_level}"
        
        return {
            "summary": summary,
            "detailed": detailed,
            "confidence": confidence
        }
    
    def _create_attribution_chart(self, shap_values: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Format SHAP values for visualization in frontend
        
        Returns list of features with their impact scores
        """
        attributions = []
        
        for feature, impact in sorted(shap_values.items(), key=lambda x: abs(x[1]), reverse=True):
            attributions.append({
                "feature": feature.replace("_", " ").title(),
                "impact": round(impact, 4),
                "impact_percentage": round(abs(impact) * 100, 2),
                "direction": "decline" if impact > 0 else "growth"
            })
        
        return attributions
    
    def _generate_counterfactuals(
        self,
        features: Dict[str, float],
        prediction: Dict
    ) -> List[Dict[str, Any]]:
        """
        Generate counterfactual scenarios
        
        "If X were different, the prediction would change to Y"
        
        Future: Use DiCE library for counterfactual generation
        """
        counterfactuals = []
        
        # Example counterfactuals
        if features.get("audience_saturation", 0) > 0.6:
            counterfactuals.append({
                "scenario": "If audience saturation decreased to 40%",
                "change": {"audience_saturation": 0.40},
                "predicted_probability": prediction["decline_probability"] - 0.15,
                "outcome": "Trend would have lower decline risk"
            })
        
        if features.get("novelty_score", 0) < 0.5:
            counterfactuals.append({
                "scenario": "If content novelty increased to 75%",
                "change": {"novelty_score": 0.75},
                "predicted_probability": prediction["decline_probability"] - 0.12,
                "outcome": "Fresh content would reduce decline risk"
            })
        
        return counterfactuals
    
    def _generate_recommendations(
        self,
        features: Dict[str, float],
        shap_values: Dict[str, float]
    ) -> List[str]:
        """
        Generate actionable recommendations based on attribution
        
        Future: Connect to strategy generation model
        """
        recommendations = []
        
        # Find most impactful negative factors
        negative_factors = [(k, v) for k, v in shap_values.items() if v > 0]
        negative_factors.sort(key=lambda x: x[1], reverse=True)
        
        for factor, _ in negative_factors[:3]:
            if factor == "audience_saturation":
                recommendations.append("Target new audience segments to reduce saturation")
            elif factor == "novelty_score":
                recommendations.append("Introduce fresh content angles and creative variations")
            elif factor == "influencer_penetration":
                recommendations.append("Reduce influencer dependency through organic community growth")
        
        return recommendations
