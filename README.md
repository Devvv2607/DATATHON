# What-If Trend Adoption Simulator

A deterministic, rule-based planning sandbox for modeling potential outcomes of trend adoption campaigns.

## Overview

The What-If Trend Adoption Simulator enables business and marketing users to model potential outcomes of trend adoption campaigns before committing resources. Rather than providing exact predictions, the simulator produces defensible range-based outputs that explicitly surface assumptions and uncertainty.

**Core Principles:**
- Range-based outputs (never exact values)
- Explicit assumption surfacing
- Deterministic, rule-based logic (no ML, no sentiment analysis)
- Defensible with partial data
- Reuses existing platform intelligence

## Architecture

The simulator operates as a composition layer with five main components:

```
User Input (Scenario)
    ↓
[Validation Layer] - Validates inputs against predefined rules
    ↓
[Baseline Extraction Layer] - Queries external systems for current metrics
    ↓
[Range Computation Layer] - Computes min-max ranges for all outputs
    ↓
[Sensitivity Analysis Layer] - Identifies most impactful assumptions
    ↓
[Interpretation Layer] - Translates ranges into strategic recommendations
    ↓
Output Response
```

## Project Structure

```
src/what_if_simulator/
├── __init__.py                 # Package initialization
├── types.py                    # Core type definitions
├── constants.py                # Configuration and constants
├── errors.py                   # Custom exceptions
├── logging_config.py           # Logging setup
├── utils.py                    # Utility functions
├── external_systems.py         # External system interfaces
├── validation.py               # Input validation component
├── baseline_extraction.py       # Baseline metric extraction
├── range_computation.py         # Range computation logic
├── roi_computation.py           # ROI and probability computation
├── interpretation.py            # Result interpretation
├── sensitivity_analysis.py      # Assumption sensitivity analysis
├── guardrails.py               # Guardrails and system notes
└── simulator.py                # Main orchestration

tests/
└── test_simulator.py           # Basic integration tests
```

## Usage

### Basic Example

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

# Create external systems client
external_systems = ExternalSystemsClient(
    trend_lifecycle_engine=MockTrendLifecycleEngine(),
    early_decline_detection=MockEarlyDeclineDetection(),
    roi_attribution=MockROIAttribution(),
)

# Create simulator
simulator = WhatIfSimulator(external_systems)

# Create scenario
scenario = ScenarioInput(
    trend_context=TrendContext(
        trend_id="trend_123",
        trend_name="TikTok Dance Challenge",
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

## Input Contract

```python
ScenarioInput {
    trend_context: {
        trend_id: str
        trend_name: str
        platform: str
        lifecycle_stage: "emerging" | "growth" | "peak" | "decline" | "dormant"
        current_risk_score: float (0-100)
        confidence: "low" | "medium" | "high"
    }
    campaign_strategy: {
        campaign_type: "short_term_influencer" | "long_term_paid" | "organic_only" | "mixed"
        budget_range: {"min": float, "max": float}
        campaign_duration_days: int
        creator_tier: "nano" | "micro" | "macro" | "mixed"
        content_intensity: "low" | "medium" | "high"
    }
    assumptions: {
        engagement_trend: "optimistic" | "neutral" | "pessimistic"
        creator_participation: "increasing" | "stable" | "declining"
        market_noise: "low" | "medium" | "high"
    }
    constraints: {
        risk_tolerance: "low" | "medium" | "high"
        max_budget_cap: float
    }
}
```

## Output Contract

```python
SimulationResponse {
    scenario_id: str
    trend_id: str
    trend_name: str
    simulation_summary: {
        scenario_label: str
        overall_outlook: "favorable" | "risky" | "unfavorable"
        confidence: "low" | "medium" | "high"
    }
    expected_growth_metrics: {
        engagement_growth_percent: {min: float, max: float}
        reach_growth_percent: {min: float, max: float}
        creator_participation_change_percent: {min: float, max: float}
    }
    expected_roi_metrics: {
        roi_percent: {min: float, max: float}
        break_even_probability: float (0-100)
        loss_probability: float (0-100)
    }
    risk_projection: {
        current_risk_score: float (0-100)
        projected_risk_score: {min: float, max: float}
        risk_trend: "improving" | "stable" | "worsening"
    }
    decision_interpretation: {
        recommended_posture: "scale" | "test_small" | "monitor" | "avoid"
        primary_opportunities: [str]
        primary_risks: [str]
    }
    assumption_sensitivity: {
        most_sensitive_factor: str
        impact_if_wrong: "low" | "medium" | "high"
    }
    guardrails: {
        data_coverage: float (0-100)
        system_note: str
    }
}
```

## Key Features

### 1. Range-Based Outputs
All numeric outputs are ranges (min-max) rather than point estimates, reflecting uncertainty explicitly.

### 2. Deterministic Logic
Uses only if-then rules, arithmetic operations, and lookup tables. No machine learning or probabilistic inference.

### 3. Assumption Transparency
All assumptions are documented explicitly in the output. Default assumptions are applied for missing inputs.

### 4. Data Coverage Tracking
Monitors data availability from external systems and widens ranges when coverage is low.

### 5. Sensitivity Analysis
Identifies which assumptions have the greatest impact on outcomes, helping prioritize data collection.

### 6. Strategic Recommendations
Translates numeric ranges into actionable postures:
- **Scale**: High confidence, favorable conditions
- **Monitor**: Moderate confidence, stable conditions
- **Test_Small**: Low confidence or worsening conditions
- **Avoid**: High risk, unfavorable conditions

### 7. Guardrails
Surfaces data limitations, special conditions, and extrapolation limits to ensure users understand reliability boundaries.

## External System Integration

The simulator integrates with three external systems:

### Trend Lifecycle Engine
Provides current engagement trend, ROI trend, and historical volatility for the trend.

### Early Decline Detection
Provides current risk score and risk trajectory.

### ROI Attribution
Maps engagement and reach growth to financial outcomes.

All external system queries are handled gracefully with fallback computations when systems are unavailable.

## Testing

Run the basic integration tests:

```bash
python tests/test_simulator.py
```

## Implementation Notes

- All code follows deterministic, rule-based logic
- No machine learning models or sentiment analysis
- External system queries are mocked for testing
- Range widening is applied when data coverage is low
- Probability calculations use linear interpolation
- Risk scores are clamped to 0-100 range
- All assumptions are documented in output guardrails

## Future Enhancements

- Scenario persistence and retrieval
- Multi-scenario comparison
- API endpoint wrapper
- Integration tests with real external systems
- Property-based testing suite
- Advanced sensitivity analysis
