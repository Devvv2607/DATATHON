# Implementation Plan: What-If Trend Adoption Simulator

## Overview

This implementation plan breaks down the What-If Trend Adoption Simulator into discrete, incremental coding tasks. The simulator is built as a composition layer that validates inputs, extracts baselines from external systems, computes range-based outputs using deterministic rules, and interprets results into strategic recommendations.

The implementation follows a layered architecture: validation → baseline extraction → range computation → sensitivity analysis → interpretation → output assembly. Each layer is implemented and tested before moving to the next, ensuring early validation of core functionality.

## Tasks

- [x] 1. Set up project structure, core types, and external system interfaces
  - Create Python package structure with modules for each component
  - Define TypedDict/dataclass types for ScenarioInput, SimulationResponse, and all nested structures
  - Define interfaces for external system queries (Trend Lifecycle Engine, Early Decline Detection, ROI Attribution)
  - Set up logging and error handling infrastructure
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8_

- [x] 2. Implement validation component
  - [x] 2.1 Create lifecycle-campaign compatibility matrix
    - Define predefined compatibility rules for all lifecycle_stage + campaign_type combinations
    - Implement compatibility check function
    - _Requirements: 1.1, 1.2_
  
  - [ ]* 2.2 Write property test for compatibility validation
    - **Property 1: Lifecycle-Campaign Compatibility Validation**
    - **Validates: Requirements 1.1**
  
  - [x] 2.3 Implement constraint validation
    - Validate budget_range against max_budget_cap
    - Validate risk_tolerance constraint
    - _Requirements: 1.3_
  
  - [ ]* 2.4 Write property test for budget constraint
    - **Property 2: Budget Constraint Enforcement**
    - **Validates: Requirements 1.3**
  
  - [x] 2.5 Implement assumption completeness check
    - Apply documented defaults for missing assumptions
    - Document which defaults are applied
    - _Requirements: 1.4_
  
  - [ ]* 2.6 Write property test for default assumptions
    - **Property 3: Default Assumption Application**
    - **Validates: Requirements 1.4**
  
  - [x] 2.7 Implement validation error response builder
    - Return structured error with error_code, error_message, validation_failures array
    - _Requirements: 1.5, 10.2_
  
  - [ ]* 2.8 Write property test for error response structure
    - **Property 4: Validation Error Structure**
    - **Validates: Requirements 1.5**

- [x] 3. Checkpoint - Validation component complete
  - Ensure all validation tests pass, ask the user if questions arise.

- [x] 4. Implement baseline extraction component
  - [x] 4.1 Create external system query interfaces
    - Implement query functions for Trend Lifecycle Engine, Early Decline Detection, ROI Attribution
    - Handle missing/stale data gracefully
    - _Requirements: 12.1, 12.2, 12.5_
  
  - [x] 4.2 Implement metric normalization
    - Normalize all metrics to 0-100 scale or percentage format
    - Verify normalized values are in correct range
    - _Requirements: 2.2_
  
  - [ ]* 4.3 Write property test for normalization
    - **Property 5: Metric Normalization Range**
    - **Validates: Requirements 2.2**
  
  - [x] 4.4 Implement data coverage computation
    - Calculate percentage of required data points available
    - Document missing data points
    - _Requirements: 2.3, 9.1_
  
  - [ ]* 4.5 Write property test for data coverage
    - **Property 6: Missing Data Documentation**
    - **Validates: Requirements 2.3**
  
  - [x] 4.6 Implement confidence adjustment logic
    - Reduce confidence when data is incomplete
    - Widen ranges when confidence < 50%
    - _Requirements: 2.4_
  
  - [ ]* 4.7 Write property test for confidence-based range widening
    - **Property 7: Confidence-Based Range Widening**
    - **Validates: Requirements 2.4**
  
  - [x] 4.8 Implement baseline source attribution
    - Preserve source of each metric for traceability
    - _Requirements: 2.5_
  
  - [ ]* 4.9 Write property test for source attribution
    - **Property 8: Baseline Source Attribution**
    - **Validates: Requirements 2.5**

- [x] 5. Checkpoint - Baseline extraction complete
  - Ensure all baseline extraction tests pass, ask the user if questions arise.

