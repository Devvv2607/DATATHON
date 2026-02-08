"""
FastAPI Router for Early Decline Signal Detection
Integrates with Lifecycle Detection (Feature #1)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import logging
from datetime import datetime, timedelta
import random
from starlette.concurrency import run_in_threadpool

from decline_signals.models import (
    DeclineSignalRequest,
    DeclineSignalResponse,
    SignalBreakdown,
    DailyMetric,
    LifecycleInfo
)
from decline_signals.config import (
    get_sensitivity_for_stage,
    ENGAGEMENT_DROP_THRESHOLDS,
    VELOCITY_DECLINE_THRESHOLDS,
    CREATOR_DECLINE_THRESHOLDS,
    QUALITY_DECLINE_THRESHOLDS
)
from decline_signals.lifecycle_handler import resolve_lifecycle_stage
from decline_signals.signals.engagement_drop import calculate_engagement_drop
from decline_signals.signals.velocity_decline import calculate_velocity_decline
from decline_signals.signals.creator_decline import calculate_creator_decline
from decline_signals.signals.quality_decline import calculate_quality_decline
from decline_signals.aggregator import aggregate_signals
from decline_signals.decline_predictor import generate_decline_prediction
from notifications.service import EmailNotificationService
from notifications import config as notifications_config

router = APIRouter()
logger = logging.getLogger(__name__)


def generate_mock_metrics(trend_name: str, lifecycle_stage: int) -> List[DailyMetric]:
    """Generate realistic mock metrics based on lifecycle stage"""
    metrics = []
    days = 30
    
    for i in range(days):
        date_obj = datetime.now() - timedelta(days=(days - i))
        progress = i / days
        
        # Base engagement varies by stage
        if lifecycle_stage == 1:  # Emerging
            base_engagement = 1000 + (progress * 5000)
        elif lifecycle_stage == 2:  # Viral
            base_engagement = 10000 + (progress * 50000)
        elif lifecycle_stage == 3:  # Plateau
            base_engagement = 50000 + (random.random() * 10000)
        elif lifecycle_stage == 4:  # Decline
            base_engagement = 60000 - (progress * 40000)
        else:  # Death
            base_engagement = max(5000 - (progress * 4000), 500)
        
        engagement = int(base_engagement * (1 + random.uniform(-0.1, 0.1)))
        views = int(engagement * random.uniform(8, 12))
        posts = int(50 + random.uniform(-10, 10))
        creators = int(25 + random.uniform(-5, 5))
        
        metrics.append(DailyMetric(
            date=date_obj.strftime("%Y-%m-%d"),
            total_engagement=engagement,
            views=views,
            posts_count=posts,
            creators_count=creators,
            avg_creator_followers=random.uniform(5000, 50000),
            avg_comments_per_post=random.uniform(10, 100),
            avg_engagement_per_post=engagement / posts if posts > 0 else 0
        ))
    
    return metrics


class AnalyzeRequest(BaseModel):
    """Request model for analyze endpoint"""
    trend_name: str
    lifecycle_stage: int = 3
    stage_name: str = "Plateau"
    confidence: float = 0.85
    notify_email: str | None = None


@router.post("/analyze", response_model=DeclineSignalResponse)
async def analyze_decline_signals(request: AnalyzeRequest):
    """
    Analyze decline signals for a trend
    
    **Integration Point:** Receives lifecycle data from Feature #1
    
    **Returns:** Decline risk score with color-coded alert level
    """
    try:
        trend_name = request.trend_name
        lifecycle_stage = request.lifecycle_stage
        stage_name = request.stage_name
        confidence = request.confidence
        logger.info(f"🔍 Analyzing decline signals for: '{trend_name}' (Stage: {stage_name})")
        
        # Create lifecycle info from the input
        lifecycle_info = LifecycleInfo(
            trend_id=f"trend_{trend_name.lower().replace(' ', '_')}",
            trend_name=trend_name,
            lifecycle_stage=lifecycle_stage,
            stage_name=stage_name,
            days_in_stage=5,
            confidence=confidence
        )
        
        # Generate metrics based on lifecycle stage
        daily_metrics = generate_mock_metrics(trend_name, lifecycle_stage)
        
        # Resolve lifecycle thresholds
        resolved_stage, resolved_name, data_quality = resolve_lifecycle_stage(lifecycle_info.dict())
        sensitivity = get_sensitivity_for_stage(resolved_stage)
        
        logger.info(f"📊 Lifecycle: Stage {resolved_stage} ({resolved_name}), Sensitivity: {sensitivity}")
        
        # Calculate all 4 signals with thresholds (returns tuple of score, explanation)
        logger.info(f"\n🔬 CALCULATING SIGNALS:")
        
        engagement_score, engagement_explanation = calculate_engagement_drop(daily_metrics, sensitivity, ENGAGEMENT_DROP_THRESHOLDS)
        logger.info(f"   1️⃣ Engagement Drop: {engagement_score:.2f}/100")
        logger.info(f"      └─ {engagement_explanation}")
        
        velocity_score, velocity_explanation = calculate_velocity_decline(daily_metrics, sensitivity, VELOCITY_DECLINE_THRESHOLDS)
        logger.info(f"   2️⃣ Velocity Decline: {velocity_score:.2f}/100")
        logger.info(f"      └─ {velocity_explanation}")
        
        creator_score, creator_explanation = calculate_creator_decline(daily_metrics, sensitivity, CREATOR_DECLINE_THRESHOLDS)
        logger.info(f"   3️⃣ Creator Decline: {creator_score:.2f}/100")
        logger.info(f"      └─ {creator_explanation}")
        
        quality_score, quality_explanation = calculate_quality_decline(daily_metrics, sensitivity, QUALITY_DECLINE_THRESHOLDS)
        logger.info(f"   4️⃣ Quality Decline: {quality_score:.2f}/100")
        logger.info(f"      └─ {quality_explanation}")
        
        signal_breakdown = SignalBreakdown(
            engagement_drop=round(engagement_score, 2),
            velocity_decline=round(velocity_score, 2),
            creator_decline=round(creator_score, 2),
            quality_decline=round(quality_score, 2)
        )
        
        # Aggregate signals
        signal_dict = {
            "engagement_drop": engagement_score,
            "velocity_decline": velocity_score,
            "creator_decline": creator_score,
            "quality_decline": quality_score
        }
        
        logger.info(f"\n⚖️ SIGNAL AGGREGATION:")
        logger.info(f"   - Weights: Engagement=27%, Velocity=28%, Creator=25%, Quality=20%")
        logger.info(f"   - Inputs: {signal_dict}")
        
        decline_risk_score, alert_level, confidence_level = aggregate_signals(
            signal_dict, resolved_stage, data_quality
        )
        
        logger.info(f"   - Raw Risk Score: {decline_risk_score:.2f}/100")
        logger.info(f"   - Alert Level: {alert_level.upper()}")
        logger.info(f"   - Confidence: {confidence_level}")  # confidence_level is a string, not a number
        
        # === DEAD TREND DETECTION ===
        # Check if low scores actually mean DEAD (not safe)
        logger.info(f"\n🔍 DEAD TREND CHECK:")
        
        # Calculate average post age from timestamps
        from datetime import datetime
        current_year = datetime.now().year
        post_ages = []
        for metric in daily_metrics:
            if hasattr(metric, 'timestamp') and metric.timestamp:
                try:
                    post_date = datetime.fromisoformat(metric.timestamp.replace('Z', '+00:00'))
                    age_years = current_year - post_date.year
                    post_ages.append(age_years)
                except:
                    pass
        
        avg_post_age = sum(post_ages) / len(post_ages) if post_ages else 0
        logger.info(f"   - Average post age: {avg_post_age:.1f} years")
        logger.info(f"   - Lifecycle stage: {resolved_stage} ({resolved_name})")
        logger.info(f"   - All signals low: {all(score < 20 for score in signal_dict.values())}")
        
        # OVERRIDE 1: Death stage + low scores + old posts = DEAD TREND
        if (decline_risk_score < 30 and  # Currently showing GREEN
            resolved_stage == 5 and       # Death stage
            avg_post_age > 3):            # Posts are old (>3 years)
            
            logger.info(f"   ⚠️ DEAD TREND DETECTED: Overriding GREEN → RED")
            logger.info(f"      Reason: Death stage + low activity + old posts ({avg_post_age:.1f}y)")
            
            decline_risk_score = 85.0  # Force RED alert
            alert_level = "red"
            confidence_level = "high"  # We're confident it's dead
            
            # Update signal breakdown to reflect dead status
            signal_breakdown = SignalBreakdown(
                engagement_drop=round(85.0, 2),    # Dead = high drop
                velocity_decline=round(85.0, 2),   # Dead = no velocity
                creator_decline=round(85.0, 2),    # Dead = creators gone
                quality_decline=round(85.0, 2)     # Dead = low quality
            )
        
        # OVERRIDE 2: Death stage + very low engagement (proxy for old)
        elif (decline_risk_score < 30 and
              resolved_stage == 5 and
              avg_post_age == 0):  # No timestamp data (mock data)
            
            # Check if engagement is extremely low (proxy for dead)
            avg_engagement_per_post = sum(m.avg_engagement_per_post for m in daily_metrics) / len(daily_metrics)
            avg_views = sum(m.views for m in daily_metrics) / len(daily_metrics)
            engagement_rate = avg_engagement_per_post / avg_views if avg_views > 0 else 0
            
            logger.info(f"   - Avg engagement/post: {avg_engagement_per_post:.1f}")
            logger.info(f"   - Avg views: {avg_views:.1f}")
            logger.info(f"   - Engagement rate: {engagement_rate:.1%}")
            
            if engagement_rate < 0.3 or avg_views < 500:  # Very low engagement or views
                logger.info(f"   ⚠️ DEAD TREND DETECTED (proxy): Overriding GREEN → ORANGE")
                logger.info(f"      Reason: Death stage + very low engagement/views")
                
                decline_risk_score = 75.0  # Force ORANGE alert
                alert_level = "orange"
                confidence_level = "medium"
                
                signal_breakdown = SignalBreakdown(
                    engagement_drop=round(75.0, 2),
                    velocity_decline=round(75.0, 2),
                    creator_decline=round(75.0, 2),
                    quality_decline=round(75.0, 2)
                )
        
        # NOTE: OVERRIDE 3 removed - lifecycle classification now properly detects viral/dead trends
        # No more hard-coded overrides needed!
        
        logger.info(f"   - Final Risk Score: {decline_risk_score:.2f}/100")
        logger.info(f"   - Final Alert: {alert_level.upper()}")
        
        # Generate time-to-die prediction (pass in correct order: metrics, score, stage)
        logger.info(f"\n⏱️ GENERATING TIME-TO-DIE PREDICTION...")
        prediction = generate_decline_prediction(
            daily_metrics, decline_risk_score, resolved_stage
        )
        time_to_die = prediction.get("time_to_critical", {}).get("days_to_critical") if prediction else None
        
        if time_to_die is not None and time_to_die < 7:
            to_email = request.notify_email or notifications_config.DEFAULT_ALERT_TO_EMAIL
            try:
                service = EmailNotificationService()
                result = await run_in_threadpool(
                    service.send_decline_days_alert,
                    to_email=to_email,
                    trend_name=trend_name,
                    days_to_critical=int(time_to_die),
                )
                logger.info(f"📧 Decline email notification result: to={to_email}, result={result}")
            except Exception as e:
                logger.error(f"❌ Failed to send decline email notification: {e}")
        
        logger.info(f"   - Days to Critical: {time_to_die} days")
        logger.info(f"   - Full Prediction: {prediction}")
        
        logger.info(f"\n" + "="*80)
        logger.info(f"📤 FINAL OUTPUT:")
        logger.info(f"   - Risk Score: {decline_risk_score:.2f}/100")
        logger.info(f"   - Alert Level: {alert_level.upper()}")
        logger.info(f"   - Time to Die: {time_to_die} days")
        logger.info(f"   - Confidence: {confidence_level}")
        logger.info("="*80 + "\n")
        
        return DeclineSignalResponse(
            trend_id=lifecycle_info.trend_id,
            decline_risk_score=round(decline_risk_score, 2),
            alert_level=alert_level,
            signal_breakdown=signal_breakdown,
            timestamp=datetime.utcnow().isoformat() + "Z",
            confidence=confidence_level,
            data_quality=data_quality,
            time_to_die=time_to_die
        )
        
    except Exception as e:
        logger.error(f"❌ Decline signal analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-from-lifecycle", response_model=DeclineSignalResponse)
async def analyze_from_lifecycle_output(lifecycle_output: dict):
    """
    Analyze decline signals directly from lifecycle detection output
    
    **Input Format:**
    ```json
    {
        "trend_id": "12345",
        "trend_name": "Grimace Shake",
        "lifecycle_stage": 2,
        "stage_name": "Viral Explosion",
        "days_in_stage": 5,
        "confidence": 0.85
    }
    ```
    """
    return await analyze_decline_signals(
        AnalyzeRequest(
            trend_name=lifecycle_output.get("trend_name"),
            lifecycle_stage=lifecycle_output.get("lifecycle_stage", 3),
            stage_name=lifecycle_output.get("stage_name", "Plateau"),
            confidence=lifecycle_output.get("confidence", 0.85),
        )
    )
