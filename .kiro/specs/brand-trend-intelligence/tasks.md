# Implementation Plan: Brand Trend Revenue Intelligence Agent

## Overview

This implementation plan breaks down the Brand Trend Revenue Intelligence Agent into discrete coding tasks. The system will be built incrementally, starting with core data models and services, then adding classification logic, recommendation generation, and finally the terminal interface. Each task builds on previous work to ensure continuous integration.

## Tasks

- [x] 1. Set up project structure and dependencies
  - Create main project directory structure (src/, tests/, config/)
  - Create requirements.txt with dependencies: pytrends, groq, hypothesis, pytest, pandas
  - Set up virtual environment activation script
  - Create .env.example file for GROQ_API_KEY
  - _Requirements: 5.1, 7.4_

- [ ] 2. Implement core data models
  - [x] 2.1 Create data model classes using dataclasses
    - Implement TrendData, TrendMetrics, TrendClassification
    - Implement GrowthRecommendations, GrowthAction, BudgetStrategy, ImpactMetrics
    - Implement DeclineAnalysis, AlternativeTrend, PivotStrategy
    - Add type hints and validation
    - _Requirements: All requirements (data foundation)_
  
  - [ ]* 2.2 Write property test for data model serialization
    - **Property: Data model round-trip**
    - **Validates: Requirements 6.1**
    - Test that all data models can be serialized to dict and back without data loss

- [ ] 3. Implement Input Validator
  - [x] 3.1 Create InputValidator class with validation methods
    - Implement validate_domain() method
    - Implement prompt_for_domain() method for terminal input
    - Add whitespace stripping and normalization
    - _Requirements: 7.1, 7.2_
  
  - [ ]* 3.2 Write property test for input validation
    - **Property 7: Input validation rejects empty domains**
    - **Validates: Requirements 7.2**
    - Generate random whitespace/empty strings, verify rejection

- [ ] 4. Implement Trend Discovery Service
  - [x] 4.1 Create TrendDiscoveryService class with pytrends integration
    - Initialize pytrends TrendReq client
    - Implement discover_trends() method
    - Implement get_trend_interest_over_time() method
    - Add error handling for API failures and rate limiting
    - _Requirements: 1.1, 1.2, 1.3, 1.4_
  
  - [ ]* 4.2 Write property test for trend discovery
    - **Property 1: Trend discovery returns sufficient results**
    - **Validates: Requirements 1.1, 1.3**
    - Mock pytrends, generate random domains, verify >= 3 results returned
  
  - [ ]* 4.3 Write unit tests for trend discovery edge cases
    - Test no trends found scenario
    - Test API timeout handling
    - Test rate limiting behavior
    - _Requirements: 1.4_

- [ ] 5. Implement Trend Analyzer
  - [x] 5.1 Create TrendAnalyzer class with growth calculation
    - Implement calculate_growth_slope() using linear regression
    - Implement analyze_trend_momentum() method
    - Add normalization to percentage growth rate
    - _Requirements: 2.5_
  
  - [ ]* 5.2 Write property test for growth slope determinism
    - **Property 3: Growth slope determinism**
    - **Validates: Requirements 2.5**
    - Generate random interest time series, calculate slope twice, verify identical results

- [ ] 6. Implement Trend Classifier
  - [x] 6.1 Create TrendClassifier class with classification logic
    - Implement classify() method with threshold-based logic
    - Define thresholds: growing >5%, stable -5% to +5%, declining <-5%
    - Add confidence score calculation
    - _Requirements: 2.1, 2.2, 2.3, 2.4_
  
  - [ ]* 6.2 Write property test for classification correctness
    - **Property 2: Classification correctness**
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.4**
    - Generate random growth slopes, verify classification matches threshold rules

- [ ] 7. Checkpoint - Ensure core analysis pipeline works
  - Run all tests for data models, validator, discovery, analyzer, and classifier
  - Verify integration between components
  - Ask user if questions arise

- [ ] 8. Implement GROQ API Service
  - [x] 8.1 Create GroqService class with API integration
    - Initialize Groq client with API key from environment
    - Implement generate_analysis() method using chat.completions.create()
    - Add error handling for authentication, rate limiting, timeouts
    - Implement exponential backoff for retries
    - _Requirements: 5.1, 5.2, 5.3, 5.4_
  
  - [ ]* 8.2 Write unit tests for GROQ service error handling
    - Test authentication failure
    - Test rate limiting with mocked responses
    - Test service unavailability
    - _Requirements: 5.3, 5.4_

