"""
Quick Reference Guide - Twitter Trend Analyzer API
===================================================

ENDPOINT SUMMARY TABLE
"""

# Core Analysis Endpoints
"""
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ANALYSIS ENDPOINTS                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│ 1. POST /analyze                                                             │
│    ────────────────────────────────────────────────────────────────────────  │
│    Purpose: Core trend analysis with decline cause detection                │
│    Input: TrendMetricsInput (trend_name + X metrics)                        │
│    Output: TrendAnalysisOutput (status, causes, confidence)                 │
│    Speed: 100-200ms                                                         │
│    Use: Fast analysis for monitoring, dashboards, integrations             │
│                                                                               │
│    CURL Example:                                                            │
│    curl -X POST "http://localhost:8000/analyze" \                          │
│      -H "Content-Type: application/json" \                                 │
│      -d '{                                                                  │
│        "trend_name": "#TechTok",                                           │
│        "x": {                                                               │
│          "tweet_volume": {"current": 45000, "previous_period": 52000},    │
│          "weekly_engagement_velocity": -0.15,                             │
│          "unique_content_ratio": 0.25                                      │
│        }                                                                    │
│      }'                                                                      │
│                                                                               │
│ 2. GET /sample-analysis?sample_type=declining                               │
│    ────────────────────────────────────────────────────────────────────────  │
│    Purpose: Test with pre-loaded sample data                               │
│    Query Params: sample_type (declining|growing|collapsed)                 │
│    Output: Same as /analyze                                                │
│    Speed: 100-200ms                                                         │
│    Use: Testing, demos, learning                                            │
│                                                                               │
│    CURL Example:                                                            │
│    curl "http://localhost:8000/sample-analysis?sample_type=declining"     │
│                                                                               │
│ 3. POST /batch-analyze                                                      │
│    ────────────────────────────────────────────────────────────────────────  │
│    Purpose: Analyze multiple trends (max 100)                              │
│    Input: Array of TrendMetricsInput                                       │
│    Output: Results array + metadata                                        │
│    Speed: Linear with trend count (~100ms per trend)                       │
│    Use: Bulk processing, monitoring dashboards, batch jobs                │
│                                                                               │
│    CURL Example:                                                            │
│    curl -X POST "http://localhost:8000/batch-analyze" \                   │
│      -H "Content-Type: application/json" \                                 │
│      -d '[                                                                  │
│        {"trend_name": "#Tech", "x": {...}},                               │
│        {"trend_name": "#Code", "x": {...}}                                │
│      ]'                                                                      │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# AI Explanation Endpoints
"""
┌─────────────────────────────────────────────────────────────────────────────┐
│                      AI-POWERED EXPLANATION ENDPOINTS                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ Note: Requires Featherless AI API key configured                            │
│                                                                               │
│ 4. POST /explain                                                             │
│    ────────────────────────────────────────────────────────────────────────  │
│    Purpose: Get AI explanations for detected causes (2-3 sentences each)    │
│    Input: TrendMetricsInput (same as /analyze)                             │
│    Output: Analysis + AI explanations per cause                            │
│    Speed: 2-5 seconds (includes LLM calls)                                 │
│    Use: Detailed cause understanding, stakeholder communication            │
│                                                                               │
│    CURL Example:                                                            │
│    curl -X POST "http://localhost:8000/explain" \                         │
│      -H "Content-Type: application/json" \                                 │
│      -d '{                                                                  │
│        "trend_name": "#TechTok",                                           │
│        "x": {...}                                                           │
│      }'                                                                      │
│                                                                               │
│ 5. POST /strategy                                                            │
│    ────────────────────────────────────────────────────────────────────────  │
│    Purpose: Generate recovery or exit strategy (3-4 paragraphs)            │
│    Input: TrendMetricsInput                                                 │
│    Output: Trend status + AI-generated strategic recommendation            │
│    Speed: 3-8 seconds                                                       │
│    Use: Decision support, action planning, recovery initiatives            │
│                                                                               │
│    CURL Example:                                                            │
│    curl -X POST "http://localhost:8000/strategy" \                        │
│      -H "Content-Type: application/json" \                                 │
│      -d '{                                                                  │
│        "trend_name": "#CryptoRally",                                       │
│        "x": {...}                                                           │
│      }'                                                                      │
│                                                                               │
│ 6. POST /executive-summary                                                   │
│    ────────────────────────────────────────────────────────────────────────  │
│    Purpose: C-level executive summary for board presentations              │
│    Input: TrendMetricsInput                                                 │
│    Output: Business-focused 2-3 paragraph summary                          │
│    Speed: 2-4 seconds                                                       │
│    Use: Executive briefings, board decks, stakeholder reports              │
│                                                                               │
│    CURL Example:                                                            │
│    curl -X POST "http://localhost:8000/executive-summary" \               │
│      -H "Content-Type: application/json" \                                 │
│      -d '{                                                                  │
│        "trend_name": "#TechTok",                                           │
│        "x": {...}                                                           │
│      }'                                                                      │
│                                                                               │
│ 7. POST /full-report                                                         │
│    ────────────────────────────────────────────────────────────────────────  │
│    Purpose: Comprehensive report (analysis + explanations + strategy)       │
│    Input: TrendMetricsInput                                                 │
│    Output: Complete multi-section report JSON                              │
│    Speed: 5-15 seconds                                                      │
│    Use: Comprehensive documentation, deep-dive analysis, archival          │
│                                                                               │
│    CURL Example:                                                            │
│    curl -X POST "http://localhost:8000/full-report" \                     │
│      -H "Content-Type: application/json" \                                 │
│      -d '{                                                                  │
│        "trend_name": "#WebDevelopment",                                    │
│        "x": {...}                                                           │
│      }'                                                                      │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# Utility Endpoints
"""
┌─────────────────────────────────────────────────────────────────────────────┐
│                          UTILITY ENDPOINTS                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│ 8. GET /health                                                               │
│    ────────────────────────────────────────────────────────────────────────  │
│    Purpose: Service health check                                            │
│    Output: Status + timestamp                                               │
│    Use: Monitoring, load balancer checks                                    │
│                                                                               │
│ 9. GET /sample-metrics-schema                                               │
│    ────────────────────────────────────────────────────────────────────────  │
│    Purpose: View input schema structure                                     │
│    Output: Example JSON with schema notes                                   │
│    Use: API documentation, integration reference                           │
│                                                                               │
│ 10. GET /api-docs-markdown                                                  │
│     ────────────────────────────────────────────────────────────────────────  │
│     Purpose: API documentation in Markdown                                  │
│     Output: Complete API reference                                          │
│     Use: Developer documentation                                            │
│                                                                               │
│ 11. GET /docs (auto-generated)                                              │
│     ────────────────────────────────────────────────────────────────────────  │
│     Purpose: Interactive API documentation (Swagger UI)                     │
│     Access: http://localhost:8000/docs                                      │
│     Use: Interactive testing, endpoint exploration                         │
│                                                                               │
│ 12. GET /redoc (auto-generated)                                             │
│     ────────────────────────────────────────────────────────────────────────  │
│     Purpose: API documentation (ReDoc)                                      │
│     Access: http://localhost:8000/redoc                                     │
│     Use: Beautiful API documentation                                        │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# Input Schema
"""
┌─────────────────────────────────────────────────────────────────────────────┐
│                         INPUT SCHEMA (REQUIRED)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│ TrendMetricsInput:                                                          │
│ {                                                                            │
│   "trend_name": "string (required)",    # Hashtag or topic name           │
│   "x": {                                # X/Twitter metrics (required)     │
│     "tweet_volume": {                                                       │
│       "current": number,                # Current tweet volume             │
│       "previous_period": number         # Previous period for comparison   │
│     },                                                                       │
│     "weekly_engagement_velocity": number,  # Engagement trend (-1.0 to 1.0)│
│     "unique_content_ratio": number,        # Content diversity (0.0-1.0)  │
│     "creator_posting_frequency": {                                         │
│       "current": number,                # Current posts per week           │
│       "previous_period": number         # Previous week posts             │
│     },                                                                       │
│     "influencer_engagement_count": number, # Active influencers           │
│     "audience_growth_rate": number,        # Growth rate (-1.0 to 1.0)   │
│     "posting_frequency_change": number     # Frequency change (-1.0-1.0) │
│   }                                                                          │
│ }                                                                            │
│                                                                               │
│ All X metrics are optional (more metrics = higher confidence)              │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# Response Schema
"""
┌─────────────────────────────────────────────────────────────────────────────┐
│                        RESPONSE SCHEMA (ANALYSIS)                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│ TrendAnalysisOutput:                                                        │
│ {                                                                            │
│   "trend_name": "string",                                                   │
│   "trend_status": "GROWING|STABLE|DECLINING|COLLAPSED",                   │
│   "decline_probability": 0.0-1.0,       # Confidence in decline (0-100%)  │
│   "severity_level": "STABLE|WARNING|CRITICAL|COLLAPSED",                  │
│   "root_causes": [                                                          │
│     {                                                                        │
│       "cause_type": "string",            # Type of decline cause          │
│       "confidence": 0.0-1.0,             # Confidence in this cause       │
│       "severity_contribution": 0.0-1.0,  # How much it contributes       │
│       "evidence": ["string"],            # Supporting evidence             │
│       "affected_platforms": ["string"],  # Where it's detected             │
│       "business_explanation": "string"   # Human-readable explanation     │
│     }                                                                        │
│   ],                                                                         │
│   "cross_platform_summary": {...},      # Health per platform             │
│   "recommended_actions": [              # Recovery or exit strategies      │
│     {                                                                        │
│       "action_type": "RECOVERY|EXIT",                                      │
│       "recommendation": "string",        # What to do                      │
│       "rationale": "string",             # Why to do it                    │
│       "expected_impact": "string",       # Potential outcome              │
│       "timeline": "string",              # When to execute                 │
│       "resources_required": "string"     # What's needed                   │
│     }                                                                        │
│   ],                                                                         │
│   "confidence_in_analysis": 0.0-1.0    # How confident in overall analysis│
│ }                                                                            │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# Error Response
"""
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ERROR RESPONSES                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│ 400 Bad Request:                                                            │
│ {                                                                            │
│   "detail": "Error message explaining what was wrong"                      │
│ }                                                                            │
│                                                                               │
│ 503 Service Unavailable:                                                    │
│ {                                                                            │
│   "detail": "AI explanation service not available. Please configure..."    │
│ }                                                                            │
│                                                                               │
│ 500 Internal Server Error:                                                  │
│ {                                                                            │
│   "detail": "Error during analysis: [error details]"                       │
│ }                                                                            │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# Common Workflows
"""
┌─────────────────────────────────────────────────────────────────────────────┐
│                        COMMON WORKFLOW EXAMPLES                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│ WORKFLOW 1: Quick Health Check                                              │
│ ─────────────────────────────────────                                       │
│   1. GET /sample-analysis?sample_type=declining  (test endpoint)           │
│   2. Check trend_status and severity_level                                  │
│   3. Review root_causes for quick understanding                             │
│                                                                               │
│ WORKFLOW 2: Detailed Analysis                                               │
│ ──────────────────────────────────                                          │
│   1. POST /analyze (basic structural analysis)                              │
│   2. POST /explain (detailed AI explanations)                               │
│   3. POST /strategy (get recovery recommendations)                          │
│   4. Review and implement recommendations                                   │
│                                                                               │
│ WORKFLOW 3: Executive Reporting                                             │
│ ────────────────────────────────                                            │
│   1. POST /batch-analyze (analyze all trends)                               │
│   2. Filter critical trends (decline_probability > 0.6)                     │
│   3. POST /executive-summary (for each critical trend)                      │
│   4. Compile summaries into board deck                                      │
│                                                                               │
│ WORKFLOW 4: Comprehensive Documentation                                     │
│ ─────────────────────────────────────────                                   │
│   1. POST /full-report (get everything in one call)                         │
│   2. Extract sections for different audiences                               │
│   3. Archive JSON for historical comparison                                 │
│   4. Use for future trend prediction/ML                                     │
│                                                                               │
│ WORKFLOW 5: Real-Time Monitoring                                            │
│ ────────────────────────────────                                            │
│   1. Poll /sample-analysis periodically                                     │
│   2. Monitor for severity changes                                           │
│   3. Alert stakeholders when status changes                                 │
│   4. GET /explain only for critical trends                                  │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# Performance Tips
"""
┌─────────────────────────────────────────────────────────────────────────────┐
│                          PERFORMANCE TIPS                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│ Fast Analysis:                                                              │
│   • Use /analyze for real-time monitoring (<100ms response)                │
│   • Cache results for identical inputs                                      │
│   • Use /batch-analyze for multiple trends in one request                  │
│                                                                               │
│ AI Explanations:                                                            │
│   • /explain, /strategy, /executive-summary: 2-15 seconds                  │
│   • Cache these expensive results when possible                            │
│   • Run as background jobs for non-critical paths                          │
│   • Use /full-report sparingly (combines all AI calls)                     │
│                                                                               │
│ Scaling:                                                                    │
│   • Start with /analyze in production                                      │
│   • Add /explain only for critical trends                                  │
│   • Use async job queues for /full-report generation                       │
│   • Implement Redis caching for frequently analyzed trends                 │
│   • Run multiple API instances behind load balancer                        │
│                                                                               │
│ Configuration:                                                              │
│   • Set MIN_CONFIDENCE_THRESHOLD = 0.3 for balanced sensitivity            │
│   • Increase to 0.5 to reduce false positives                              │
│   • Decrease to 0.2 for more comprehensive cause detection                 │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# Getting Started
"""
┌─────────────────────────────────────────────────────────────────────────────┐
│                           GETTING STARTED                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│ 1. INSTALL DEPENDENCIES:                                                    │
│    pip install fastapi uvicorn pydantic openai requests python-dotenv      │
│                                                                               │
│ 2. CONFIGURE API KEYS:                                                      │
│    export FEATHERLESS_API_KEY="your_key_here"                              │
│    export TWITTER_API_KEY="your_key_here"                                  │
│                                                                               │
│ 3. START SERVER:                                                            │
│    python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000          │
│                                                                               │
│ 4. TEST API:                                                                │
│    curl http://localhost:8000/sample-analysis?sample_type=declining       │
│                                                                               │
│ 5. INTERACTIVE DOCS:                                                        │
│    Open http://localhost:8000/docs in browser                              │
│                                                                               │
│ 6. RUN EXAMPLES:                                                            │
│    python examples_ai_endpoints.py                                         │
│                                                                               │
│ 7. FULL DEMO:                                                               │
│    python demo_all_features.py                                             │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
"""

print(__doc__)
