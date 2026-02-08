"""Interfaces for querying external platform systems."""

from abc import ABC, abstractmethod
from typing import Optional
import logging

from .types import (
    TrendLifecycleEngineResponse,
    EarlyDeclineDetectionResponse,
    ROIAttributionResponse,
    RangeValue,
)

logger = logging.getLogger(__name__)


class TrendLifecycleEngine(ABC):
    """Interface for querying Trend Lifecycle Engine."""

    @abstractmethod
    def query(self, trend_id: str) -> Optional[TrendLifecycleEngineResponse]:
        """
        Query the Trend Lifecycle Engine for trend metrics.
        
        Args:
            trend_id: The ID of the trend to query
            
        Returns:
            TrendLifecycleEngineResponse if data is available, None if unavailable
        """
        pass


class EarlyDeclineDetection(ABC):
    """Interface for querying Early Decline Detection system."""

    @abstractmethod
    def query(self, trend_id: str) -> Optional[EarlyDeclineDetectionResponse]:
        """
        Query the Early Decline Detection system for risk metrics.
        
        Args:
            trend_id: The ID of the trend to query
            
        Returns:
            EarlyDeclineDetectionResponse if data is available, None if unavailable
        """
        pass


class ROIAttribution(ABC):
    """Interface for querying ROI Attribution system."""

    @abstractmethod
    def query(
        self,
        engagement_growth_range: RangeValue,
        reach_growth_range: RangeValue,
        campaign_budget: float,
        campaign_duration_days: int,
    ) -> Optional[ROIAttributionResponse]:
        """
        Query the ROI Attribution system for ROI projections.
        
        Args:
            engagement_growth_range: Projected engagement growth range
            reach_growth_range: Projected reach growth range
            campaign_budget: Campaign budget amount
            campaign_duration_days: Campaign duration in days
            
        Returns:
            ROIAttributionResponse if data is available, None if unavailable
        """
        pass


class MockTrendLifecycleEngine(TrendLifecycleEngine):
    """Mock implementation for testing."""

    def query(self, trend_id: str) -> Optional[TrendLifecycleEngineResponse]:
        """Return mock data for testing."""
        logger.debug(f"Mock query to Trend Lifecycle Engine for trend_id={trend_id}")
        return TrendLifecycleEngineResponse(
            lifecycle_stage="growth",
            engagement_trend=65.0,
            roi_trend=55.0,
            historical_volatility=35.0,
        )


class MockEarlyDeclineDetection(EarlyDeclineDetection):
    """Mock implementation for testing."""

    def query(self, trend_id: str) -> Optional[EarlyDeclineDetectionResponse]:
        """Return mock data for testing."""
        logger.debug(f"Mock query to Early Decline Detection for trend_id={trend_id}")
        return EarlyDeclineDetectionResponse(
            current_risk_score=40.0,
            risk_indicators=["moderate_volatility", "stable_engagement"],
            risk_trajectory="stable",
        )


class MockROIAttribution(ROIAttribution):
    """Mock implementation for testing."""

    def query(
        self,
        engagement_growth_range: RangeValue,
        reach_growth_range: RangeValue,
        campaign_budget: float,
        campaign_duration_days: int,
    ) -> Optional[ROIAttributionResponse]:
        """Return mock data for testing."""
        logger.debug(
            f"Mock query to ROI Attribution: engagement={engagement_growth_range}, "
            f"reach={reach_growth_range}, budget={campaign_budget}, duration={campaign_duration_days}"
        )
        # Simple mock: average the engagement and reach growth, scale by budget efficiency
        avg_growth = (engagement_growth_range.max + reach_growth_range.max) / 2
        roi_min = avg_growth * 0.5 - 10
        roi_max = avg_growth * 1.2 + 5
        return ROIAttributionResponse(
            roi_percent_range=RangeValue(min=roi_min, max=roi_max),
            confidence=70.0,
        )


class ExternalSystemsClient:
    """Client for accessing external platform systems."""

    def __init__(
        self,
        trend_lifecycle_engine: TrendLifecycleEngine,
        early_decline_detection: EarlyDeclineDetection,
        roi_attribution: ROIAttribution,
    ):
        """
        Initialize the external systems client.
        
        Args:
            trend_lifecycle_engine: Trend Lifecycle Engine implementation
            early_decline_detection: Early Decline Detection implementation
            roi_attribution: ROI Attribution implementation
        """
        self.trend_lifecycle_engine = trend_lifecycle_engine
        self.early_decline_detection = early_decline_detection
        self.roi_attribution = roi_attribution

    def get_trend_metrics(self, trend_id: str) -> Optional[TrendLifecycleEngineResponse]:
        """Get trend metrics from Trend Lifecycle Engine."""
        try:
            return self.trend_lifecycle_engine.query(trend_id)
        except Exception as e:
            logger.error(f"Error querying Trend Lifecycle Engine: {e}")
            return None

    def get_risk_metrics(self, trend_id: str) -> Optional[EarlyDeclineDetectionResponse]:
        """Get risk metrics from Early Decline Detection."""
        try:
            return self.early_decline_detection.query(trend_id)
        except Exception as e:
            logger.error(f"Error querying Early Decline Detection: {e}")
            return None

    def get_roi_projection(
        self,
        engagement_growth_range: RangeValue,
        reach_growth_range: RangeValue,
        campaign_budget: float,
        campaign_duration_days: int,
    ) -> Optional[ROIAttributionResponse]:
        """Get ROI projection from ROI Attribution."""
        try:
            return self.roi_attribution.query(
                engagement_growth_range,
                reach_growth_range,
                campaign_budget,
                campaign_duration_days,
            )
        except Exception as e:
            logger.error(f"Error querying ROI Attribution: {e}")
            return None
