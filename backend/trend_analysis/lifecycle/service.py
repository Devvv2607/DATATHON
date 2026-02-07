"""
Business Logic Service for Trend Lifecycle Detection
Orchestrates feature extraction, classification, and validation
"""

import logging
from typing import Dict, Any
from bson import ObjectId

from .schemas import (
    TrendLifecycleResponse, 
    TrendLifecycleDocument,
    STAGE_NAMES
)
from .feature_engineering import FeatureEngineer
from .lifecycle_model import LifecycleClassifier
from .gemini_validator import GeminiValidator
from .db import lifecycle_db

logger = logging.getLogger(__name__)


class LifecycleService:
    """
    Main service orchestrating the lifecycle detection pipeline
    """
    
    def __init__(self):
        self.feature_engineer = FeatureEngineer()
        self.classifier = LifecycleClassifier()
        self.gemini_validator = GeminiValidator()
    
    async def detect_lifecycle(self, trend_name: str) -> TrendLifecycleResponse:
        """
        Main pipeline: Extract → Classify → Validate → Store
        
        Args:
            trend_name: Name of the trend to analyze
        
        Returns:
            TrendLifecycleResponse with strict contract
        """
        logger.info(f"🔍 Starting lifecycle detection for: '{trend_name}'")
        
        try:
            # === STEP 1: Feature Extraction ===
            logger.info("📡 Extracting features from APIs...")
            
            google_signals = await self.feature_engineer.extract_google_signals(trend_name)
            
            # Try Twitter first, fallback to Reddit if Twitter fails
            twitter_signals = await self.feature_engineer.extract_twitter_signals(trend_name)
            if twitter_signals.post_volume == 0:
                logger.info("⚠️ Twitter data unavailable, using Reddit as primary source")
            
            # Always get Reddit data (more reliable than Twitter)
            reddit_signals = await self.feature_engineer.extract_reddit_signals(trend_name)
            
            aggregated_signals = self.feature_engineer.compute_aggregated_signals(
                google_signals, twitter_signals, reddit_signals
            )
            
            logger.info(f"✅ Features extracted - Interest: {google_signals.interest_score:.1f}, Reddit posts: {reddit_signals.post_count}, Growth: {aggregated_signals.growth_rate:.1f}%")
            
            # === DATA SOURCE STATUS ===
            data_sources_used = []
            if google_signals.interest_score > 0:
                data_sources_used.append("Google Trends")
            if twitter_signals.post_volume > 0:
                data_sources_used.append("Twitter")
            if reddit_signals.post_count > 0:
                data_sources_used.append("Reddit")
            
            data_source_status = ", ".join(data_sources_used) if data_sources_used else "None (using fallback)"
            is_real_data = len(data_sources_used) > 0
            
            logger.info(f"{'✅ REAL-TIME DATA' if is_real_data else '⚠️ MOCK DATA'} | Sources: {data_source_status}")
            
            # === STEP 2: Rule-based Classification ===
            logger.info("🧮 Classifying lifecycle stage...")
            
            stage, base_confidence = self.classifier.classify(
                google_signals,
                twitter_signals,
                reddit_signals,
                aggregated_signals
            )
            
            stage_name = STAGE_NAMES[stage]
            
            logger.info(f"✅ Classified as: {stage_name} (confidence: {base_confidence:.2f})")
            
            # === STEP 3: AI Validation (Optional) ===
            logger.info("🤖 Validating with Gemini AI...")
            
            is_valid, confidence_adjustment, reasoning = await self.gemini_validator.validate_stage(
                trend_name,
                stage,
                google_signals,
                twitter_signals,
                reddit_signals,
                aggregated_signals
            )
            
            # Calculate final confidence
            final_confidence = self.classifier.calculate_confidence_score(
                base_confidence,
                aggregated_signals,
                google_signals
            )
            final_confidence *= confidence_adjustment
            final_confidence = max(0.0, min(1.0, final_confidence))
            
            logger.info(f"✅ Gemini validation: {reasoning} (adjustment: {confidence_adjustment:.2f})")
            logger.info(f"📊 Final confidence: {final_confidence:.2f}")
            
            # === STEP 4: Store in MongoDB ===
            logger.info("💾 Saving to database...")
            
            document_data = {
                "trend_id": str(ObjectId()),
                "trend_name": trend_name,
                "lifecycle_stage": int(stage),
                "stage_name": stage_name,
                "days_in_stage": 0,  # Will be calculated by DB
                "confidence": round(final_confidence, 2),
                "google_signals": google_signals.dict(),
                "twitter_signals": twitter_signals.dict(),
                "reddit_signals": reddit_signals.dict(),
                "aggregated_signals": aggregated_signals.dict()
            }
            
            trend_id = await lifecycle_db.upsert_lifecycle(document_data)
            
            # Get updated days_in_stage from DB
            updated_doc = await lifecycle_db.get_by_name(trend_name)
            days_in_stage = updated_doc.get("days_in_stage", 0) if updated_doc else 0
            
            logger.info(f"✅ Saved with trend_id: {trend_id}")
            
            # === STEP 5: Return Strict Contract ===
            response = TrendLifecycleResponse(
                trend_id=trend_id,
                trend_name=trend_name,
                lifecycle_stage=int(stage),
                stage_name=stage_name,
                days_in_stage=days_in_stage,
                confidence=round(final_confidence, 2)
            )
            
            logger.info(f"✅ Lifecycle detection complete: {stage_name} (Stage {stage})")
            logger.info(f"{'='*80}")
            logger.info(f"🎯 FINAL RESULT: {'REAL-TIME DATA ANALYSIS' if is_real_data else 'FALLBACK MODE'}")
            logger.info(f"   Data Sources: {data_source_status}")
            logger.info(f"   Confidence: {final_confidence:.2%}")
            logger.info(f"{'='*80}")
            
            return response
        
        except Exception as e:
            logger.error(f"❌ Lifecycle detection failed: {e}", exc_info=True)
            raise
    
    async def get_lifecycle_by_name(self, trend_name: str) -> Dict[str, Any]:
        """
        Retrieve stored lifecycle data by trend name
        """
        doc = await lifecycle_db.get_by_name(trend_name)
        
        if not doc:
            return {"error": "Trend not found"}
        
        return doc
    
    async def get_trends_by_stage(self, stage: int, limit: int = 50) -> list:
        """
        Get all trends in a specific lifecycle stage
        """
        return await lifecycle_db.get_by_stage(stage, limit)


# Singleton instance
lifecycle_service = LifecycleService()
