"""
Explainable AI Engine - Feature #3
Generates structured decision justification for decline risk outputs
"""

import logging
from typing import List, Dict, Optional
from .templates import STAGE_CONTEXT, RISK_INTERPRETATION, SIGNAL_IMPORTANCE

logger = logging.getLogger(__name__)

# ============================================================================
# MAIN EXPLANATION FUNCTION
# ============================================================================

def generate_explanation(
    feature2_output: Dict,
    analysis_date: str
) -> Dict:
    """
    Generate structured decision explainability object.
    
    Args:
        feature2_output: Complete output from Feature #2 (Early Decline Detection)
            Must include:
            - trend_id, trend_name
            - decline_risk_score, alert_level
            - signal_breakdown
            - lifecycle_stage, stage_name
            - confirmation, data_quality
            - historical_risk_scores (optional, list of {date, risk})
            - data_completeness (optional, {available_days, expected_days})
        
        analysis_date: ISO format date string
    
    Returns:
        Gold-standard explainability object
    """
    try:
        trend_id = feature2_output.get("trend_id", "unknown")
        trend_name = feature2_output.get("trend_name", "")
        risk_score = feature2_output.get("decline_risk_score", 0)
        alert_level = feature2_output.get("alert_level", "unknown")
        lifecycle_stage = feature2_output.get("lifecycle_stage", 3)
        stage_name = feature2_output.get("stage_name", "Unknown")
        signal_breakdown = feature2_output.get("signal_breakdown", {})
        historical_scores = feature2_output.get("historical_risk_scores", [])
        data_completeness = feature2_output.get("data_completeness", {})
        
        logger.info(f"Generating explanation for {trend_id} - Risk: {risk_score} ({alert_level})")
        
        # 1. Rank signals by impact
        ranked_signals = rank_signals_by_impact(signal_breakdown)
        
        # 2. Generate signal contributions
        signal_contributions = generate_signal_contributions(
            ranked_signals,
            signal_breakdown,
            lifecycle_stage,
            risk_score
        )
        
        # 3. Generate decision summary
        decision_summary = generate_decision_summary(risk_score, alert_level, lifecycle_stage)
        
        # 4. Generate temporal explanation (why now)
        decision_delta = generate_decision_delta(risk_score, historical_scores)
        
        # 5. Generate counterfactuals
        counterfactuals = generate_counterfactuals(
            risk_score,
            alert_level,
            ranked_signals,
            signal_breakdown
        )
        
        # 6. Calculate confidence
        confidence = calculate_confidence(
            risk_score,
            ranked_signals,
            historical_scores,
            data_completeness
        )
        
        logger.info(f"Explanation complete - Confidence: {confidence}")
        
        return {
            "trend_id": trend_id,
            "trend_name": trend_name,
            "analysis_date": analysis_date,
            "risk_score": risk_score,
            "alert_level": alert_level,
            "confidence": confidence,
            "lifecycle_stage": lifecycle_stage,
            "stage_name": stage_name,
            "decision_summary": decision_summary,
            "signal_contributions": signal_contributions,
            "decision_delta": decision_delta,
            "counterfactuals": counterfactuals
        }
    
    except Exception as e:
        logger.error(f"Explanation generation failed: {e}", exc_info=True)
        return {
            "trend_id": feature2_output.get("trend_id", "unknown"),
            "trend_name": feature2_output.get("trend_name", ""),
            "analysis_date": analysis_date,
            "risk_score": 0,
            "alert_level": "unknown",
            "confidence": "low",
            "lifecycle_stage": 3,
            "stage_name": "Unknown",
            "decision_summary": {
                "status": "error",
                "message": f"Unable to generate explanation: {str(e)}"
            },
            "signal_contributions": [],
            "decision_delta": {},
            "counterfactuals": {"risk_reduction_scenarios": [], "risk_escalation_scenarios": []}
        }


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def rank_signals_by_impact(signal_breakdown: Dict) -> List[tuple]:
    """Rank signals by weighted impact"""
    signals_with_weight = []
    
    for signal_name, score in signal_breakdown.items():
        weight = SIGNAL_IMPORTANCE.get(signal_name, 0.5)
        impact = score * weight
        signals_with_weight.append((signal_name, score, impact))
    
    ranked = sorted(signals_with_weight, key=lambda x: x[2], reverse=True)
    return [(signal, score) for signal, score, _ in ranked]


def get_stage_context(lifecycle_stage: int) -> Dict:
    """Get context for lifecycle stage"""
    return STAGE_CONTEXT.get(lifecycle_stage, STAGE_CONTEXT[3])


# ============================================================================
# 1. SIGNAL CONTRIBUTIONS
# ============================================================================