- [ ] 6. Implement range computation component - engagement growth
  - [x] 6.1 Implement engagement growth range computation
    - Apply campaign_strategy multipliers to baseline engagement_trend
    - Apply engagement_trend assumption modifiers (accelerating/stable/decelerating)
    - Apply creator_participation assumption modifiers (high/medium/low)
    - Apply market_noise assumption modifiers (widens range)
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_
  
  - [ ]* 6.2 Write property test for engagement growth range structure
    - **Property 9: Engagement Growth Range Structure**
    - **Validates: Requirements 3.1**
  
  - [ ]* 6.3 Write property test for campaign parameters affecting engagement
    - **Property 10: Campaign Parameters Affect Engagement Range**
    - **Validates: Requirements 3.2**
  
  - [ ]* 6.4 Write property test for accelerating trend
    - **Property 11: Accelerating Trend Increases Upper Bound**
    - **Validates: Requirements 3.3**
  
  - [ ]* 6.5 Write property test for decelerating trend
    - **Property 12: Decelerating Trend Decreases Upper Bound**
    - **Validates: Requirements 3.4**
  
  - [ ]* 6.6 Write property test for low creator participation
    - **Property 13: Low Creator Participation Reduces Bounds**
    - **Validates: Requirements 3.5**
  
  - [ ]* 6.7 Write property test for high market noise
    - **Property 14: High Market Noise Widens Range**
    - **Validates: Requirements 3.6**

- [ ] 7. Implement range computation component - reach growth
  - [x] 7.1 Implement reach growth range computation
    - Factor in creator_tier (conservative for nano/micro, aggressive for macro/mega)
    - Factor in campaign_duration_days (diminishing returns > 90 days)
    - Apply saturation reduction for peak lifecycle stage
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_
  
  - [ ]* 7.2 Write property test for reach growth range structure
    - **Property 15: Reach Growth Range Structure**
    - **Validates: Requirements 4.1**
  
  - [ ]* 7.3 Write property test for creator tier affecting reach
    - **Property 16: Creator Tier Affects Reach**
    - **Validates: Requirements 4.2, 4.3, 4.4**
  
  - [ ]* 7.4 Write property test for long campaign diminishing returns
    - **Property 17: Long Campaign Diminishing Returns**
    - **Validates: Requirements 4.5**
  
  - [ ]* 7.5 Write property test for peak stage reducing reach
    - **Property 18: Peak Stage Reduces Reach**
    - **Validates: Requirements 4.6**

- [ ] 8. Implement range computation component - ROI and probabilities
  - [x] 8.1 Implement ROI range computation
    - Use engagement_growth_percent and reach_growth_percent ranges as inputs
    - Query ROI Attribution system
    - _Requirements: 5.1, 5.2_
  
  - [ ]* 8.2 Write property test for ROI range structure
    - **Property 19: ROI Range Structure**
    - **Validates: Requirements 5.1**
  
  - [x] 8.3 Implement break-even probability computation
    - Calculate likelihood that roi_percent >= 0
    - _Requirements: 5.3_
  
  - [ ]* 8.4 Write property test for break-even probability
    - **Property 20: Break-Even Probability Correctness**
    - **Validates: Requirements 5.3**
  
  - [x] 8.5 Implement loss probability computation
    - Calculate likelihood that roi_percent < 0
    - _Requirements: 5.4_
  
  - [ ]* 8.6 Write property test for loss probability
    - **Property 21: Loss Probability Correctness**
    - **Validates: Requirements 5.4**
  
  - [ ]* 8.7 Write property test for probability complementarity
    - **Property 22: Probability Complementarity**
    - **Validates: Requirements 5.3, 5.4**
  
  - [x] 8.8 Implement probability adjustments
    - Reduce break_even_probability for high budget relative to baseline engagement
    - Increase loss_probability for decline/dormant lifecycle stages
    - _Requirements: 5.5, 5.6_
  
  - [ ]* 8.9 Write property test for high budget reducing break-even probability
    - **Property 23: High Budget Reduces Break-Even Probability**
    - **Validates: Requirements 5.5**
  
  - [ ]* 8.10 Write property test for decline stage increasing loss probability
    - **Property 24: Decline Stage Increases Loss Probability**
    - **Validates: Requirements 5.6**

- [ ] 9. Implement range computation component - risk projection
  - [x] 9.1 Implement risk score projection
    - Apply campaign_strategy parameters as risk modifiers
    - Increase risk for aggressive_growth + peak combination
    - Maintain/decrease risk for sustainable_engagement + growth combination
    - _Requirements: 6.1, 6.2, 6.3, 6.4_
  
  - [ ]* 9.2 Write property test for campaign parameters affecting risk
    - **Property 25: Campaign Parameters Affect Risk**
    - **Validates: Requirements 6.2**
  
  - [ ]* 9.3 Write property test for sustainable engagement maintaining risk
    - **Property 26: Sustainable Engagement Maintains Risk**
    - **Validates: Requirements 6.4**
  
  - [ ] 9.4 Implement risk tolerance constraint flagging
    - Flag scenarios where projected_risk_score exceeds current_risk_score and risk_tolerance is "low"
    - _Requirements: 6.5_
  
  - [ ]* 9.5 Write property test for risk tolerance constraint flagging
    - **Property 27: Risk Tolerance Constraint Flagging**
    - **Validates: Requirements 6.5**
  
  - [x] 9.6 Implement risk trend determination
    - Determine risk_trend (increasing/stable/decreasing) by comparing current vs projected
    - _Requirements: 6.6_
  
  - [ ]* 9.7 Write property test for risk trend determination
    - **Property 28: Risk Trend Determination**
    - **Validates: Requirements 6.6**

