"""Explainability component for generating executive summaries."""

import logging
from typing import List, Dict, Any

from .types import SimulationResponse, ScenarioInput

logger = logging.getLogger(__name__)


class ExecutiveSummaryGenerator:
    """Generates executive summaries explaining simulation results."""

    @staticmethod
    def generate_executive_summary(
        result: SimulationResponse,
        scenario: ScenarioInput,
    ) -> Dict[str, Any]:
        """
        Generate comprehensive executive summary.
        
        Args:
            result: Simulation response
            scenario: Original scenario input
            
        Returns:
            Dictionary containing executive summary
        """
        summary = {
            "trend_analysis": ExecutiveSummaryGenerator._generate_trend_analysis(result, scenario),
            "success_probability": ExecutiveSummaryGenerator._generate_success_probability(result),
            "financial_outlook": ExecutiveSummaryGenerator._generate_financial_outlook(result),
            "risk_assessment": ExecutiveSummaryGenerator._generate_risk_assessment(result, scenario),
            "strategic_recommendation": ExecutiveSummaryGenerator._generate_strategic_recommendation(result, scenario),
            "key_drivers": ExecutiveSummaryGenerator._generate_key_drivers(result, scenario),
            "critical_assumptions": ExecutiveSummaryGenerator._generate_critical_assumptions(result, scenario),
            "action_items": ExecutiveSummaryGenerator._generate_action_items(result, scenario),
        }
        return summary

    @staticmethod
    def _generate_trend_analysis(result: SimulationResponse, scenario: ScenarioInput) -> Dict[str, Any]:
        """Generate trend analysis section."""
        lifecycle_stage = scenario.trend_context.lifecycle_stage
        current_risk = result.risk_projection.current_risk_score
        risk_trend = result.risk_projection.risk_trend
        
        stage_descriptions = {
            "emerging": "early-stage trend with growth potential but limited historical data",
            "growth": "rapidly expanding trend with strong momentum and creator participation",
            "peak": "at maximum adoption with high saturation and potential volatility",
            "decline": "losing momentum with decreasing engagement and creator interest",
            "dormant": "inactive trend with minimal engagement and high risk of failure",
        }
        
        risk_descriptions = {
            "improving": "risk is decreasing, indicating stabilization",
            "stable": "risk is stable, indicating predictable conditions",
            "worsening": "risk is increasing, indicating deteriorating conditions",
        }
        
        return {
            "stage": lifecycle_stage,
            "stage_description": stage_descriptions.get(lifecycle_stage, "unknown"),
            "current_risk_score": current_risk,
            "risk_level": ExecutiveSummaryGenerator._classify_risk_level(current_risk),
            "risk_trend": risk_trend,
            "risk_trend_description": risk_descriptions.get(risk_trend, "unknown"),
            "interpretation": ExecutiveSummaryGenerator._interpret_trend_stage(lifecycle_stage, current_risk, risk_trend),
        }

    @staticmethod
    def _generate_success_probability(result: SimulationResponse) -> Dict[str, Any]:
        """Generate success probability section."""
        break_even_prob = result.expected_roi_metrics.break_even_probability
        loss_prob = result.expected_roi_metrics.loss_probability
        roi_min = result.expected_roi_metrics.roi_percent.min
        roi_max = result.expected_roi_metrics.roi_percent.max
        
        success_level = ExecutiveSummaryGenerator._classify_success_probability(break_even_prob)
        
        return {
            "break_even_probability": break_even_prob,
            "loss_probability": loss_prob,
            "success_level": success_level,
            "roi_range": {
                "min": roi_min,
                "max": roi_max,
                "midpoint": (roi_min + roi_max) / 2,
            },
            "interpretation": ExecutiveSummaryGenerator._interpret_success_probability(break_even_prob, roi_min, roi_max),
        }

    @staticmethod
    def _generate_financial_outlook(result: SimulationResponse) -> Dict[str, Any]:
        """Generate financial outlook section."""
        roi_range = result.expected_roi_metrics.roi_percent
        break_even_prob = result.expected_roi_metrics.break_even_probability
        
        outlook = "positive" if break_even_prob >= 70 else "moderate" if break_even_prob >= 40 else "negative"
        
        return {
            "outlook": outlook,
            "roi_range_min": roi_range.min,
            "roi_range_max": roi_range.max,
            "best_case_roi": roi_range.max,
            "worst_case_roi": roi_range.min,
            "expected_roi": (roi_range.min + roi_range.max) / 2,
            "break_even_probability": break_even_prob,
            "interpretation": ExecutiveSummaryGenerator._interpret_financial_outlook(roi_range, break_even_prob),
        }

    @staticmethod
    def _generate_risk_assessment(result: SimulationResponse, scenario: ScenarioInput) -> Dict[str, Any]:
        """Generate risk assessment section."""
        current_risk = result.risk_projection.current_risk_score
        projected_risk_min = result.risk_projection.projected_risk_score.min
        projected_risk_max = result.risk_projection.projected_risk_score.max
        risk_trend = result.risk_projection.risk_trend
        
        risk_change = (projected_risk_max - current_risk)
        
        return {
            "current_risk_score": current_risk,
            "current_risk_level": ExecutiveSummaryGenerator._classify_risk_level(current_risk),
            "projected_risk_range": {
                "min": projected_risk_min,
                "max": projected_risk_max,
                "midpoint": (projected_risk_min + projected_risk_max) / 2,
            },
            "risk_change": risk_change,
            "risk_trend": risk_trend,
            "risk_tolerance": scenario.constraints.risk_tolerance,
            "tolerance_alignment": ExecutiveSummaryGenerator._assess_tolerance_alignment(
                scenario.constraints.risk_tolerance,
                projected_risk_max,
            ),
            "interpretation": ExecutiveSummaryGenerator._interpret_risk_assessment(
                current_risk, projected_risk_max, risk_trend, scenario.constraints.risk_tolerance
            ),
        }

    @staticmethod
    def _generate_strategic_recommendation(result: SimulationResponse, scenario: ScenarioInput) -> Dict[str, Any]:
        """Generate strategic recommendation section."""
        posture = result.decision_interpretation.recommended_posture
        outlook = result.simulation_summary.overall_outlook
        
        posture_descriptions = {
            "scale": "Aggressively scale investment - conditions are favorable",
            "monitor": "Monitor closely and maintain current investment level",
            "test_small": "Test with limited budget before scaling",
            "avoid": "Avoid this scenario - risk is too high",
        }
        
        outlook_descriptions = {
            "favorable": "Strong conditions support investment",
            "risky": "Moderate conditions with uncertainty",
            "unfavorable": "Weak conditions suggest caution",
        }
        
        return {
            "recommended_posture": posture,
            "posture_description": posture_descriptions.get(posture, "unknown"),
            "overall_outlook": outlook,
            "outlook_description": outlook_descriptions.get(outlook, "unknown"),
            "confidence": result.simulation_summary.confidence,
            "rationale": ExecutiveSummaryGenerator._generate_posture_rationale(result, scenario),
        }

    @staticmethod
    def _generate_key_drivers(result: SimulationResponse, scenario: ScenarioInput) -> Dict[str, Any]:
        """Generate key drivers section."""
        opportunities = result.decision_interpretation.primary_opportunities
        risks = result.decision_interpretation.primary_risks
        sensitive_factor = result.assumption_sensitivity.most_sensitive_factor
        impact_if_wrong = result.assumption_sensitivity.impact_if_wrong
        
        return {
            "primary_opportunities": opportunities,
            "primary_risks": risks,
            "most_sensitive_assumption": sensitive_factor,
            "sensitivity_impact": impact_if_wrong,
            "engagement_growth_range": {
                "min": result.expected_growth_metrics.engagement_growth_percent.min,
                "max": result.expected_growth_metrics.engagement_growth_percent.max,
            },
            "reach_growth_range": {
                "min": result.expected_growth_metrics.reach_growth_percent.min,
                "max": result.expected_growth_metrics.reach_growth_percent.max,
            },
            "interpretation": ExecutiveSummaryGenerator._interpret_key_drivers(result),
        }

    @staticmethod
    def _generate_critical_assumptions(result: SimulationResponse, scenario: ScenarioInput) -> Dict[str, Any]:
        """Generate critical assumptions section."""
        return {
            "engagement_trend": scenario.assumptions.engagement_trend,
            "creator_participation": scenario.assumptions.creator_participation,
            "market_noise": scenario.assumptions.market_noise,
            "most_sensitive_factor": result.assumption_sensitivity.most_sensitive_factor,
            "impact_if_wrong": result.assumption_sensitivity.impact_if_wrong,
            "data_coverage": result.guardrails.data_coverage,
            "data_quality_note": ExecutiveSummaryGenerator._assess_data_quality(result.guardrails.data_coverage),
            "interpretation": ExecutiveSummaryGenerator._interpret_assumptions(result, scenario),
        }

    @staticmethod
    def _generate_action_items(result: SimulationResponse, scenario: ScenarioInput) -> List[Dict[str, str]]:
        """Generate action items section."""
        actions = []
        
        posture = result.decision_interpretation.recommended_posture
        if posture == "scale":
            actions.append({
                "priority": "high",
                "action": "Increase budget allocation and expand creator network",
                "rationale": "Favorable conditions support aggressive scaling",
            })
            actions.append({
                "priority": "high",
                "action": "Accelerate campaign timeline to capitalize on momentum",
                "rationale": "Trend is in growth phase with strong engagement potential",
            })
        elif posture == "monitor":
            actions.append({
                "priority": "medium",
                "action": "Maintain current investment level and monitor metrics weekly",
                "rationale": "Conditions are stable but uncertain",
            })
            actions.append({
                "priority": "medium",
                "action": "Prepare contingency plans for risk escalation",
                "rationale": "Risk trend may change",
            })
        elif posture == "test_small":
            actions.append({
                "priority": "high",
                "action": "Start with limited budget pilot program",
                "rationale": "Low confidence requires validation before scaling",
            })
            actions.append({
                "priority": "high",
                "action": "Establish clear success metrics and decision gates",
                "rationale": "Need to validate assumptions before committing resources",
            })
        elif posture == "avoid":
            actions.append({
                "priority": "high",
                "action": "Avoid this scenario or significantly reduce scope",
                "rationale": "Risk is too high relative to potential returns",
            })
            actions.append({
                "priority": "medium",
                "action": "Explore alternative trends or strategies",
                "rationale": "Better opportunities likely exist",
            })
        
        # Add assumption validation action
        sensitive_factor = result.assumption_sensitivity.most_sensitive_factor
        if result.assumption_sensitivity.impact_if_wrong == "high":
            actions.append({
                "priority": "high",
                "action": f"Validate {sensitive_factor} assumption with market research",
                "rationale": f"This assumption has high impact on outcomes",
            })
        
        # Add data quality action
        if result.guardrails.data_coverage < 75:
            actions.append({
                "priority": "medium",
                "action": "Collect additional data to improve confidence",
                "rationale": f"Current data coverage is {result.guardrails.data_coverage:.0f}%",
            })
        
        return actions

    # Helper methods for interpretation
    @staticmethod
    def _classify_risk_level(risk_score: float) -> str:
        """Classify risk level from score."""
        if risk_score < 25:
            return "low"
        elif risk_score < 50:
            return "moderate"
        elif risk_score < 75:
            return "high"
        else:
            return "critical"

    @staticmethod
    def _classify_success_probability(break_even_prob: float) -> str:
        """Classify success probability."""
        if break_even_prob >= 80:
            return "very_high"
        elif break_even_prob >= 60:
            return "high"
        elif break_even_prob >= 40:
            return "moderate"
        elif break_even_prob >= 20:
            return "low"
        else:
            return "very_low"

    @staticmethod
    def _interpret_trend_stage(lifecycle_stage: str, risk_score: float, risk_trend: str) -> str:
        """Generate interpretation of trend stage."""
        if lifecycle_stage == "emerging":
            return f"This is an early-stage trend with {ExecutiveSummaryGenerator._classify_risk_level(risk_score)} risk. Early adoption could provide competitive advantage but requires careful monitoring."
        elif lifecycle_stage == "growth":
            return f"This trend is in growth phase with {ExecutiveSummaryGenerator._classify_risk_level(risk_score)} risk and {risk_trend} trajectory. Strong momentum presents significant opportunity."
        elif lifecycle_stage == "peak":
            return f"This trend is at peak adoption with {ExecutiveSummaryGenerator._classify_risk_level(risk_score)} risk. Market saturation is high, limiting growth potential."
        elif lifecycle_stage == "decline":
            return f"This trend is declining with {ExecutiveSummaryGenerator._classify_risk_level(risk_score)} risk. Engagement is decreasing, making investment risky."
        elif lifecycle_stage == "dormant":
            return f"This trend is dormant with {ExecutiveSummaryGenerator._classify_risk_level(risk_score)} risk. Minimal engagement makes investment unlikely to succeed."
        return "Unknown trend stage"

    @staticmethod
    def _interpret_success_probability(break_even_prob: float, roi_min: float, roi_max: float) -> str:
        """Generate interpretation of success probability."""
        success_level = ExecutiveSummaryGenerator._classify_success_probability(break_even_prob)
        
        if success_level == "very_high":
            return f"Excellent financial outlook with {break_even_prob:.0f}% probability of breaking even. Expected ROI range of {roi_min:.0f}% to {roi_max:.0f}% is very attractive."
        elif success_level == "high":
            return f"Strong financial outlook with {break_even_prob:.0f}% probability of breaking even. Expected ROI range of {roi_min:.0f}% to {roi_max:.0f}% is favorable."
        elif success_level == "moderate":
            return f"Moderate financial outlook with {break_even_prob:.0f}% probability of breaking even. Expected ROI range of {roi_min:.0f}% to {roi_max:.0f}% requires careful consideration."
        elif success_level == "low":
            return f"Weak financial outlook with {break_even_prob:.0f}% probability of breaking even. Expected ROI range of {roi_min:.0f}% to {roi_max:.0f}% is concerning."
        else:
            return f"Very weak financial outlook with {break_even_prob:.0f}% probability of breaking even. Expected ROI range of {roi_min:.0f}% to {roi_max:.0f}% suggests avoiding this scenario."

    @staticmethod
    def _interpret_financial_outlook(roi_range, break_even_prob: float) -> str:
        """Generate interpretation of financial outlook."""
        if break_even_prob >= 70:
            return f"Strong financial case with best-case ROI of {roi_range.max:.0f}% and worst-case of {roi_range.min:.0f}%. High probability of positive returns justifies investment."
        elif break_even_prob >= 40:
            return f"Moderate financial case with best-case ROI of {roi_range.max:.0f}% and worst-case of {roi_range.min:.0f}%. Requires risk mitigation strategies."
        else:
            return f"Weak financial case with best-case ROI of {roi_range.max:.0f}% and worst-case of {roi_range.min:.0f}%. High risk of losses suggests reconsidering investment."

    @staticmethod
    def _interpret_risk_assessment(current_risk: float, projected_risk_max: float, risk_trend: str, risk_tolerance: str) -> str:
        """Generate interpretation of risk assessment."""
        risk_change = projected_risk_max - current_risk
        
        if risk_trend == "improving":
            return f"Risk is improving from {current_risk:.0f} to {projected_risk_max:.0f}. Campaign execution is expected to stabilize the trend."
        elif risk_trend == "stable":
            return f"Risk remains stable at approximately {projected_risk_max:.0f}. Conditions are predictable and manageable."
        else:  # worsening
            return f"Risk is worsening from {current_risk:.0f} to {projected_risk_max:.0f}. Campaign execution may increase volatility. {risk_tolerance} risk tolerance may be insufficient."

    @staticmethod
    def _assess_tolerance_alignment(risk_tolerance: str, projected_risk_max: float) -> str:
        """Assess alignment between risk tolerance and projected risk."""
        if risk_tolerance == "low" and projected_risk_max > 60:
            return "misaligned - projected risk exceeds tolerance"
        elif risk_tolerance == "medium" and projected_risk_max > 75:
            return "misaligned - projected risk exceeds tolerance"
        elif risk_tolerance == "high":
            return "aligned - high tolerance accommodates projected risk"
        else:
            return "aligned - projected risk within tolerance"

    @staticmethod
    def _generate_posture_rationale(result: SimulationResponse, scenario: ScenarioInput) -> str:
        """Generate rationale for recommended posture."""
        posture = result.decision_interpretation.recommended_posture
        break_even_prob = result.expected_roi_metrics.break_even_probability
        risk_trend = result.risk_projection.risk_trend
        lifecycle_stage = scenario.trend_context.lifecycle_stage
        
        if posture == "scale":
            return f"Break-even probability of {break_even_prob:.0f}% with {risk_trend} risk trend supports aggressive scaling. {lifecycle_stage} stage trend has strong growth potential."
        elif posture == "monitor":
            return f"Break-even probability of {break_even_prob:.0f}% with {risk_trend} risk trend suggests maintaining current investment. Monitor for changes in conditions."
        elif posture == "test_small":
            return f"Break-even probability of {break_even_prob:.0f}% with {risk_trend} risk trend requires validation. Start with limited budget to test assumptions."
        else:  # avoid
            return f"Break-even probability of {break_even_prob:.0f}% with {risk_trend} risk trend and {lifecycle_stage} stage trend makes this scenario too risky."

    @staticmethod
    def _interpret_key_drivers(result: SimulationResponse) -> str:
        """Generate interpretation of key drivers."""
        opportunities = result.decision_interpretation.primary_opportunities
        risks = result.decision_interpretation.primary_risks
        
        opp_str = ", ".join(opportunities[:2])
        risk_str = ", ".join(risks[:2])
        
        return f"Key opportunities include {opp_str}. Main risks are {risk_str}. Success depends on capitalizing on opportunities while mitigating risks."

    @staticmethod
    def _assess_data_quality(data_coverage: float) -> str:
        """Assess data quality based on coverage."""
        if data_coverage >= 90:
            return "Excellent - high confidence in data"
        elif data_coverage >= 75:
            return "Good - sufficient data for analysis"
        elif data_coverage >= 50:
            return "Fair - limited data, ranges widened"
        else:
            return "Poor - significant data gaps, use with caution"

    @staticmethod
    def _interpret_assumptions(result: SimulationResponse, scenario: ScenarioInput) -> str:
        """Generate interpretation of critical assumptions."""
        sensitive_factor = result.assumption_sensitivity.most_sensitive_factor
        impact = result.assumption_sensitivity.impact_if_wrong
        data_coverage = result.guardrails.data_coverage
        
        return f"Assumptions are based on {data_coverage:.0f}% data coverage. The {sensitive_factor} assumption has {impact} impact on outcomes. Validate this assumption before committing resources."


