"""Baseline extraction component for retrieving and normalizing metrics."""

import logging
from typing import Optional, Dict, Any

from .types import (
    ScenarioInput,
    RangeValue,
    TrendLifecycleEngineResponse,
    EarlyDeclineDetectionResponse,
)
from .external_systems import ExternalSystemsClient
from .utils import normalize_to_range
from .constants import (
    DATA_COVERAGE_THRESHOLD_LOW,
    CONFIDENCE_THRESHOLD_LOW,
)

logger = logging.getLogger(__name__)


class BaselineExtractor:
    """Extracts and normalizes baseline metrics from external systems."""

    def __init__(self, external_systems: ExternalSystemsClient):
        """
        Initialize baseline extractor.
        
        Args:
            external_systems: Client for accessing external systems
        """
        self.external_systems = external_systems

    def extract_baseline(self, scenario: ScenarioInput) -> Dict[str, Any]:
        """
        Extract baseline metrics from external systems.
        
        Args:
            scenario: The scenario to extract baseline for
            
        Returns:
            Dictionary containing baseline metrics and metadata
        """
        baseline = {
            "engagement_trend": None,
            "roi_trend": None,
            "current_risk_score": scenario.trend_context.current_risk_score,
            "historical_volatility": None,
            "risk_trajectory": None,
            "data_coverage": 0,
            "missing_data_points": [],
            "sources": {},
        }

        # Query Trend Lifecycle Engine
        trend_metrics = self.external_systems.get_trend_metrics(
            scenario.trend_context.trend_id
        )
        if trend_metrics:
            baseline["engagement_trend"] = self._normalize_metric(
                trend_metrics.engagement_trend
            )
            baseline["roi_trend"] = self._normalize_metric(trend_metrics.roi_trend)
            baseline["historical_volatility"] = self._normalize_metric(
                trend_metrics.historical_volatility
            )
            baseline["sources"]["engagement_trend"] = "Trend_Lifecycle_Engine"
            baseline["sources"]["roi_trend"] = "Trend_Lifecycle_Engine"
            baseline["sources"]["historical_volatility"] = "Trend_Lifecycle_Engine"
            logger.info(f"Retrieved trend metrics for trend_id={scenario.trend_context.trend_id}")
        else:
            baseline["missing_data_points"].extend([
                "engagement_trend",
                "roi_trend",
                "historical_volatility",
            ])
            logger.warning(f"Failed to retrieve trend metrics for trend_id={scenario.trend_context.trend_id}")

        # Query Early Decline Detection
        risk_metrics = self.external_systems.get_risk_metrics(
            scenario.trend_context.trend_id
        )
        if risk_metrics:
            baseline["current_risk_score"] = self._normalize_metric(
                risk_metrics.current_risk_score
            )
            baseline["risk_trajectory"] = risk_metrics.risk_trajectory
            baseline["sources"]["current_risk_score"] = "Early_Decline_Detection"
            baseline["sources"]["risk_trajectory"] = "Early_Decline_Detection"
            logger.info(f"Retrieved risk metrics for trend_id={scenario.trend_context.trend_id}")
        else:
            baseline["missing_data_points"].append("risk_trajectory")
            logger.warning(f"Failed to retrieve risk metrics for trend_id={scenario.trend_context.trend_id}")

        # Calculate data coverage
        required_data_points = 5  # engagement_trend, roi_trend, historical_volatility, current_risk_score, risk_trajectory
        available_data_points = required_data_points - len(baseline["missing_data_points"])
        baseline["data_coverage"] = (available_data_points / required_data_points) * 100

        logger.info(f"Data coverage: {baseline['data_coverage']:.1f}%")

        return baseline

    @staticmethod
    def _normalize_metric(value: float, min_val: float = 0, max_val: float = 100) -> float:
        """
        Normalize a metric to 0-100 range.
        
        Args:
            value: The value to normalize
            min_val: Minimum bound
            max_val: Maximum bound
            
        Returns:
            Normalized value
        """
        return normalize_to_range(value, min_val, max_val)

    @staticmethod
    def adjust_confidence_for_data_coverage(
        original_confidence: str,
        data_coverage: float,
    ) -> str:
        """
        Adjust confidence level based on data coverage.
        
        Args:
            original_confidence: Original confidence level
            data_coverage: Data coverage percentage
            
        Returns:
            Adjusted confidence level
        """
        if data_coverage < 50:
            logger.warning(f"Low data coverage ({data_coverage:.1f}%) - reducing confidence")
            return "low"
        elif data_coverage < 75:
            if original_confidence == "high":
                return "medium"
        return original_confidence

    @staticmethod
    def should_widen_ranges(data_coverage: float, confidence: str) -> bool:
        """
        Determine if output ranges should be widened.
        
        Args:
            data_coverage: Data coverage percentage
            confidence: Confidence level
            
        Returns:
            True if ranges should be widened
        """
        return data_coverage < DATA_COVERAGE_THRESHOLD_LOW or confidence == "low"

    @staticmethod
    def get_range_widening_factor(data_coverage: float, confidence: str) -> float:
        """
        Calculate range widening factor.
        
        Args:
            data_coverage: Data coverage percentage
            confidence: Confidence level
            
        Returns:
            Widening factor (1.0 = no widening)
        """
        factor = 1.0

        if data_coverage < 50:
            factor *= 1.5
        elif data_coverage < 75:
            factor *= 1.2

        if confidence == "low":
            factor *= 1.3
        elif confidence == "medium":
            factor *= 1.1

        return factor