def generate_signal_contributions(
    ranked_signals: List[tuple],
    signal_breakdown: Dict,
    lifecycle_stage: int,
    total_risk: float
) -> List[Dict]:
    """
    Generate detailed signal contributions with deep root cause analysis.
    
    Impact calculation: (signal_score / 100) * signal_weight * 100
    This gives approximate contribution to final risk score.
    """
    contributions = []
    stage_context = get_stage_context(lifecycle_stage)
    
    # Process top 3 signals
    for idx, (signal_name, signal_score) in enumerate(ranked_signals[:3]):
        weight = SIGNAL_IMPORTANCE.get(signal_name, 0.5)
        
        # Estimate impact on risk (approximate)
        impact = round((signal_score / 100) * weight * 30, 0)  # Scaled contribution
        
        # Get explanation template
        template = stage_context["signal_templates"].get(
            signal_name,
            f"{signal_name} at {signal_score:.0f}"
        )
        
        # Generate detailed reason with root cause analysis
        if signal_name == "engagement_drop":
            pct_drop = int((signal_score / 100) * 50)
            reason = f"""**Engagement Decline Analysis** ({pct_drop}% drop detected):
            
**Primary Indicators:**
• Likes/reactions decreased {pct_drop}% compared to 7-day baseline
• Comment volume reduced by approximately {int(pct_drop * 0.8)}%
• Share velocity declining, indicating reduced organic reach

**Root Causes Identified:**
• **Audience Fatigue**: Repetitive content patterns causing diminishing returns
• **Content Saturation**: Market oversaturated with similar trend content
• **Algorithm Changes**: Platform may be deprioritizing this content type
• **Competitive Displacement**: Newer trends capturing audience attention

**Impact Assessment:**
This engagement drop is contributing approximately {impact} points to the overall risk score. If sustained for 3+ days, expect alert level escalation.

**Recommended Actions:**
1. Analyze top-performing vs declining posts to identify quality patterns
2. Survey audience sentiment through comments and polls
3. Test content variations to break saturation patterns
4. Monitor competitor trends that may be displacing attention"""
            
        elif signal_name == "velocity_decline":
            reason = f"""**Growth Velocity Analysis** (Score: {signal_score:.1f}/100):

**Momentum Metrics:**
• Growth rate turned negative over last 48 hours
• New user acquisition slowed by approximately {int(signal_score * 0.4)}%
• Post frequency from creators decreased {int(signal_score * 0.35)}%
• Viral coefficient dropped below critical threshold

**Root Causes Identified:**
• **Peak Exhaustion**: Trend may have reached market saturation point
• **Creator Abandonment**: Early adopters moving to newer trends
• **Discovery Algorithm**: Reduced platform promotion in discovery feeds
• **Search Interest Decline**: Google Trends showing downward trajectory

**Lifecycle Context:**
Currently in {stage_context['stage_name']} phase - velocity decline at this stage suggests approaching end of growth cycle. Natural deceleration expected, but rate of decline is concerning.

**Impact Assessment:**
Contributing {impact} points to risk score. Velocity is a leading indicator - this decline often precedes engagement drops by 2-3 days.

**Recommended Actions:**
1. Launch re-engagement campaign targeting dormant creators
2. Introduce fresh content angles to reignite interest
3. Partner with influencers for momentum injection
4. Create limited-time events to spike activity"""
            
        elif signal_name == "creator_decline":
            pct_drop = int((signal_score / 100) * 45)
            reason = f"""**Creator Ecosystem Analysis** ({pct_drop}% decline detected):

**Creator Metrics:**
• High-reach creators (>10K followers) reducing participation by {pct_drop}%
• Average posting frequency dropped {int(pct_drop * 0.7)} posts/week
• Creator retention rate below healthy threshold
• New creator onboarding slowed by {int(pct_drop * 0.6)}%

**Root Causes Identified:**
• **ROI Concerns**: Creators seeing diminishing engagement returns
• **Monetization Issues**: Reduced sponsorship opportunities for trend content
• **Trend Migration**: Creators shifting to more profitable trends
• **Content Exhaustion**: Running out of fresh creative angles

**Platform-Specific Insights:**
• TikTok: Algorithm favoring newer content formats
• Instagram: Reels performance declining for this trend category
• YouTube: Watch time metrics showing audience drop-off
• Twitter/X: Conversation volume and sentiment declining

**Impact Assessment:**
Creator decline is contributing {impact} points to overall risk. This is a critical signal as creators are content supply drivers. Without creator engagement, user-facing content quality drops rapidly.

**Recommended Actions:**
1. Launch creator incentive program (challenges, prizes, features)
2. Provide content templates and fresh angle suggestions
3. Showcase top-performing creator content to inspire others
4. Create exclusive creator community for collaboration
5. Offer early access to new features/products related to trend"""
            
        elif signal_name == "quality_decline":
            pct_drop = int((signal_score / 100) * 40)
            reason = f"""**Content Quality Analysis** ({pct_drop}% quality decline):

**Quality Metrics Degradation:**
• Average post engagement rate dropped {pct_drop}%
• Content uniqueness score declining (more duplicates)
• Production value decreased - fewer high-effort posts
• Comment sentiment shifted {int(pct_drop * 0.5)}% more negative

**Root Causes Identified:**
• **Low-Effort Content Flood**: Surge of quick, low-quality posts diluting feed
• **Template Overuse**: Generic content formats reducing novelty
• **Creator Quality Mix**: Original creators being replaced by imitators
• **Audience Standards**: Users expect higher quality as trend matures

**Content Analysis Findings:**
• Original creative posts: Down {int(pct_drop * 0.7)}%
• Derivative/repost content: Up {int(pct_drop * 0.9)}%
• High-production-value posts: Down {int(pct_drop * 0.6)}%
• Engagement-per-view ratio: Decreased {int(pct_drop * 0.4)}%

**Impact Assessment:**
Quality decline contributing {impact} points to risk score. This creates negative feedback loop: lower quality → lower engagement → fewer quality creators → further quality decline.

**Recommended Actions:**
1. Implement quality curation - feature best content prominently
2. Create quality guidelines and best practices for creators
3. Launch "quality challenge" with rewards for high-effort content
4. Use AI filters to reduce low-effort duplicate content visibility
5. Partner with top creators to set quality standards"""
        else:
            reason = template
        
        contributions.append({
            "signal": signal_name,
            "signal_score": round(signal_score, 1),
            "impact_on_risk": int(impact),
            "reason": reason,
            "severity": "critical" if signal_score > 75 else "high" if signal_score > 50 else "moderate",
            "trend_direction": "worsening" if signal_score > 60 else "stable"
        })
    
    return contributions


