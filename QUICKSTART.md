# Quick Start Guide

## Installation

```bash
pip install -r requirements.txt
```

## Running the Demo

```bash
python demo.py
```

This runs three example scenarios:
1. **Aggressive Growth Strategy** on a growing trend
2. **Conservative Strategy** on a declining trend
3. **Balanced Strategy** on a peak trend

## Running Tests

```bash
python tests/test_simulator.py
```

## Basic Usage

```python
from what_if_simulator.types import (
    ScenarioInput,
    TrendContext,
    CampaignStrategy,
    Assumptions,
    Constraints,
)
from what_if_simulator.external_systems import (
    MockTrendLifecycleEngine,
    MockEarlyDeclineDetection,
    MockROIAttribution,
    ExternalSystemsClient,
)
from what_if_simulator.simulator import WhatIfSimulator

# Initialize
external_systems = ExternalSystemsClient(
    trend_lifecycle_engine=MockTrendLifecycleEngine(),
    early_decline_detection=MockEarlyDeclineDetection(),
    roi_attribution=MockROIAttribution(),
)
simulator = WhatIfSimulator(external_systems)

# Create scenario
scenario = ScenarioInput(
    trend_context=TrendContext(
        trend_id="trend_123",
        trend_name="My Trend",
        platform="tiktok",
        lifecycle_stage="growth",
        current_risk_score=45.0,
        confidence="medium",
    ),
    campaign_strategy=CampaignStrategy(
        campaign_type="short_term_influencer",
        budget_range={"min": 5000, "max": 15000},
        campaign_duration_days=30,
        creator_tier="macro",
        content_intensity="high",
    ),
    assumptions=Assumptions(
        engagement_trend="optimistic",
        creator_participation="increasing",
        market_noise="low",
    ),
    constraints=Constraints(
        risk_tolerance="medium",
        max_budget_cap=50000,
    ),
)

# Run simulation
result = simulator.simulate(scenario)

# Access results
print(f"Recommended Posture: {result.decision_interpretation.recommended_posture}")
print(f"Break-Even Probability: {result.expected_roi_metrics.break_even_probability}%")
print(f"Engagement Growth: {result.expected_growth_metrics.engagement_growth_percent.min}% - {result.expected_growth_metrics.engagement_growth_percent.max}%")
```

## Understanding Results

### Recommended Posture
- **scale**: High confidence, favorable conditions - scale up investment
- **monitor**: Moderate confidence, stable conditions - monitor closely
- **test_small**: Low confidence or worsening conditions - test with small budget
- **avoid**: High risk, unfavorable conditions - avoid this scenario

### Overall Outlook
- **favorable**: Strong break-even probability with stable/improving risk
- **risky**: Moderate conditions with some uncertainty
- **unfavorable**: Low break-even probability or worsening risk

### Key Metrics
- **Engagement Growth**: Range of expected user interaction increase
- **Reach Growth**: Range of expected audience expansion
- **ROI Range**: Expected return on investment range
- **Break-Even Probability**: Likelihood of recovering investment
- **Risk Trend**: Direction of risk evolution (improving/stable/worsening)

### Guardrails
- **Data Coverage**: Percentage of required data available (lower = wider ranges)
- **System Note**: Explains limitations, missing data, and special conditions

## Customizing External Systems

Replace mock implementations with real ones:

```python
from my_systems import RealTrendLifecycleEngine, RealEarlyDeclineDetection, RealROIAttribution

external_systems = ExternalSystemsClient(
    trend_lifecycle_engine=RealTrendLifecycleEngine(),
    early_decline_detection=RealEarlyDeclineDetection(),
    roi_attribution=RealROIAttribution(),
)
```

## Key Principles

1. **Range-Based**: All outputs are ranges, never exact predictions
2. **Transparent**: All assumptions are documented explicitly
3. **Deterministic**: Uses only rule-based logic, no ML
4. **Defensible**: Works with partial data, surfaces limitations
5. **Actionable**: Translates ranges into strategic recommendations

## Troubleshooting

### Import Errors
Ensure `src` is in your Python path:
```python
import sys
sys.path.insert(0, 'src')
```

### Validation Errors
Check that all required fields are provided and valid:
- `lifecycle_stage` must be one of: emerging, growth, peak, decline, dormant
- `campaign_type` must be one of: short_term_influencer, long_term_paid, organic_only, mixed
- `creator_tier` must be one of: nano, micro, macro, mixed
- Budget range max must not exceed max_budget_cap

### Missing Data
If external systems are unavailable, the simulator:
- Documents missing data in guardrails
- Widens output ranges to reflect uncertainty
- Uses fallback computations
- Continues simulation with reduced confidence

## Next Steps

1. Review the demo scenarios in `demo.py`
2. Read the full documentation in `README.md`
3. Explore the design document: `.kiro/specs/what-if-trend-simulator/design.md`
4. Check the requirements: `.kiro/specs/what-if-trend-simulator/requirements.md`