- [ ] 9. Implement Growth Recommender
  - [x] 9.1 Create GrowthRecommender class with GROQ integration
    - Implement generate_recommendations() method
    - Create structured prompt template for growth recommendations
    - Parse GROQ response into GrowthRecommendations data model
    - Ensure exactly 3 actions, budget strategy, and quantified impact
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_
  
  - [ ]* 9.2 Write property test for complete growth recommendations
    - **Property 4: Complete growth recommendations**
    - **Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5**
    - Generate random growing trend data, verify recommendation completeness
  
  - [ ]* 9.3 Write property test for data integrity in recommendations
    - **Property 8: Data integrity in recommendations**
    - **Validates: Requirements 8.1, 8.2, 8.4**
    - Verify output metrics are derived from input, not hallucinated

- [ ] 10. Implement Decline Analyzer
  - [x] 10.1 Create DeclineAnalyzer class with GROQ integration
    - Implement analyze_decline() method
    - Create structured prompt template for decline analysis
    - Calculate days until collapse using decay rate
    - Estimate marketing burn projection
    - Determine EXIT vs TRY REVIVAL recommendation
    - Parse GROQ response for alternative trends and pivot strategy
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_
  
  - [ ]* 10.2 Write property test for complete decline analysis
    - **Property 5: Complete decline analysis**
    - **Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.5**
    - Generate random declining trend data, verify analysis completeness

- [ ] 11. Implement Response Formatter
  - [x] 11.1 Create ResponseFormatter class with JSON output
    - Implement format_response() method
    - Add JSON validation before output
    - Implement pretty-printing for readability
    - Handle serialization of custom data models
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_
  
  - [ ]* 11.2 Write property test for valid JSON output
    - **Property 6: Valid and complete JSON output**
    - **Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5**
    - Generate random analysis results, verify JSON validity and completeness
  
  - [ ]* 11.3 Write property test for reasoning references
    - **Property 9: Reasoning references actual metrics**
    - **Validates: Requirements 8.3**
    - Verify reasoning text contains numeric values from input metrics

- [ ] 12. Checkpoint - Ensure recommendation pipeline works
  - Run all tests for GROQ service, recommenders, and formatter
  - Test end-to-end flow from classification to formatted output
  - Ask user if questions arise

- [ ] 13. Implement main application pipeline
  - [x] 13.1 Create main application orchestrator
    - Wire together all components (validator → discovery → analyzer → classifier → recommender → formatter)
    - Implement error handling and propagation
    - Add logging for debugging
    - _Requirements: All requirements (integration)_
  
  - [ ]* 13.2 Write integration tests for complete pipeline
    - Test growing trend end-to-end flow
    - Test declining trend end-to-end flow
    - Test stable trend end-to-end flow
    - Test error scenarios
    - _Requirements: All requirements_

- [ ] 14. Implement terminal interface
  - [x] 14.1 Create terminal UI with input prompts
    - Implement main() function with terminal input/output
    - Add clear prompts for domain input
    - Display formatted JSON output
    - Add error message display
    - _Requirements: 7.1, 7.2, 7.3_
  
  - [ ]* 14.2 Write property test for uncertainty indication
    - **Property 10: Uncertainty indication for sparse data**
    - **Validates: Requirements 8.5**
    - Generate sparse trend data, verify uncertainty indicators present

- [ ] 15. Add configuration and environment setup
  - [x] 15.1 Create configuration management
    - Load GROQ_API_KEY from environment
    - Add configuration for thresholds (growth/decline percentages)
    - Create config.py for centralized settings
    - Add validation for required environment variables
    - _Requirements: 5.1, 7.4_

- [ ] 16. Final checkpoint and testing
  - Run complete test suite (unit + property tests)
  - Test with real GROQ API (manual verification)
  - Verify all 10 correctness properties pass
  - Test with various domain inputs
  - Ensure all tests pass, ask user if questions arise

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Property tests validate universal correctness properties with 100+ iterations
- Unit tests validate specific examples and edge cases
- Mock external APIs (pytrends, GROQ) in automated tests
- The system uses the existing venv environment