def format_executive_summary(summary: Dict[str, Any]) -> str:
    """Format executive summary for display."""
    lines = []
    
    lines.append("\n" + "="*80)
    lines.append("EXECUTIVE SUMMARY - TREND ADOPTION ANALYSIS")
    lines.append("="*80)
    
    # Trend Analysis
    lines.append("\n[TREND ANALYSIS]")
    lines.append("-" * 80)
    ta = summary["trend_analysis"]
    lines.append(f"Lifecycle Stage: {ta['stage'].upper()}")
    lines.append(f"Stage Description: {ta['stage_description']}")
    lines.append(f"Current Risk Score: {ta['current_risk_score']:.0f}/100 ({ta['risk_level'].upper()})")
    lines.append(f"Risk Trend: {ta['risk_trend'].upper()}")
    lines.append(f"Analysis: {ta['interpretation']}")
    
    # Success Probability
    lines.append("\n[SUCCESS PROBABILITY]")
    lines.append("-" * 80)
    sp = summary["success_probability"]
    lines.append(f"Break-Even Probability: {sp['break_even_probability']:.0f}%")
    lines.append(f"Success Level: {sp['success_level'].upper()}")
    lines.append(f"Expected ROI: {sp['roi_range']['midpoint']:.0f}% (Range: {sp['roi_range']['min']:.0f}% to {sp['roi_range']['max']:.0f}%)")
    lines.append(f"Analysis: {sp['interpretation']}")
    
    # Financial Outlook
    lines.append("\n[FINANCIAL OUTLOOK]")
    lines.append("-" * 80)
    fo = summary["financial_outlook"]
    lines.append(f"Outlook: {fo['outlook'].upper()}")
    lines.append(f"Best Case ROI: {fo['best_case_roi']:.0f}%")
    lines.append(f"Worst Case ROI: {fo['worst_case_roi']:.0f}%")
    lines.append(f"Expected ROI: {fo['expected_roi']:.0f}%")
    lines.append(f"Analysis: {fo['interpretation']}")
    
    # Risk Assessment
    lines.append("\n[RISK ASSESSMENT]")
    lines.append("-" * 80)
    ra = summary["risk_assessment"]
    lines.append(f"Current Risk: {ra['current_risk_score']:.0f}/100 ({ra['current_risk_level'].upper()})")
    lines.append(f"Projected Risk: {ra['projected_risk_range']['min']:.0f} to {ra['projected_risk_range']['max']:.0f}")
    lines.append(f"Risk Trend: {ra['risk_trend'].upper()}")
    lines.append(f"Risk Tolerance: {ra['risk_tolerance'].upper()}")
    lines.append(f"Alignment: {ra['tolerance_alignment'].upper()}")
    lines.append(f"Analysis: {ra['interpretation']}")
    
    # Strategic Recommendation
    lines.append("\n[STRATEGIC RECOMMENDATION]")
    lines.append("-" * 80)
    sr = summary["strategic_recommendation"]
    lines.append(f"Recommended Posture: {sr['recommended_posture'].upper()}")
    lines.append(f"Description: {sr['posture_description']}")
    lines.append(f"Overall Outlook: {sr['overall_outlook'].upper()}")
    lines.append(f"Confidence: {sr['confidence'].upper()}")
    lines.append(f"Rationale: {sr['rationale']}")
    
    # Key Drivers
    lines.append("\n[KEY DRIVERS]")
    lines.append("-" * 80)
    kd = summary["key_drivers"]
    lines.append(f"Engagement Growth: {kd['engagement_growth_range']['min']:.0f}% to {kd['engagement_growth_range']['max']:.0f}%")
    lines.append(f"Reach Growth: {kd['reach_growth_range']['min']:.0f}% to {kd['reach_growth_range']['max']:.0f}%")
    lines.append("Primary Opportunities:")
    for opp in kd["primary_opportunities"][:3]:
        lines.append(f"  + {opp}")
    lines.append("Primary Risks:")
    for risk in kd["primary_risks"][:3]:
        lines.append(f"  - {risk}")
    lines.append(f"Most Sensitive Factor: {kd['most_sensitive_assumption']} ({kd['sensitivity_impact'].upper()} impact)")
    
    # Critical Assumptions
    lines.append("\n[CRITICAL ASSUMPTIONS]")
    lines.append("-" * 80)
    ca = summary["critical_assumptions"]
    lines.append(f"Engagement Trend: {ca['engagement_trend'].upper()}")
    lines.append(f"Creator Participation: {ca['creator_participation'].upper()}")
    lines.append(f"Market Noise: {ca['market_noise'].upper()}")
    lines.append(f"Data Coverage: {ca['data_coverage']:.0f}%")
    lines.append(f"Data Quality: {ca['data_quality_note']}")
    lines.append(f"Analysis: {ca['interpretation']}")
    
    # Action Items
    lines.append("\n[ACTION ITEMS]")
    lines.append("-" * 80)
    for i, action in enumerate(summary["action_items"], 1):
        priority_marker = "[HIGH]" if action["priority"] == "high" else "[MED]"
        lines.append(f"{priority_marker} {action['action']}")
        lines.append(f"   Rationale: {action['rationale']}")
    
    lines.append("\n" + "="*80)
    
    return "\n".join(lines)