- [x] 10. Checkpoint - Range computation complete
  - Ensure all range computation tests pass, ask the user if questions arise.

- [ ] 11. Implement sensitivity analysis component
  - [x] 11.1 Implement assumption variation logic
    - For each assumption (engagement_trend, creator_participation, market_noise), compute output ranges with each possible value
    - Measure range width for each output metric
    - _Requirements: 7.1_
  
  - [ ]* 11.2 Write property test for most sensitive factor identification
    - **Property 29: Most Sensitive Factor Identification**
    - **Validates: Requirements 7.1**
  
  - [ ] 11.3 Implement impact_if_wrong computation
    - Describe change in key outputs if most_sensitive_factor is inverted or significantly altered
    - _Requirements: 7.3_
  
  - [ ]* 11.4 Write property test for impact if wrong computation
    - **Property 30: Impact If Wrong Computation**
    - **Validates: Requirements 7.3**
  
  - [ ] 11.5 Implement sensitive factor surfacing in decision interpretation
    - Ensure most_sensitive_factor is mentioned in decision_interpretation
    - _Requirements: 7.4, 7.5, 7.6_
  
  - [ ]* 11.6 Write property test for sensitive factor surfacing
    - **Property 31: Sensitive Factor Surfacing**
    - **Validates: Requirements 7.4**

- [ ] 12. Implement interpretation component
  - [x] 12.1 Implement recommended posture logic
    - "aggressive": break_even_probability >= 70% AND risk_trend in [stable, decreasing]
    - "moderate": break_even_probability in [40%, 70%] AND risk_trend = stable
    - "conservative": break_even_probability < 40% OR risk_trend = increasing
    - "avoid": lifecycle_stage in [decline, dormant] AND loss_probability > 60%
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_
  
  - [ ]* 12.2 Write property test for recommended posture computation
    - **Property 32: Recommended Posture Computation**
    - **Validates: Requirements 8.1**
  
  - [x] 12.3 Implement opportunities identification
    - Identify primary_opportunities based on reach potential, creator availability, engagement trend
    - _Requirements: 8.6_
  
  - [ ]* 12.4 Write property test for opportunities identification
    - **Property 33: Opportunities Identification**
    - **Validates: Requirements 8.6**
  
  - [x] 12.5 Implement risks identification
    - Identify primary_risks based on volatility, declining trends, budget constraints
    - _Requirements: 8.7_
  
  - [ ]* 12.6 Write property test for risks identification
    - **Property 34: Risks Identification**
    - **Validates: Requirements 8.7**

- [ ] 13. Implement guardrails and system notes
  - [x] 13.1 Implement system note generation
    - Generate notes for low data coverage, emerging/dormant stages, extreme budgets, constraint conflicts
    - _Requirements: 9.2, 9.5, 9.6, 9.7_
  
  - [ ]* 13.2 Write property test for low data coverage warning
    - **Property 36: Low Data Coverage Warning**
    - **Validates: Requirements 9.2**
  
  - [ ]* 13.3 Write property test for emerging/dormant stage note
    - **Property 39: Emerging/Dormant Stage Note**
    - **Validates: Requirements 9.5**
  
  - [ ]* 13.4 Write property test for extreme budget note
    - **Property 40: Extreme Budget Note**
    - **Validates: Requirements 9.6**
  
  - [ ]* 13.5 Write property test for constraint conflict documentation
    - **Property 41: Constraint Conflict Documentation**
    - **Validates: Requirements 9.7**

