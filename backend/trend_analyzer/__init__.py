"""
Trend Analyzer Module
Twitter/X trend decline analysis with causal explanations
"""

from .trend_analyzer import TrendAnalyzer
from .explanation_engine import TrendAnalysisExplainer
from .schemas import TrendMetricsInput, TrendAnalysisOutput

__all__ = [
    "TrendAnalyzer",
    "TrendAnalysisExplainer",
    "TrendMetricsInput",
    "TrendAnalysisOutput"
]