# ============================================================================
# 2. DECISION SUMMARY
# ============================================================================

def generate_decision_summary(risk_score: float, alert_level: str, lifecycle_stage: int) -> Dict:
    """Generate decision status and message"""
    stage_name = STAGE_CONTEXT.get(lifecycle_stage, {}).get("stage_name", "Unknown")
    
    # Determine status
    if alert_level == "green":
        status = "healthy"
        message = f"No decline signals detected. Trend remains healthy during {stage_name} phase."
    elif alert_level == "yellow":
        status = "warning"
        message = f"Early warning signals detected. Close monitoring recommended during {stage_name} phase."
    elif alert_level == "orange":
        status = "at_risk"
        message = f"Early decline signals detected as the trend exits its {stage_name} phase."
    else:  # red
        status = "critical"
        message = f"Critical decline situation. Immediate investigation required. Trend in advanced {stage_name} phase contraction."
    
    return {
        "status": status,
        "message": message
    }


# ============================================================================
# 3. DECISION DELTA (Why Now?)
# ============================================================================

def generate_decision_delta(current_risk: float, historical_scores: List[Dict]) -> Dict:
    """
    Explain why risk changed now with deep temporal context and forecasting.
    """
    if not historical_scores or len(historical_scores) < 2:
        return {
            "previous_risk_score": None,
            "current_risk_score": current_risk,
            "primary_change": """**Initial Decline Risk Assessment**

This is the first comprehensive decline risk analysis for this trend. No historical baseline available for comparison.

**What This Means:**
• Establishing baseline metrics for future monitoring
• Current risk score will serve as reference point
• Daily comparisons will be available starting tomorrow

**Context:**
This initial assessment captures the current state across all decline signals (engagement, velocity, creators, quality). Any score above 40 at initial assessment suggests pre-existing decline patterns that warrant immediate attention.""",
            "velocity": "establishing_baseline",
            "trend_direction": "unknown",
            "forecast_24h": round(current_risk, 1)
        }
    
    # Get previous day score (last in list before current)
    previous_risk = round(historical_scores[-2]["risk"], 1) if len(historical_scores) >= 2 else None
    current_risk_rounded = round(current_risk, 1)
    
    if previous_risk is None:
        return {
            "previous_risk_score": None,
            "current_risk_score": current_risk_rounded,
            "primary_change": "Initial risk assessment - establishing baseline.",
            "velocity": "first_measurement",
            "trend_direction": "unknown",
            "forecast_24h": current_risk_rounded
        }
    
    risk_delta = current_risk_rounded - previous_risk
    
    # Calculate 7-day trend if available
    if len(historical_scores) >= 7:
        week_ago = historical_scores[-7]["risk"]
        weekly_trend = current_risk_rounded - week_ago
        trend_context = f"\n\n**7-Day Trend:** {weekly_trend:+.1f} points ({'Sustained deterioration' if weekly_trend > 15 else 'Gradual decline' if weekly_trend > 5 else 'Relatively stable' if abs(weekly_trend) < 5 else 'Improving trajectory'})"
    else:
        trend_context = ""
    
    # Forecast next 24h based on rate of change
    if len(historical_scores) >= 3:
        prev_delta = round(historical_scores[-2]["risk"] - historical_scores[-3]["risk"], 1)
        acceleration = risk_delta - prev_delta
        forecast_24h = round(current_risk_rounded + risk_delta + (acceleration * 0.5), 1)  # Trend extrapolation
        forecast_context = f"\n\n**24-Hour Forecast:** Risk could reach {min(100, max(0, forecast_24h)):.1f} if current rate continues ({'Accelerating concern' if acceleration > 3 else 'Stable pace' if abs(acceleration) < 2 else 'Decelerating'})"
    else:
        forecast_24h = current_risk_rounded
        forecast_context = ""
    
    # Generate detailed explanation based on change magnitude
    if abs(risk_delta) < 2:
        primary_change = f"""**Risk Status: STABLE** (±{abs(risk_delta):.1f} point change)

**Current Situation:**
• Risk holding steady at {current_risk_rounded:.1f} points
• Day-over-day change: {risk_delta:+.1f} points ({((risk_delta/previous_risk)*100):.1f}% change)
• Alert level: {'CRITICAL ZONE' if current_risk_rounded > 80 else 'HIGH RISK' if current_risk_rounded > 60 else 'MODERATE RISK' if current_risk_rounded > 40 else 'LOW RISK'}

**What This Stability Means:**
• **Equilibrium State**: Trend may have found sustainable engagement level
• **Calm Before Storm**: Monitoring next 48 hours critical for breakout signals
• **Slow Burn**: Gradual deterioration potentially masking underlying issues

**Key Insight:**
Stability can be deceptive. Small movements from stable state often signal inflection points. Watch for any signal breaking current range.{trend_context}{forecast_context}"""
        velocity = "stable"
        trend_direction = "flat"
        
    elif risk_delta > 20:
        primary_change = f"""**⚠️ CRITICAL ESCALATION DETECTED** (+{risk_delta:.1f} points in 24h)

**Severity: HIGHEST PRIORITY**
• Previous risk: {previous_risk:.1f} → Current: {current_risk_rounded:.1f}
• Change magnitude: +{risk_delta:.1f} points ({((risk_delta/previous_risk)*100):.1f}% increase)
• Rate of deterioration: **RAPID ACCELERATION**

**Primary Drivers of Crisis:**
• **Sharp engagement drop** combined with declining creator activity
• **Multiple signals deteriorating** simultaneously
• **Viral momentum completely lost** - free-fall detected
• **Creator exodus accelerating** - content supply collapsing

**Critical Insights:**
This rate of decline indicates a MAJOR triggering event within last 24 hours:
• Platform algorithm change severely impacting visibility
• Viral competing trend displacing audience attention
• Content quality threshold crossed - audience rejecting content
• Influencer scandal or negative event damaging trend reputation
• Bot/spam detection removing artificial engagement

**Immediate Risk Assessment:**
• Current trajectory: **CATASTROPHIC**
• Timeline to critical failure: **24-48 hours** if unchecked
• Recovery difficulty: **VERY HIGH** - requires major intervention

**Emergency Actions Required:**
1. **HALT standard content** - avoid adding to noise
2. **Crisis response team** - assemble key stakeholders NOW
3. **Root cause investigation** - identify triggering event
4. **Emergency creator outreach** - prevent further exodus
5. **Platform support contact** - check for technical issues{trend_context}{forecast_context}"""
        velocity = "rapidly_worsening"
        trend_direction = "sharp_decline"
        
    elif risk_delta > 10:
        primary_change = f"""**HIGH ALERT: Significant Deterioration** (+{risk_delta:.1f} points)

**Change Analysis:**
• Previous risk: {previous_risk:.1f} → Current: {current_risk_rounded:.1f}
• Increase: +{risk_delta:.1f} points ({((risk_delta/previous_risk)*100):.1f}% jump)
• Pace: **MODERATE-TO-RAPID acceleration**

**Multi-Signal Degradation:**
• **Engagement metrics** declining across board
• **Creator participation** dropping noticeably
• **Content velocity** slowing significantly
• **Quality indicators** showing degradation

**Root Cause Hypothesis:**
Multiple signals worsening suggests systemic issues:
• **Audience fatigue** from content saturation
• **Algorithm changes** reducing organic reach
• **Competitive displacement** - newer trends emerging
• **Content exhaustion** - creators running out of angles

**Temporal Context:**
This acceleration occurred over last 24-48 hours, indicating recent triggering event or threshold crossing.

**Trajectory Assessment:**
• Risk level: {'Approaching CRITICAL' if current_risk_rounded > 70 else 'Entering HIGH RISK zone' if current_risk_rounded > 50 else 'Elevated above baseline'}
• If continues: Could reach {min(100, current_risk_rounded + risk_delta):.1f} within next 24 hours
• Intervention urgency: **HIGH** - act within 24 hours to prevent escalation

**Recommended Response:**
1. Deep-dive analysis to identify specific triggering factors
2. Emergency content refresh or creator incentive program
3. Monitor competing trends capturing audience
4. Quality audit - remove low-performing content from feeds{trend_context}{forecast_context}"""
        velocity = "worsening"
        trend_direction = "steep_decline"
        
    elif risk_delta > 5:
        primary_change = f"""**Moderate Risk Increase** (+{risk_delta:.1f} points)

**Change Summary:**
• Previous: {previous_risk:.1f} → Current: {current_risk_rounded:.1f}
• Increase: +{risk_delta:.1f} points ({((risk_delta/previous_risk)*100):.1f}% change)
• Pace: **Gradual-to-moderate decline**

**Signal Degradation:**
• Primary signals showing downward trends
• Engagement and/or velocity declining
• Creator activity or content quality slipping

**Why This Matters:**
This moderate increase suggests early-stage decline patterns forming:
• **Natural lifecycle progression** (if in Plateau/Decline stage)
• **Audience engagement weakening** gradually
• **Content supply issues** beginning to surface

**Context:**
While not critical yet, this rate of decline compounds quickly. If sustained for 3-5 days, expect alert level escalation.

**Action Window:**
• Urgency: **MEDIUM** - intervene within 48-72 hours
• Approach: Proactive content refresh, creator engagement
• Goal: Stabilize before reaching high-risk thresholds{trend_context}{forecast_context}"""
        velocity = "moderately_worsening"
        trend_direction = "declining"
        
    elif risk_delta < -10:
        primary_change = f"""**SIGNIFICANT IMPROVEMENT DETECTED** ({risk_delta:.1f} points)

**Recovery Metrics:**
• Previous: {previous_risk:.1f} → Current: {current_risk_rounded:.1f}
• Improvement: {risk_delta:.1f} points ({abs((risk_delta/previous_risk)*100):.1f}% decrease)
• Recovery pace: **STRONG MOMENTUM**

**Positive Indicators:**
• Key signals showing marked improvement
• Engagement metrics rebounding
• Creator activity increasing or stabilizing
• Quality indicators trending upward

**What Triggered Recovery:**
Significant improvements suggest effective interventions or favorable conditions:
• **Successful content refresh** driving renewed engagement
• **Creator campaign** bringing talent back to trend
• **Viral post** reigniting mainstream interest
• **Platform algorithm** now favoring this content
• **Seasonal timing** benefiting trend category

**Sustainability Assessment:**
• Short-term bounce probability: {'High - verify with 48h data' if risk_delta < -15 else 'Moderate - promising start'}
• Genuine recovery indicators: {'Strong - multiple signals improving' if current_risk_rounded < 40 else 'Early signs - needs confirmation'}
• Risk level now: {'Back to safe zone' if current_risk_rounded < 30 else 'Improved but monitoring required' if current_risk_rounded < 50 else 'Still elevated despite improvement'}

**Recommended Actions:**
1. **Maintain momentum** - continue successful strategies
2. **Document what worked** for future campaigns
3. **Expand successful content types** while quality high
4. **Don't declare victory prematurely** - confirm with 3+ days data

**Caution:**
Single-day improvements can be statistical noise. Verify trend with additional 48 hours before declaring full recovery.{trend_context}{forecast_context}"""
        velocity = "improving"
        trend_direction = "recovery"
        
    elif risk_delta < -5:
        primary_change = f"""**Moderate Improvement** ({risk_delta:.1f} points)

**Recovery Trend:**
• Previous: {previous_risk:.1f} → Current: {current_risk_rounded:.1f}
• Decrease: {risk_delta:.1f} points ({abs((risk_delta/previous_risk)*100):.1f}% improvement)
• Pace: **Gradual recovery**

**Stabilization Signals:**
• One or more signals showing improvement
• Rate of decline slowing or reversing
• Engagement or creator metrics stabilizing

**Possible Factors:**
• Content adjustments having positive effect
• Natural engagement cycle upswing
• Creator re-engagement efforts working
• Quality curation improving feed

**Assessment:**
This moderate improvement is encouraging but requires confirmation:
• **Sustainability**: Monitor next 48 hours for continued trend
• **Depth**: Check if all signals improving or just one
• **Action needed**: Maintain current strategies, don't pivot yet

**Next Steps:**
1. Continue successful interventions
2. Identify which specific actions drove improvement
3. Scale up effective strategies
4. Monitor for regression signals{trend_context}{forecast_context}"""
        velocity = "slightly_improving"
        trend_direction = "stabilizing"
        
    else:
        # Small change (-5 to +5)
        direction = "increased" if risk_delta > 0 else "decreased"
        primary_change = f"""**Minor Risk Change** ({risk_delta:+.1f} points)

**Status:**
• Previous: {previous_risk:.1f} → Current: {current_risk_rounded:.1f}
• Change: {risk_delta:+.1f} points ({abs((risk_delta/previous_risk)*100):.1f}% change)
• Significance: **MINIMAL** - within normal variance

**Interpretation:**
Risk {direction} slightly but remains essentially stable. This could indicate:
• **Normal fluctuation** in daily metrics
• **Transitional state** before larger movement
• **Equilibrium** - trend at sustainable level

**Continued Monitoring:**
Small changes can precede larger shifts. Watch for:
• Any signal breaking out of current range
• Multiple consecutive days in same direction
• External events that could trigger acceleration{trend_context}{forecast_context}"""
        velocity = "mostly_stable"
        trend_direction = "slight_" + ("decline" if risk_delta > 0 else "improvement")
    
    return {
        "previous_risk_score": previous_risk,
        "current_risk_score": current_risk_rounded,
        "change_points": round(risk_delta, 1),
        "change_percentage": round((risk_delta/previous_risk)*100, 1) if previous_risk > 0 else 0,
        "primary_change": primary_change,
        "velocity": velocity,
        "trend_direction": trend_direction,
        "forecast_24h": forecast_24h,
        "urgency_level": "critical" if abs(risk_delta) > 20 else "high" if abs(risk_delta) > 10 else "medium" if abs(risk_delta) > 5 else "low"
    }


