"""Test script to show declining trend output"""
import sys
import pandas as pd
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, 'src')

from models import TrendData, TrendMetrics, TrendClassification, DeclineAnalysis, AlternativeTrend, PivotStrategy
from formatter import ResponseFormatter

# Create synthetic declining trend data
dates = pd.date_range(end=datetime.now(), periods=90, freq='D')
values = [70 - int(j * 0.33) for j in range(90)]  # Declining pattern

interest_df = pd.DataFrame({
    'declining trend': values
}, index=dates)

trend_data = TrendData(
    keyword="declining trend example",
    domain="test domain",
    interest_over_time=interest_df,
    current_interest=40,
    peak_interest=70,
    related_queries=["related query 1", "related query 2", "related query 3"]
)

# Create classification
classification = TrendClassification(
    category="declining",
    confidence=0.82,
    growth_rate=-8.5,
    reasoning="Trend shows negative momentum with -8.5% monthly decline. Current interest at 40, down from peak of 70. Declining trajectory suggests waning market interest."
)

# Create decline analysis
decline_analysis = DeclineAnalysis(
    days_until_collapse=180,
    projected_marketing_burn=6500.00,
    recommendation="TRY REVIVAL",
    revival_conditions=["Significant external event drives renewed interest", "New product innovation"],
    alternative_trends=[
        AlternativeTrend(
            keyword="emerging alternative 1",
            growth_rate=15.0,
            relevance_to_domain="Growing interest in related space",
            entry_difficulty="medium"
        ),
        AlternativeTrend(
            keyword="innovative alternative 2",
            growth_rate=12.0,
            relevance_to_domain="New developments in the field",
            entry_difficulty="low"
        )
    ],
    pivot_strategy=PivotStrategy(
        approach="Gradually shift from declining trend to emerging alternatives",
        timeline="2-3 months",
        key_actions=["Research alternative trends", "Test content with new keywords", "Reallocate 20% of budget"]
    )
)

# Format and print
formatter = ResponseFormatter(output_format="table")
output = formatter.format_response(classification, decline_analysis, trend_data)
print(output)
