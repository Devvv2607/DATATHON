"""
Explainable Trend Intelligence Engine (Twitter/X Edition)
Analyzes trend decline on Twitter/X with confidence-scored causal analysis.
"""

import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime, timedelta
import math


class SeverityLevel(str, Enum):
    """Severity classification for trend decline."""
    STABLE = "STABLE"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    COLLAPSED = "COLLAPSED"


class TrendStatus(str, Enum):
    """Classification of trend momentum."""
    GROWING = "GROWING"
    STABLE = "STABLE"
    DECLINING = "DECLINING"
    COLLAPSED = "COLLAPSED"


@dataclass
class DeclineCause:
    """Single detected cause of decline with confidence and evidence."""
    cause_type: str
    confidence: float  # 0.0 to 1.0
    severity_contribution: float  # How much this cause contributes to overall decline
    evidence: List[str]  # Specific metrics supporting this cause
    affected_platforms: List[str]  # Which platforms show this pattern
    business_explanation: str  # Non-technical summary


@dataclass
class RecommendedAction:
    """Actionable strategy for recovery or exit."""
    action_type: str  # "RECOVERY" or "EXIT"
    priority: str  # "HIGH", "MEDIUM", "LOW"
    description: str
    expected_impact: str
    timeframe: str
    platforms_targeted: List[str]


@dataclass
class TrendAnalysisResult:
    """Complete structured analysis output."""
    trend_name: str
    analysis_timestamp: str
    trend_status: str  # GROWING, STABLE, DECLINING, COLLAPSED
    decline_probability: float  # 0.0 to 1.0
    severity_level: str  # STABLE, WARNING, CRITICAL, COLLAPSED
    root_causes: List[DeclineCause]
    cross_platform_summary: Dict[str, Any]
    recommended_actions: List[RecommendedAction]
    confidence_in_analysis: float