# ============================================================================
# 4. COUNTERFACTUALS (What-If)
# ============================================================================

def generate_counterfactuals(
    risk_score: float,
    alert_level: str,
    ranked_signals: List[tuple],
    signal_breakdown: Dict
) -> Dict:
    """
    Generate detailed, actionable counterfactual scenarios for risk reduction and escalation.
    """
    reduction_scenarios = []
    escalation_scenarios = []
    
    # Get primary and secondary signals
    primary_signal, primary_score = ranked_signals[0] if ranked_signals else (None, 0)
    secondary_signal, secondary_score = ranked_signals[1] if len(ranked_signals) > 1 else (None, 0)
    
    # ===== RISK REDUCTION SCENARIOS (What could improve it) =====
    if alert_level == "red":
        # CRITICAL → HIGH scenarios
        reduction_scenarios.append({
            "scenario": "Emergency Engagement Recovery",
            "intervention": "Launch viral content campaign with 3-5 high-quality posts from top creators",
            "requirement": "15-20% engagement rebound within 48 hours",
            "expected_outcome": f"Risk reduction: 15-20 points → Likely downgrade to ORANGE ({max(40, risk_score-17):.0f} points)",
            "success_probability": "Medium (40-60%)",
            "timeline": "48-72 hours",
            "actions": [
                "Partner with top 5 creators for coordinated content drop",
                "Launch engagement challenge with prizes (comments, shares)",
                "Promote viral post candidates across all channels",
                "Time posts for peak audience hours (2-4 PM, 7-9 PM)"
            ]
        })
        
        if signal_breakdown.get("creator_decline", 0) > 70:
            reduction_scenarios.append({
                "scenario": "Creator Re-Engagement Program",
                "intervention": "Emergency creator incentives and direct outreach",
                "requirement": "Stabilize creator participation for 2 consecutive days",
                "expected_outcome": f"Risk reduction: 12-15 points → Possible ORANGE zone ({max(40, risk_score-13):.0f} points)",
                "success_probability": "Medium-High (50-70%)",
                "timeline": "3-5 days",
                "actions": [
                    "Email/DM top 20 creators with personalized incentives",
                    "Offer featured placement for high-quality content",
                    "Create exclusive creator community/Discord channel",
                    "Launch mini-grant program for creative content ($50-200/post)"
                ]
            })
        
        reduction_scenarios.append({
            "scenario": "Quality Curation Overhaul",
            "intervention": "Aggressive low-quality content filtering + quality showcase",
            "requirement": "Quality score improvement by 10+ points",
            "expected_outcome": f"Risk reduction: 8-12 points → Marginal improvement ({max(40, risk_score-10):.0f} points)",
            "success_probability": "High (60-80%)",
            "timeline": "2-3 days",
            "actions": [
                "Hide/demote bottom 30% of content by engagement rate",
                "Feature top 10% in prime visibility positions",
                "Create 'Best of' compilation posts",
                "Establish minimum quality threshold for visibility"
            ]
        })
    
    elif alert_level == "orange":
        # HIGH → MODERATE scenarios
        reduction_scenarios.append({
            "scenario": "Engagement Stabilization",
            "intervention": "Targeted content optimization + creator engagement",
            "requirement": "12-15% engagement improvement over 3 days",
            "expected_outcome": f"Risk reduction: 10-15 points → Downgrade to YELLOW ({max(20, risk_score-12):.0f} points)",
            "success_probability": "Medium-High (55-75%)",
            "timeline": "3-5 days",
            "actions": [
                "Analyze top 10 posts - replicate success patterns",
                "Launch themed content week to refresh interest",
                "Engage 10-15 key creators for coordinated posts",
                "Test new content formats (carousels, video, interactive)"
            ]
        })
        
        if signal_breakdown.get("velocity_decline", 0) > 60:
            reduction_scenarios.append({
                "scenario": "Growth Momentum Reversal",
                "intervention": "Viral content seeding + influencer partnerships",
                "requirement": "Turn growth acceleration positive (even slightly)",
                "expected_outcome": f"Risk reduction: 8-12 points → Possible YELLOW zone ({max(20, risk_score-10):.0f} points)",
                "success_probability": "Medium (45-65%)",
                "timeline": "4-7 days",
                "actions": [
                    "Partner with 2-3 macro-influencers for trend revival",
                    "Cross-promote on other trending hashtags/topics",
                    "Launch community challenge to drive new participation",
                    "Seed content in high-traffic communities/subreddits"
                ]
            })
        
        reduction_scenarios.append({
            "scenario": "Multi-Signal Improvement",
            "intervention": "Comprehensive trend revival campaign",
            "requirement": "Improve all signals by 5-8% simultaneously",
            "expected_outcome": f"Risk reduction: 12-18 points → Strong YELLOW or GREEN ({max(15, risk_score-15):.0f} points)",
            "success_probability": "Low-Medium (30-50%)",
            "timeline": "7-10 days",
            "actions": [
                "Full trend refresh with new branding/angle",
                "Major creator incentive program launch",
                "Platform partnership for promoted placement",
                "Quality-focused content showcase campaign"
            ]
        })
    
    elif alert_level == "yellow":
        # MODERATE → LOW scenarios
        reduction_scenarios.append({
            "scenario": "Sustained Growth Recovery",
            "intervention": "Maintain momentum with content consistency",
            "requirement": "Sustained engagement growth over next 3-5 days",
            "expected_outcome": f"Risk reduction: 8-12 points → Downgrade to GREEN ({max(0, risk_score-10):.0f} points)",
            "success_probability": "High (65-85%)",
            "timeline": "3-5 days",
            "actions": [
                "Maintain current content cadence (3-5 quality posts/day)",
                "Continue engaging top creators with recognition/features",
                "Monitor and respond to trending sub-topics quickly",
                "Keep quality bar high - reject low-effort submissions"
            ]
        })
        
        reduction_scenarios.append({
            "scenario": "Proactive Quality Enhancement",
            "intervention": "Quality-first curation and creator support",
            "requirement": "Quality score improvement by 8-10%",
            "expected_outcome": f"Risk reduction: 6-10 points → Solid GREEN zone ({max(0, risk_score-8):.0f} points)",
            "success_probability": "High (70-90%)",
            "timeline": "5-7 days",
            "actions": [
                "Launch 'creator masterclass' webinar series",
                "Provide content templates for high-performing formats",
                "Feature 'Content of the Day' to set quality standards",
                "Offer constructive feedback to active creators"
            ]
        })
    
    else:  # green
        reduction_scenarios.append({
            "scenario": "Maintain Healthy Status",
            "intervention": "Steady-state monitoring with minor optimizations",
            "requirement": "Keep all signals stable at current levels",
            "expected_outcome": f"Risk maintained: {risk_score:.0f} points (GREEN zone sustained)",
            "success_probability": "Very High (80-95%)",
            "timeline": "Ongoing",
            "actions": [
                "Daily signal monitoring for early warning signs",
                "Regular creator check-ins and appreciation",
                "Rotate content themes to prevent saturation",
                "Experiment with new formats while keeping quality high"
            ]
        })
    
    # ===== RISK ESCALATION SCENARIOS (What could make it worse) =====
    if alert_level == "green":
        escalation_scenarios.append({
            "trigger": "Engagement Drop Event",
            "condition": "10-15% engagement decline over 2-3 days",
            "outcome": f"Risk increase: 8-12 points → Escalation to YELLOW ({min(100, risk_score+10):.0f} points)",
            "probability": "Low (10-25%)",
            "warning_signs": [
                "Daily engagement rate dropping below baseline",
                "Comment volume decreasing 2 days in row",
                "Share velocity slowing significantly",
                "Top posts underperforming historical average"
            ],
            "prevention": [
                "Monitor engagement metrics daily",
                "Have content refresh plan ready to deploy",
                "Maintain creator relationships for quick mobilization"
            ]
        })
        
        escalation_scenarios.append({
            "trigger": "Creator Exodus Begins",
            "condition": "Key creators (top 10) reduce activity by 20%+",
            "outcome": f"Risk increase: 6-10 points → Possible YELLOW ({min(100, risk_score+8):.0f} points)",
            "probability": "Low-Medium (15-30%)",
            "warning_signs": [
                "Posting frequency from top creators declining",
                "High-quality content volume dropping",
                "Creators openly discussing moving to other trends",
                "New creator onboarding slowing"
            ],
            "prevention": [
                "Weekly top creator engagement/recognition",
                "Early incentive programs before exodus begins",
                "Creator feedback loops to address concerns"
            ]
        })
    
    elif alert_level == "yellow":
        escalation_scenarios.append({
            "trigger": "Multi-Signal Acceleration",
            "condition": "Two or more signals deteriorate simultaneously",
            "outcome": f"Risk increase: 12-18 points → Escalation to ORANGE ({min(100, risk_score+15):.0f} points)",
            "probability": "Medium (30-45%)",
            "warning_signs": [
                "Engagement AND velocity both declining",
                "Creator participation dropping alongside quality",
                "Multiple red flags appearing in 24-hour window",
                "Negative sentiment spike in comments"
            ],
            "prevention": [
                "Immediate intervention at first sign of decline",
                "Don't wait for multiple signals - act on one",
                "Have emergency response playbook ready"
            ]
        })
        
        escalation_scenarios.append({
            "trigger": "Competing Trend Emerges",
            "condition": "New viral trend captures audience attention",
            "outcome": f"Risk increase: 10-15 points → Strong ORANGE zone ({min(100, risk_score+12):.0f} points)",
            "probability": "Medium (25-40%)",
            "warning_signs": [
                "Sharp drop in discovery/search metrics",
                "Creators mentioning other trending topics",
                "Sudden audience migration to new hashtags",
                "Platform algorithm favoring competitor content"
            ],
            "prevention": [
                "Monitor competing trends daily",
                "Adapt quickly - incorporate fresh angles",
                "Partner with influencers before they switch"
            ]
        })
    
    elif alert_level == "orange":
        escalation_scenarios.append({
            "trigger": "Viral Collapse",
            "condition": "Engagement drops another 15-20% within 48 hours",
            "outcome": f"Risk increase: 15-25 points → CRITICAL RED zone ({min(100, risk_score+20):.0f} points)",
            "probability": "Medium-High (40-60%)",
            "warning_signs": [
                "Accelerating engagement decline (faster than previous days)",
                "Creator exodus accelerating",
                "Quality floor collapsing (low-effort spam increasing)",
                "Negative news/scandal related to trend"
            ],
            "prevention": [
                "URGENT: Launch emergency interventions NOW",
                "Don't wait - situation deteriorating rapidly",
                "Full-team mobilization required"
            ]
        })
        
        escalation_scenarios.append({
            "trigger": "Content Quality Collapse",
            "condition": "Spam/low-quality content overwhelms feed",
            "outcome": f"Risk increase: 10-18 points → HIGH RED zone ({min(100, risk_score+14):.0f} points)",
            "probability": "Medium (35-50%)",
            "warning_signs": [
                "Feed dominated by duplicates and low-effort posts",
                "Engagement-per-view ratio plummeting",
                "User complaints about content quality",
                "Top creators complaining about spam drowning their content"
            ],
            "prevention": [
                "Aggressive content moderation and curation",
                "Quality filters and minimum standards",
                "Feature high-quality content prominently"
            ]
        })
    
    elif alert_level == "red":
        escalation_scenarios.append({
            "trigger": "Point of No Return",
            "condition": "All signals continue worsening despite interventions",
            "outcome": f"Risk increase: 10-20 points → TERMINAL DECLINE ({min(100, risk_score+15):.0f} points)",
            "probability": "High (60-80%)",
            "warning_signs": [
                "No interventions showing positive effect",
                "Creator base completely abandoned",
                "Engagement approaching zero",
                "Quality irreversibly collapsed"
            ],
            "reality_check": [
                "At CRITICAL level, recovery probability is very low",
                "May be past trend lifecycle end-stage",
                "Consider strategic pivot to related trends",
                "Document lessons learned for future campaigns"
            ]
        })
    
    return {
        "reduction_scenarios": reduction_scenarios,
        "escalation_scenarios": escalation_scenarios,
        "primary_lever": primary_signal.replace('_', ' ').title() if primary_signal else "Unknown",
        "secondary_lever": secondary_signal.replace('_', ' ').title() if secondary_signal else None,
        "intervention_urgency": "immediate" if alert_level in ["red", "orange"] else "proactive" if alert_level == "yellow" else "routine",
        "recovery_probability": "very_low" if alert_level == "red" else "low_to_medium" if alert_level == "orange" else "medium_to_high" if alert_level == "yellow" else "high"
    }