- [ ] 14. Implement output assembly and response building
  - [x] 14.1 Create simulation_summary builder
    - Compute overall_outlook based on break_even_probability and risk_trend
    - Include scenario_label and confidence
    - _Requirements: 10.1_
  
  - [x] 14.2 Create response builder
    - Assemble all output sections into SimulationResponse
    - Ensure all required fields are present
    - _Requirements: 10.1, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8_
  
  - [ ]* 14.3 Write property test for output structure completeness
    - **Property 42: Output Structure Completeness**
    - **Validates: Requirements 10.1**
  
  - [ ]* 14.4 Write property test for growth metrics structure
    - **Property 44: Growth Metrics Structure**
    - **Validates: Requirements 10.3**
  
  - [ ]* 14.5 Write property test for ROI metrics structure
    - **Property 45: ROI Metrics Structure**
    - **Validates: Requirements 10.4**
  
  - [ ]* 14.6 Write property test for risk projection structure
    - **Property 46: Risk Projection Structure**
    - **Validates: Requirements 10.5**
  
  - [ ]* 14.7 Write property test for decision interpretation structure
    - **Property 47: Decision Interpretation Structure**
    - **Validates: Requirements 10.6**
  
  - [ ]* 14.8 Write property test for assumption sensitivity structure
    - **Property 48: Assumption Sensitivity Structure**
    - **Validates: Requirements 10.7**
  
  - [ ]* 14.9 Write property test for guardrails structure
    - **Property 49: Guardrails Structure**
    - **Validates: Requirements 10.8**

- [ ] 15. Implement core simulation orchestration
  - [x] 15.1 Create main simulate() function
    - Orchestrate validation → baseline extraction → range computation → sensitivity analysis → interpretation → output assembly
    - Handle errors at each stage
    - _Requirements: 11.3, 11.4, 11.7_
  
  - [ ]* 15.2 Write property test for deterministic computation
    - **Property 50: Deterministic Computation**
    - **Validates: Requirements 11.3, 11.4**
  
  - [ ]* 15.3 Write property test for assumption documentation
    - **Property 51: Assumption Documentation**
    - **Validates: Requirements 11.7**

- [ ] 16. Implement scenario persistence layer
  - [ ] 16.1 Create scenario storage interface
    - Implement scenario creation with unique scenario_id
    - Implement scenario retrieval by scenario_id
    - Implement scenario versioning (preserve original, create new version on modification)
    - _Requirements: 13.1, 13.2, 13.3_
  
  - [ ] 16.2 Implement scenario metadata
    - Store created_timestamp, last_modified_timestamp, created_by_user_id
    - _Requirements: 13.4_
  
  - [ ] 16.3 Implement scenario filtering
    - Support filtering by trend_id, lifecycle_stage, date range
    - _Requirements: 13.5_
  
  - [ ]* 16.4 Write property test for scenario persistence
    - **Property 53: Scenario Persistence**
    - **Validates: Requirements 13.1**
  
  - [ ]* 16.5 Write property test for scenario retrieval
    - **Property 54: Scenario Retrieval**
    - **Validates: Requirements 13.2**
  
  - [ ]* 16.6 Write property test for scenario version preservation
    - **Property 55: Scenario Version Preservation**
    - **Validates: Requirements 13.3**
  
  - [ ]* 16.7 Write property test for scenario metadata inclusion
    - **Property 56: Scenario Metadata Inclusion**
    - **Validates: Requirements 13.4**
  
  - [ ]* 16.8 Write property test for scenario filtering
    - **Property 57: Scenario Filtering**
    - **Validates: Requirements 13.5**

- [x] 17. Checkpoint - Core simulator complete
  - Ensure all core simulator tests pass, ask the user if questions arise.

- [ ] 18. Create API endpoint wrapper
  - [ ] 18.1 Create HTTP endpoint for scenario submission
    - Accept ScenarioInput JSON
    - Return SimulationResponse JSON or error response
    - _Requirements: 10.1, 10.2_
  
  - [ ] 18.2 Create HTTP endpoint for scenario retrieval
    - Accept scenario_id
    - Return scenario configuration and simulation results
    - _Requirements: 13.2_
  
  - [ ] 18.3 Create HTTP endpoint for scenario listing
    - Support filtering by trend_id, lifecycle_stage, date range
    - _Requirements: 13.5_

- [ ] 19. Integration testing
  - [ ]* 19.1 Write integration tests for end-to-end simulation flow
    - Test complete flow from scenario submission to response
    - Test with various scenario configurations
    - _Requirements: All_
  
  - [ ]* 19.2 Write integration tests for external system interactions
    - Test graceful handling of missing/stale data from external systems
    - Test error propagation and documentation
    - _Requirements: 12.5_

- [x] 20. Final checkpoint - All tests pass
  - Ensure all unit tests, property tests, and integration tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional property-based and integration tests that can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation of each component
- Property tests validate universal correctness properties across generated inputs
- Unit tests validate specific examples and edge cases
- All code must follow deterministic, rule-based logic (no ML, no sentiment analysis)
- External system queries must handle missing/stale data gracefully
- All assumptions must be documented explicitly in output