class TrendAnalyzer:
    """Main class for trend decline analysis across platforms."""

    # Decline cause types
    CAUSE_TYPES = {
        "ENGAGEMENT_DECAY": "Engagement Decay",
        "CONTENT_SATURATION": "Content Saturation / Repetition Fatigue",
        "CREATOR_DISENGAGEMENT": "Creator Disengagement",
        "INFLUENCER_DROPOFF": "Influencer Activity Collapse",
        "POSTING_FREQUENCY_COLLAPSE": "Posting Frequency Collapse",
        "ALGORITHMIC_VISIBILITY": "Algorithmic Visibility Reduction",
        "AUDIENCE_FATIGUE": "Audience Fatigue",
        "COMPETING_TREND": "Competing Trend Emergence",
        "TEMPORAL_RELEVANCE": "Temporal Relevance Loss",
    }

    def __init__(self, min_confidence_threshold: float = 0.3):
        """
        Initialize analyzer.
        
        Args:
            min_confidence_threshold: Minimum confidence (0-1) to report a cause
        """
        self.min_confidence_threshold = min_confidence_threshold

    def analyze(self, metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze Twitter/X trend metrics and detect decline causes.
        
        Args:
            metrics_data: X/Twitter metrics structured data
            
        Returns:
            Dictionary with complete analysis (serializable to JSON)
        """
        trend_name = metrics_data.get("trend_name", "Unknown")
        
        # Extract X/Twitter metrics
        x_metrics = metrics_data.get("x", {})
        
        if not x_metrics:
            raise ValueError("X/Twitter metrics required for analysis")
        
        # Detect decline causes from X metrics
        detected_causes = self._detect_all_causes(x_metrics)
        
        # Calculate overall trend status and decline probability
        trend_status, decline_probability = self._calculate_trend_status(
            detected_causes, x_metrics
        )
        
        # Determine severity
        severity_level = self._determine_severity(decline_probability, detected_causes)
        
        # Generate platform summary
        platform_summary = self._generate_platform_summary(x_metrics)
        
        # Generate recommended actions
        recommended_actions = self._generate_actions(detected_causes, trend_status, severity_level)
        
        # Calculate analysis confidence
        analysis_confidence = self._calculate_analysis_confidence(
            detected_causes, x_metrics
        )
        
        # Build result object
        result = TrendAnalysisResult(
            trend_name=trend_name,
            analysis_timestamp=datetime.utcnow().isoformat() + "Z",
            trend_status=trend_status.value,
            decline_probability=round(decline_probability, 3),
            severity_level=severity_level.value,
            root_causes=detected_causes,
            cross_platform_summary=platform_summary,
            recommended_actions=recommended_actions,
            confidence_in_analysis=round(analysis_confidence, 3),
        )
        
        return self._serialize_result(result)

    def _detect_all_causes(
        self,
        x_metrics: Dict,
    ) -> List[DeclineCause]:
        """Detect all meaningful decline causes from X/Twitter metrics."""
        causes = []
        
        # 1. Engagement Decay
        engagement_cause = self._detect_engagement_decay(x_metrics)
        if engagement_cause and engagement_cause.confidence >= self.min_confidence_threshold:
            causes.append(engagement_cause)
        
        # 2. Content Saturation
        saturation_cause = self._detect_content_saturation(x_metrics)
        if saturation_cause and saturation_cause.confidence >= self.min_confidence_threshold:
            causes.append(saturation_cause)
        
        # 3. Creator Disengagement
        creator_cause = self._detect_creator_disengagement(x_metrics)
        if creator_cause and creator_cause.confidence >= self.min_confidence_threshold:
            causes.append(creator_cause)
        
        # 4. Influencer Drop-off
        influencer_cause = self._detect_influencer_dropoff(x_metrics)
        if influencer_cause and influencer_cause.confidence >= self.min_confidence_threshold:
            causes.append(influencer_cause)
        
        # 5. Posting Frequency Collapse
        posting_cause = self._detect_posting_collapse(x_metrics)
        if posting_cause and posting_cause.confidence >= self.min_confidence_threshold:
            causes.append(posting_cause)
        
        # 6. Algorithmic Visibility
        algo_cause = self._detect_algorithmic_visibility(x_metrics)
        if algo_cause and algo_cause.confidence >= self.min_confidence_threshold:
            causes.append(algo_cause)
        
        # 7. Audience Fatigue
        fatigue_cause = self._detect_audience_fatigue(x_metrics)
        if fatigue_cause and fatigue_cause.confidence >= self.min_confidence_threshold:
            causes.append(fatigue_cause)
        
        # 8. Temporal Relevance Loss
        temporal_cause = self._detect_temporal_loss(x_metrics)
        if temporal_cause and temporal_cause.confidence >= self.min_confidence_threshold:
            causes.append(temporal_cause)
        
        # Sort by confidence (descending)
        causes.sort(key=lambda x: x.confidence, reverse=True)
        return causes

    def _detect_engagement_decay(
        self, x_metrics: Dict
    ) -> Optional[DeclineCause]:
        """Detect if engagement (likes, retweets, comments) is declining."""
        evidences = []
        
        # X/Twitter engagement decay
        if x_metrics and "weekly_engagement_velocity" in x_metrics:
            velocity = x_metrics["weekly_engagement_velocity"]
            if velocity < -0.1:  # More than 10% weekly decline
                evidences.append(f"X engagement declining at {velocity:.1%} per week")
        
        if not evidences:
            return None
        
        confidence = min(1.0, 0.85)
        
        return DeclineCause(
            cause_type=self.CAUSE_TYPES["ENGAGEMENT_DECAY"],
            confidence=confidence,
            severity_contribution=confidence * 0.8,
            evidence=evidences,
            affected_platforms=["X"],
            business_explanation="Users are interacting less with content (fewer likes, retweets, comments). This suggests waning interest or reduced visibility.",
        )

    def _detect_content_saturation(
        self, x_metrics: Dict
    ) -> Optional[DeclineCause]:
        """Detect if trend is overexposed or repetitive."""
        evidences = []
        
        # X content saturation
        if x_metrics and "unique_content_ratio" in x_metrics:
            ratio = x_metrics["unique_content_ratio"]
            if ratio < 0.3:  # Less than 30% unique content
                evidences.append(f"Only {ratio:.0%} of posts are unique content (high repetition)")
        
        if not evidences:
            return None
        
        confidence = 0.72
        
        return DeclineCause(
            cause_type=self.CAUSE_TYPES["CONTENT_SATURATION"],
            confidence=confidence,
            severity_contribution=confidence * 0.75,
            evidence=evidences,
            affected_platforms=["X"],
            business_explanation="The trend has become oversaturated with repetitive content. Audiences are fatigued by lack of novelty and variation.",
        )

    def _detect_creator_disengagement(
        self, x_metrics: Dict
    ) -> Optional[DeclineCause]:
        """Detect if content creators are losing interest."""
        evidences = []
        
        # X posting decline
        if x_metrics and "posts_per_day" in x_metrics:
            curr = x_metrics["posts_per_day"].get("current", 0)
            prev = x_metrics["posts_per_day"].get("previous_period", curr)
            if prev > 0:
                decline = (curr - prev) / prev
                if decline < -0.3:  # >30% decline in posting
                    evidences.append(f"Daily posts down {decline:.1%}")
        
        if not evidences:
            return None
        
        confidence = 0.65
        
        return DeclineCause(
            cause_type=self.CAUSE_TYPES["CREATOR_DISENGAGEMENT"],
            confidence=confidence,
            severity_contribution=confidence * 0.85,
            evidence=evidences,
            affected_platforms=["X"],
            business_explanation="Content creators are posting less frequently. This signals reduced interest in participating with the trend.",
        )

    def _detect_influencer_dropoff(self, x_metrics: Dict) -> Optional[DeclineCause]:
        """Detect if influencers have stopped engaging with the trend."""
        evidences = []
        
        if not x_metrics:
            return None
        
        # Top account activity
        if "top_accounts_participation" in x_metrics:
            top_accounts = x_metrics["top_accounts_participation"]
            if isinstance(top_accounts, dict):
                active = top_accounts.get("current", 0)
                prev = top_accounts.get("previous_period", active)
                if prev > 0:
                    decline = (active - prev) / prev
                    if decline < -0.2:
                        evidences.append(f"Top influencer accounts down {decline:.1%}")
        
        # Influencer engagement rate
        if "top_influencer_engagement" in x_metrics:
            engagement = x_metrics["top_influencer_engagement"]
            if isinstance(engagement, dict):
                curr = engagement.get("current", 0)
                prev = engagement.get("previous_period", curr)
                if prev > 0:
                    decline = (curr - prev) / prev
                    if decline < -0.25:
                        evidences.append(f"Influencer engagement rate down {decline:.1%}")
        
        if not evidences:
            return None
        
        confidence = 0.7
        
        return DeclineCause(
            cause_type=self.CAUSE_TYPES["INFLUENCER_DROPOFF"],
            confidence=confidence,
            severity_contribution=confidence * 0.9,
            evidence=evidences,
            affected_platforms=["X"],
            business_explanation="Key influencers and high-profile accounts have stopped participating in the trend. This creates a cascading effect reducing overall visibility.",
        )

    def _detect_posting_collapse(
        self, x_metrics: Dict
    ) -> Optional[DeclineCause]:
        """Detect if overall posting volume has collapsed."""
        evidences = []
        
        # X volume collapse
        if x_metrics and "tweet_volume" in x_metrics:
            curr = x_metrics["tweet_volume"].get("current", 0)
            prev = x_metrics["tweet_volume"].get("previous_period", curr)
            if prev > 0 and curr / prev < 0.5:  # Less than 50% of previous
                decline = (curr - prev) / prev
                evidences.append(f"Tweet volume down {decline:.1%}")
        
        if not evidences:
            return None
        
        confidence = 0.9
        
        return DeclineCause(
            cause_type=self.CAUSE_TYPES["POSTING_FREQUENCY_COLLAPSE"],
            confidence=confidence,
            severity_contribution=confidence * 0.95,
            evidence=evidences,
            affected_platforms=["X"],
            business_explanation="Total posts/content volume has collapsed. The trend is rapidly losing critical mass.",
        )

    def _detect_algorithmic_visibility(self, x_metrics: Dict) -> Optional[DeclineCause]:
        """Detect if algorithmic visibility has been reduced."""
        evidences = []
        
        if not x_metrics:
            return None
        
        # Reach decline (disproportionate to engagement)
        if "reach_per_tweet" in x_metrics:
            reach = x_metrics["reach_per_tweet"]
            if isinstance(reach, dict):
                curr = reach.get("current", 1)
                prev = reach.get("previous_period", curr)
                if prev > 0:
                    decline = (curr - prev) / prev
                    if decline < -0.3:
                        evidences.append(f"Reach per tweet down {decline:.1%} (algorithmic suppression)")
        
        # Impression velocity
        if "impression_velocity" in x_metrics:
            velocity = x_metrics["impression_velocity"]
            if velocity < -0.15:
                evidences.append(f"Impressions declining at {velocity:.1%} per day (reduced distribution)")
        
        if not evidences:
            return None
        
        confidence = 0.65
        
        return DeclineCause(
            cause_type=self.CAUSE_TYPES["ALGORITHMIC_VISIBILITY"],
            confidence=confidence,
            severity_contribution=confidence * 0.8,
            evidence=evidences,
            affected_platforms=["X"],
            business_explanation="The platform's algorithm is de-prioritizing the trend in feeds and recommendations. Posts reach fewer people despite being posted.",
        )

    def _detect_audience_fatigue(
        self, x_metrics: Dict
    ) -> Optional[DeclineCause]:
        """Detect if audiences are tired of the trend."""
        evidences = []
        
        # X sentiment decline
        if x_metrics and "sentiment_score" in x_metrics:
            sentiment = x_metrics["sentiment_score"]
            if isinstance(sentiment, dict):
                score = sentiment.get("current", 0)
                if score < -0.1:  # Negative sentiment
                    evidences.append(f"Sentiment score negative ({score:.2f}), indicating audience backlash")
        
        if not evidences:
            return None
        
        confidence = 0.68
        
        return DeclineCause(
            cause_type=self.CAUSE_TYPES["AUDIENCE_FATIGUE"],
            confidence=confidence,
            severity_contribution=confidence * 0.7,
            evidence=evidences,
            affected_platforms=["X"],
            business_explanation="The audience is tired of seeing this trend. Sentiment indicates waning interest or negative perception from followers.",
        )

    def _detect_competing_trend(self, google_trends_metrics: Dict) -> Optional[DeclineCause]:
        """Detect if a competing trend is siphoning interest."""
        evidences = []
        
        if not google_trends_metrics:
            return None
        
        # Competing trends in same category
        if "competing_trends" in google_trends_metrics:
            competitors = google_trends_metrics["competing_trends"]
            if isinstance(competitors, list):
                rising = [t for t in competitors if t.get("trend_direction") == "rising"]
                if len(rising) > 0:
                    trending_names = ", ".join([t.get("name", "Unknown") for t in rising[:3]])
                    evidences.append(f"Related trends rising: {trending_names}")
        
        # Interest shift in category
        if "category_interest_shift" in google_trends_metrics:
            shift = google_trends_metrics["category_interest_shift"]
            if isinstance(shift, dict):
                this_trend = shift.get("this_trend", 0)
                category = shift.get("category_total", 1)
                if category > 0:
                    share = this_trend / category
                    if share < 0.3:
                        evidences.append(f"Trend's share of category interest dropped to {share:.0%}")
        
        if not evidences:
            return None
        
        confidence = 0.6
        
        return DeclineCause(
            cause_type=self.CAUSE_TYPES["COMPETING_TREND"],
            confidence=confidence,
            severity_contribution=confidence * 0.65,
            evidence=evidences,
            affected_platforms=["Google Trends"],
            business_explanation="Related or alternative trends are gaining interest, competing for audience attention and content creation effort.",
        )

    def _detect_temporal_loss(
        self, x_metrics: Dict
    ) -> Optional[DeclineCause]:
        """Detect if the trend has lost temporal relevance (e.g., event-based)."""
        evidences = []
        
        # Event-based relevance loss
        if x_metrics and "days_since_peak" in x_metrics:
            days = x_metrics["days_since_peak"]
            if days > 30:
                evidences.append(f"Trend peaked {days} days ago, natural lifecycle decline")
        
        if not evidences:
            return None
        
        confidence = 0.55
        
        return DeclineCause(
            cause_type=self.CAUSE_TYPES["TEMPORAL_RELEVANCE"],
            confidence=confidence,
            severity_contribution=confidence * 0.6,
            evidence=evidences,
            affected_platforms=["X"],
            business_explanation="The trend is temporally bound (event-specific). Relevance naturally decays as the context fades.",
        )

    def _calculate_trend_status(
        self,
        causes: List[DeclineCause],
        x_metrics: Dict,
    ) -> tuple:
        """Calculate overall trend status and decline probability."""
        
        # Aggregate confidence of all causes
        total_cause_confidence = sum(c.confidence for c in causes) if causes else 0.0
        
        # Check direct metrics for growth signals
        growth_signals = 0
        if x_metrics and x_metrics.get("weekly_engagement_velocity", 0) > 0.05:
            growth_signals += 1
        
        # Determine decline probability
        if total_cause_confidence > 2.0:
            decline_prob = 0.95
            status = TrendStatus.COLLAPSED
        elif total_cause_confidence > 1.5:
            decline_prob = 0.80
            status = TrendStatus.DECLINING
        elif total_cause_confidence > 0.8:
            decline_prob = 0.60
            status = TrendStatus.DECLINING
        elif total_cause_confidence > 0.3:
            decline_prob = 0.40
            status = TrendStatus.STABLE
        else:
            decline_prob = 0.15
            status = TrendStatus.GROWING if growth_signals >= 1 else TrendStatus.STABLE
        
        return status, decline_prob

    def _determine_severity(
        self, decline_probability: float, causes: List[DeclineCause]
    ) -> SeverityLevel:
        """Determine severity level based on decline probability and causes."""
        
        if decline_probability >= 0.85:
            return SeverityLevel.COLLAPSED
        elif decline_probability >= 0.65:
            if any(c.confidence > 0.8 for c in causes):
                return SeverityLevel.CRITICAL
            return SeverityLevel.WARNING
        elif decline_probability >= 0.40:
            return SeverityLevel.WARNING
        else:
            return SeverityLevel.STABLE

    def _generate_platform_summary(
        self,
        x_metrics: Dict,
    ) -> Dict[str, Any]:
        """Generate X/Twitter platform summary of trend health."""
        
        summary = {}
        
        # X summary
        if x_metrics:
            summary["X"] = {
                "tweet_volume": x_metrics.get("tweet_volume", {}).get("current", 0),
                "engagement_velocity": x_metrics.get("weekly_engagement_velocity", 0),
                "reach_per_post": x_metrics.get("reach_per_tweet", {}).get("current", 0),
                "unique_content_ratio": x_metrics.get("unique_content_ratio", 0),
                "sentiment": x_metrics.get("sentiment_score", {}).get("current", 0),
                "health_status": "Declining" if x_metrics.get("weekly_engagement_velocity", 0) < -0.1 else "Stable",
            }
        
        return summary

    def _generate_actions(
        self, causes: List[DeclineCause], status: TrendStatus, severity: SeverityLevel
    ) -> List[RecommendedAction]:
        """Generate actionable recovery or exit strategies."""
        
        actions = []
        
        # Recovery actions for declining trends
        if status == TrendStatus.DECLINING and severity in [SeverityLevel.WARNING, SeverityLevel.CRITICAL]:
            # Cause-specific recovery strategies
            for cause in causes[:3]:  # Top 3 causes
                if "ENGAGEMENT_DECAY" in cause.cause_type:
                    actions.append(
                        RecommendedAction(
                            action_type="RECOVERY",
                            priority="HIGH",
                            description="Launch engagement campaign: Partner with creators for fresh content angles and encourage community interaction.",
                            expected_impact="Reverse engagement decline by 30-50% within 2-3 weeks",
                            timeframe="Immediate (1-3 weeks)",
                            platforms_targeted=cause.affected_platforms,
                        )
                    )
                
                elif "CONTENT_SATURATION" in cause.cause_type:
                    actions.append(
                        RecommendedAction(
                            action_type="RECOVERY",
                            priority="HIGH",
                            description="Refresh trend format: Introduce new creative angles, meme variations, or storytelling formats.",
                            expected_impact="Reinvigorate audience interest with novelty; 40% increase in unique content",
                            timeframe="Immediate (1-2 weeks)",
                            platforms_targeted=cause.affected_platforms,
                        )
                    )
                
                elif "CREATOR_DISENGAGEMENT" in cause.cause_type:
                    actions.append(
                        RecommendedAction(
                            action_type="RECOVERY",
                            priority="HIGH",
                            description="Creator incentive program: Offer rewards, featured placements, or partnerships to re-engage content creators.",
                            expected_impact="Increase posting frequency by 40-60%; restore creative momentum",
                            timeframe="Immediate (2-4 weeks)",
                            platforms_targeted=cause.affected_platforms,
                        )
                    )
                
                elif "INFLUENCER_DROPOFF" in cause.cause_type:
                    actions.append(
                        RecommendedAction(
                            action_type="RECOVERY",
                            priority="CRITICAL",
                            description="Influencer revival: Reach out to top accounts with new angles, exclusive access, or collaboration opportunities.",
                            expected_impact="Restore influencer participation; amplify reach 3-5x via their followers",
                            timeframe="Immediate (1-2 weeks)",
                            platforms_targeted=["X", "TikTok"],
                        )
                    )
                
                elif "AUDIENCE_FATIGUE" in cause.cause_type:
                    actions.append(
                        RecommendedAction(
                            action_type="RECOVERY",
                            priority="MEDIUM",
                            description="Pivot to related trends or derivative concepts to retain audience interest.",
                            expected_impact="Redirect fatigue into new trend momentum; 50% audience retention",
                            timeframe="Immediate (1-2 weeks)",
                            platforms_targeted=cause.affected_platforms,
                        )
                    )
                
                elif "COMPETING_TREND" in cause.cause_type:
                    actions.append(
                        RecommendedAction(
                            action_type="RECOVERY",
                            priority="MEDIUM",
                            description="Merge or bridge trends: Create content that bridges this trend with emerging competitor trends.",
                            expected_impact="Capture interest from both audiences; slow decline to plateau",
                            timeframe="Short-term (1-3 weeks)",
                            platforms_targeted=cause.affected_platforms,
                        )
                    )
        
        # Exit strategies for collapsed trends
        if severity == SeverityLevel.COLLAPSED:
            actions.append(
                RecommendedAction(
                    action_type="EXIT",
                    priority="HIGH",
                    description="Divert resources to emerging trends or evergreen content strategies.",
                    expected_impact="Minimize sunk costs; redirect audience to higher-momentum content",
                    timeframe="Immediate (1 week)",
                    platforms_targeted=["X", "Reddit", "TikTok"],
                )
            )
        
        # Monitoring action (always recommended)
        actions.append(
            RecommendedAction(
                action_type="RECOVERY" if status in [TrendStatus.DECLINING] else "MONITOR",
                priority="MEDIUM",
                description="Set up daily monitoring dashboards for key metrics: engagement velocity, posting volume, and reach.",
                expected_impact="Early detection of further decline or potential recovery",
                timeframe="Ongoing",
                platforms_targeted=["X", "Reddit", "TikTok", "Google Trends"],
            )
        )
        
        return actions

    def _calculate_analysis_confidence(
        self, causes: List[DeclineCause], x_metrics: Dict
    ) -> float:
        """Calculate confidence in the overall analysis."""
        
        # Base confidence on number and quality of detected causes
        cause_confidence = min(1.0, len(causes) / 3.0 * 0.5)
        
        # Boost confidence if X metrics have data
        x_data_count = len([v for v in x_metrics.values() if v is not None]) if x_metrics else 0
        platform_confidence = min(1.0, x_data_count / 10.0) * 0.3
        
        # Cause quality (average confidence of detected causes)
        cause_quality = (sum(c.confidence for c in causes) / len(causes)) if causes else 0.0
        cause_quality = cause_quality * 0.2
        
        return cause_confidence + platform_confidence + cause_quality

    def _serialize_result(self, result: TrendAnalysisResult) -> Dict[str, Any]:
        """Convert TrendAnalysisResult to JSON-serializable dictionary."""
        
        return {
            "trend_name": result.trend_name,
            "analysis_timestamp": result.analysis_timestamp,
            "trend_status": result.trend_status,
            "decline_probability": result.decline_probability,
            "severity_level": result.severity_level,
            "root_causes": [
                {
                    "cause_type": cause.cause_type,
                    "confidence": round(cause.confidence, 3),
                    "severity_contribution": round(cause.severity_contribution, 3),
                    "evidence": cause.evidence,
                    "affected_platforms": cause.affected_platforms,
                    "business_explanation": cause.business_explanation,
                }
                for cause in result.root_causes
            ],
            "cross_platform_summary": result.cross_platform_summary,
            "recommended_actions": [
                {
                    "action_type": action.action_type,
                    "priority": action.priority,
                    "description": action.description,
                    "expected_impact": action.expected_impact,
                    "timeframe": action.timeframe,
                    "platforms_targeted": action.platforms_targeted,
                }
                for action in result.recommended_actions
            ],
            "confidence_in_analysis": result.confidence_in_analysis,
        }