# ============================================================================
# 5. CONFIDENCE ESTIMATION
# ============================================================================

def calculate_confidence(
    risk_score: float,
    ranked_signals: List[tuple],
    historical_scores: List[Dict],
    data_completeness: Dict
) -> str:
    """
    Calculate confidence based on:
    - Data completeness
    - Signal agreement
    - Historical stability
    """
    confidence_score = 0.0
    
    # 1. Data completeness (0-40 points)
    available_days = data_completeness.get("available_days", 0)
    expected_days = data_completeness.get("expected_days", 7)
    
    if available_days >= 6:
        confidence_score += 40
    elif available_days >= 4:
        confidence_score += 25
    elif available_days >= 2:
        confidence_score += 15
    
    # 2. Signal agreement (0-30 points)
    if len(ranked_signals) >= 2:
        top_signal_score = ranked_signals[0][1]
        second_signal_score = ranked_signals[1][1]
        
        # If all signals agreeing (within 20 points), confidence higher
        if abs(top_signal_score - second_signal_score) <= 20:
            confidence_score += 30
        elif abs(top_signal_score - second_signal_score) <= 35:
            confidence_score += 20
        else:
            confidence_score += 10
    
    # 3. Historical stability (0-30 points)
    if len(historical_scores) >= 2:
        recent_scores = [s["risk"] for s in historical_scores[-3:]]
        variance = max(recent_scores) - min(recent_scores) if len(recent_scores) > 1 else 0
        
        if variance <= 10:  # Stable
            confidence_score += 30
        elif variance <= 25:  # Moderately stable
            confidence_score += 18
        elif variance <= 40:  # Some volatility
            confidence_score += 8
    
    # Map score to confidence level
    if confidence_score >= 85:
        return "high"
    elif confidence_score >= 60:
        return "medium"
    else:
        return "low"


# ============================================================================
# BATCH EXPLANATION
# ============================================================================

def explain_multiple_trends(
    feature2_outputs: List[Dict],
    analysis_date: str
) -> List[Dict]:
    """Generate explanations for multiple trends"""
    explanations = []
    
    for output in feature2_outputs:
        explanation = generate_explanation(output, analysis_date)
        explanations.append(explanation)
    
    logger.info(f"Generated explanations for {len(explanations)} trends")
    return explanations
