"""
Business logic layer for trend analysis
Orchestrates ML models, data processing, and external API calls
"""

from typing import List, Dict, Any, Optional
import random
from datetime import datetime, timedelta
from trend_analysis.ml.feature_engineering import FeatureEngineer
from trend_analysis.ml.decline_model import DeclinePredictor
from trend_analysis.ml.explainability import ExplainabilityEngine
from trend_analysis.ml.simulation import TrendSimulator
from trend_analysis.schema import (
    TrendOverview, TrendDetails, DeclinePrediction,
    ExplanationResponse, SimulationResponse, TrendStatus, PlatformType
)
from shared.utils import generate_time_series, calculate_health_score

class TrendAnalysisService:
    """
    Core service layer for trend analysis operations
    
    This service:
    1. Fetches data from social media APIs (mocked for now)
    2. Processes raw data through feature engineering
    3. Runs ML models for predictions
    4. Formats results for API responses
    """
    
    def __init__(self):
        self.feature_engineer = FeatureEngineer()
        self.decline_predictor = DeclinePredictor()
        self.explainability_engine = ExplainabilityEngine()
        self.simulator = TrendSimulator()
        
        # Mock trend database (replace with real DB)
        self.mock_trends = self._generate_mock_trends()
    
    def get_all_trends(
        self,
        platforms: Optional[List[PlatformType]] = None,
        status: Optional[TrendStatus] = None,
        limit: int = 20
    ) -> List[TrendOverview]:
        """
        Get list of trending topics
        
        In production:
        - Query database with filters
        - Cache popular queries
        - Real-time data from social APIs
        """
        trends = self.mock_trends
        
        # Apply filters
        if platforms:
            trends = [t for t in trends if any(p in t["platforms"] for p in platforms)]
        
        if status:
            trends = [t for t in trends if t["status"] == status]
        
        return trends[:limit]
    
    def get_trend_details(self, trend_id: str) -> Optional[TrendDetails]:
        """
        Get detailed information about a specific trend
        
        Includes:
        - Historical metrics
        - Top contributors
        - Geographic distribution
        """
        # Find trend in mock database
        trend = next((t for t in self.mock_trends if t["id"] == trend_id), None)
        
        if not trend:
            return None
        
        # Generate detailed historical data
        engagement_history = generate_time_series(days=30, volatility=0.15)
        sentiment_history = generate_time_series(days=30, volatility=0.1)
        
        # Mock influencer data
        top_influencers = [
            {"name": "@techinfluencer", "followers": 1_200_000, "engagement": 8.5},
            {"name": "@trendmaker", "followers": 850_000, "engagement": 12.3},
            {"name": "@viralcreator", "followers": 650_000, "engagement": 9.8}
        ]
        
        # Mock geographic data
        geographic_spread = {
            "US": 35.2,
            "UK": 18.5,
            "India": 15.3,
            "Canada": 8.7,
            "Australia": 7.1,
            "Others": 15.2
        }
        
        return TrendDetails(
            **trend,
            engagement_history=engagement_history,
            sentiment_history=sentiment_history,
            top_influencers=top_influencers,
            geographic_spread=geographic_spread
        )
    
    def predict_decline(self, trend_id: str) -> Optional[DeclinePrediction]:
        """
        Predict if and when a trend will decline
        
        Process:
        1. Extract features from trend data
        2. Run through ML model
        3. Return prediction with confidence
        """
        trend = next((t for t in self.mock_trends if t["id"] == trend_id), None)
        
        if not trend:
            return None
        
        # Extract features
        features = self.feature_engineer.extract_features(trend_id, trend)
        
        # Get prediction from model
        prediction = self.decline_predictor.predict_decline(features)
        
        return DeclinePrediction(
            trend_id=trend_id,
            **prediction
        )
    
    def explain_prediction(self, trend_id: str) -> Optional[ExplanationResponse]:
        """
        Generate explanation for why a trend is predicted to decline
        
        Uses SHAP values and counterfactual reasoning
        """
        # Get prediction first
        prediction_dict = self.predict_decline(trend_id)
        
        if not prediction_dict:
            return None
        
        # Get trend features
        trend = next((t for t in self.mock_trends if t["id"] == trend_id), None)
        features = self.feature_engineer.extract_features(trend_id, trend)
        
        # Generate explanation
        explanation = self.explainability_engine.explain_prediction(
            prediction=prediction_dict.model_dump(),
            features=features
        )
        
        return ExplanationResponse(**explanation)
    
    def simulate_intervention(
        self,
        trend_id: str,
        interventions: Dict[str, float],
        forecast_days: int = 30
    ) -> Optional[SimulationResponse]:
        """
        Simulate what-if scenarios with interventions
        
        Examples:
        - Add 5 influencers: {"add_influencers": 5}
        - Increase novelty by 20%: {"increase_content_novelty": 0.2}
        """
        trend = next((t for t in self.mock_trends if t["id"] == trend_id), None)
        
        if not trend:
            return None
        
        # Get current features
        current_features = self.feature_engineer.extract_features(trend_id, trend)
        
        # Run simulation
        simulation = self.simulator.simulate_intervention(
            current_features=current_features,
            interventions=interventions,
            forecast_days=forecast_days
        )
        
        return SimulationResponse(**simulation)
    
    def get_trend_trajectory(self, trend_id: str, days: int = 30) -> List[Dict]:
        """
        Get predicted trend trajectory
        
        Returns daily predictions for health score, engagement, sentiment
        """
        prediction = self.decline_predictor.predict_trajectory(trend_id, days)
        return prediction
    
    def _generate_mock_trends(self) -> List[Dict[str, Any]]:
        """
        Generate realistic mock trends for demo
        
        In production: Replace with database queries
        """
        trend_names = [
            "#AIRevolution2026",
            "#SustainableFashion",
            "#MetaverseLife",
            "#CryptoRecovery",
            "#RemoteWork",
            "#HealthTech",
            "#GenZMarketing",
            "#ClimateAction",
            "#WebThreeDev",
            "#MindfulLiving"
        ]
        
        platforms_options = [
            [PlatformType.TWITTER, PlatformType.INSTAGRAM],
            [PlatformType.TIKTOK, PlatformType.YOUTUBE],
            [PlatformType.REDDIT, PlatformType.TWITTER],
            [PlatformType.INSTAGRAM, PlatformType.TIKTOK, PlatformType.TWITTER]
        ]
        
        statuses = [TrendStatus.GROWING, TrendStatus.PEAK, TrendStatus.DECLINING, TrendStatus.EMERGING]
        
        trends = []
        
        for i, name in enumerate(trend_names):
            engagement = random.uniform(2.5, 12.0)
            sentiment = random.uniform(0.5, 0.9)
            viral_coef = random.uniform(0.8, 2.5)
            
            health = calculate_health_score(
                engagement=engagement * 10,
                sentiment=sentiment * 100,
                velocity=random.uniform(-50, 50),
                novelty=random.uniform(30, 85)
            )
            
            trends.append({
                "id": f"trend_{i+1}",
                "name": name,
                "description": f"Analysis of {name} trend across social media platforms",
                "platforms": random.choice(platforms_options),
                "status": random.choice(statuses),
                "metrics": {
                    "engagement_rate": round(engagement, 2),
                    "sentiment_score": round(sentiment, 3),
                    "viral_coefficient": round(viral_coef, 2),
                    "health_score": health
                },
                "top_hashtags": [name, f"#{name.split('#')[1][:5]}", "#trending"],
                "created_at": datetime.now() - timedelta(days=random.randint(5, 45)),
                "last_updated": datetime.now()
            })
        
        return trends
