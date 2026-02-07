# Explainable Trend Intelligence Engine

**A Python module and FastAPI service for detecting and analyzing social media trend decline across multiple platforms with confidence-scored causal explanations.**

---

## 📋 Overview

This system detects whether a trend/meme/hashtag is losing momentum or collapsing, identifies **multiple contributing causes** across platforms (X, Reddit, TikTok, Google Trends), and quantifies each cause with **confidence scores (0–1)**.

### Key Features

✅ **Multi-platform analysis** (X, Reddit, TikTok, Google Trends)
✅ **9 distinct decline cause types** with confidence scoring
✅ **Causal explanations** grounded in actual metrics (never hallucinated)
✅ **Structured JSON output** for programmatic integration
✅ **Actionable recommendations** (recovery strategies or exit plans)
✅ **FastAPI REST service** for HTTP-based integration
✅ **Batch analysis** for analyzing multiple trends simultaneously
✅ **Executive summaries** in multiple formats (JSON, Markdown, CSV)

---

## 📦 Project Structure

```
trend-analyzer/
├── trend_analyzer.py      # Core TrendAnalyzer class
├── schemas.py             # Pydantic request/response models
├── api.py                 # FastAPI application
├── sample_data.py         # Sample datasets and loaders
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── examples.py            # Usage examples
└── sample_data_*.json     # Pre-made sample datasets
```

---

## 🚀 Installation

### Prerequisites
- Python 3.9+
- pip

### Setup

```bash
# Clone or navigate to the project directory
cd trend-analyzer

# Install dependencies
pip install -r requirements.txt
```

---

## 🎯 Quick Start

### Option 1: Direct Python Usage

```python
from trend_analyzer import TrendAnalyzer
from sample_data import load_sample_data
import json

# Initialize the analyzer
analyzer = TrendAnalyzer(min_confidence_threshold=0.3)

# Load sample data (declining trend)
metrics = load_sample_data("declining")

# Run analysis
result = analyzer.analyze(metrics)

# Print result as formatted JSON
print(json.dumps(result, indent=2))
```

### Option 2: FastAPI REST Service

```bash
# Start the API server
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

Then visit:
- **API Root:** http://localhost:8000
- **Swagger Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Test the API

```bash
# Test with sample data (declining trend)
curl http://localhost:8000/sample-analysis?sample_type=declining

# Test with custom data
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d @sample_data_declining.json
```

---

## 📊 Decline Cause Types

The analyzer detects up to 9 distinct causes of trend decline:

| Cause Type | Description | Confidence Range |
|-----------|-------------|------------------|
| **Engagement Decay** | Declining likes, retweets, comments, views | 0.3–1.0 |
| **Content Saturation** | Repetitive, lack of novelty | 0.3–1.0 |
| **Creator Disengagement** | Reduced posting frequency by creators | 0.3–1.0 |
| **Influencer Dropoff** | Key accounts stop participating | 0.6–1.0 |
| **Posting Frequency Collapse** | Overall volume drops >50% | 0.5–1.0 |
| **Algorithmic Visibility** | Platform algorithm de-prioritizes trend | 0.6–1.0 |
| **Audience Fatigue** | Users tired of the trend | 0.3–1.0 |
| **Competing Trend Emergence** | Related trends gaining interest | 0.6–1.0 |
| **Temporal Relevance Loss** | Event-based or seasonal decline | 0.5–1.0 |

---

## 📥 Input Schema

### Request Format

Send metrics as JSON following this structure:

```json
{
  "trend_name": "string (required)",
  "x": {
    "tweet_volume": {"current": 45000, "previous_period": 52000},
    "weekly_engagement_velocity": -0.15,
    "unique_content_ratio": 0.25,
    "posts_per_day": {"current": 2800, "previous_period": 3200},
    "reach_per_tweet": {"current": 850, "previous_period": 1100},
    "impression_velocity": -0.18,
    "top_accounts_participation": {"current": 42, "previous_period": 55},
    "top_influencer_engagement": {"current": 12500, "previous_period": 18000},
    "sentiment_score": {"current": -0.08, "previous_period": 0.15},
    "days_since_peak": 28
  },
  "reddit": {
    "posts_volume": {"current": 1200, "previous_period": 1600},
    "posts_per_day": {"current": 85, "previous_period": 115},
    "avg_comment_per_post": {"current": 8.5, "previous_period": 12.3},
    "upvote_ratio": {"current": 0.48},
    "subscriber_growth_rate": 0.005,
    "top_post_variance": 0.32
  },
  "tiktok": {
    "hashtag_views": {"current": 2800000, "previous_period": 3500000},
    "hashtag_video_count": {"current": 4200, "previous_period": 5800},
    "videos_per_day": {"current": 320, "previous_period": 480},
    "avg_engagement_rate": {"current": 0.042, "previous_period": 0.068},
    "sound_reuse_rate": 0.68,
    "hashtag_views_decline": -0.22
  },
  "google_trends": {
    "search_interest_score": 35,
    "search_interest_slope": -0.14,
    "seasonality_score": 0.85,
    "competing_trends": [
      {"name": "#DevLife", "trend_direction": "rising"}
    ],
    "category_interest_shift": {"this_trend": 35, "category_total": 120}
  }
}
```

### Field Notes

- **trend_name** (required): String identifier for the trend
- **All platforms optional:** Include only platforms with available data
- **PeriodMetric objects:** Compare current vs previous period (typically weekly)
- **Velocity metrics:** -0.15 = 15% decline per period
- **Ratios:** 0–1 scale (e.g., 0.68 = 68%)
- **Scores:** 0–100 range (Google Trends) or -1 to 1 (sentiment)

---

## 📤 Output Schema

### Response Format

```json
{
  "trend_name": "string",
  "analysis_timestamp": "2026-02-07T14:30:00Z",
  "trend_status": "GROWING|STABLE|DECLINING|COLLAPSED",
  "decline_probability": 0.72,
  "severity_level": "STABLE|WARNING|CRITICAL|COLLAPSED",
  "root_causes": [
    {
      "cause_type": "Engagement Decay",
      "confidence": 0.85,
      "severity_contribution": 0.68,
      "evidence": [
        "X engagement declining at -15.0% per week",
        "Reddit comments declined -35.3%"
      ],
      "affected_platforms": ["X", "Reddit"],
      "business_explanation": "Users are interacting less with content..."
    }
  ],
  "cross_platform_summary": {
    "X": {
      "tweet_volume": 45000,
      "engagement_velocity": -0.15,
      "health_status": "Declining"
    }
  },
  "recommended_actions": [
    {
      "action_type": "RECOVERY",
      "priority": "HIGH",
      "description": "Launch engagement campaign...",
      "expected_impact": "Reverse engagement decline by 30-50%",
      "timeframe": "Immediate (1-3 weeks)",
      "platforms_targeted": ["X", "Reddit"]
    }
  ],
  "confidence_in_analysis": 0.65
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `trend_status` | string | GROWING, STABLE, DECLINING, or COLLAPSED |
| `decline_probability` | float (0–1) | Confidence that trend is declining |
| `severity_level` | string | STABLE, WARNING, CRITICAL, or COLLAPSED |
| `root_causes` | array | Up to 9 detected causes, ranked by confidence |
| `confidence_in_analysis` | float (0–1) | Quality confidence of the analysis itself |

---

## 🔌 API Endpoints

### `POST /analyze`
Analyze a single trend from provided metrics.

**Request:** TrendMetricsInput JSON
**Response:** TrendAnalysisOutput JSON

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"trend_name": "MyTrend", "x": {...}, ...}'
```

---

### `GET /sample-analysis`
Run analysis on pre-loaded sample data (great for testing).

**Query Parameters:**
- `sample_type` (string): "declining" (default), "growing", or "collapsed"

**Response:** TrendAnalysisOutput JSON

```bash
curl "http://localhost:8000/sample-analysis?sample_type=declining"
```

---

### `POST /batch-analyze`
Analyze up to 100 trends in a single request.

**Request:** Array of TrendMetricsInput objects
**Response:** Object with results array, errors array, metadata

```bash
curl -X POST http://localhost:8000/batch-analyze \
  -H "Content-Type: application/json" \
  -d '[{"trend_name": "Trend1", ...}, {"trend_name": "Trend2", ...}]'
```

---

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-07T14:30:00Z",
  "service": "Trend Intelligence Engine"
}
```

---

### `GET /sample-metrics-schema`
Get sample JSON schema and structure.

---

### `GET /api-docs-markdown`
Get full API documentation in Markdown format.

---

## 💻 Python Module Usage

### Basic Analysis

```python
from trend_analyzer import TrendAnalyzer

analyzer = TrendAnalyzer()
result = analyzer.analyze(metrics_dict)
```

### With Confidence Threshold

```python
# Only report causes with >50% confidence
analyzer = TrendAnalyzer(min_confidence_threshold=0.5)
result = analyzer.analyze(metrics_dict)
```

### Utility Functions

```python
from utils import (
    generate_executive_summary,
    export_analysis_report,
    merge_trend_analyses,
    detect_platform_health
)

# Generate plain-English summary
summary = generate_executive_summary(result)
print(summary)

# Export in different formats
json_report = export_analysis_report(result, format="json")
md_report = export_analysis_report(result, format="markdown")
csv_report = export_analysis_report(result, format="csv")

# Track trend over time
analyses = [result1, result2, result3]  # Multiple analyses
trajectory = merge_trend_analyses(analyses)

# Get platform-specific health
health = detect_platform_health(result)
```

---

## 📝 Examples

### Example 1: Declining Trend Analysis

**Input:**
```python
from sample_data import load_sample_data
metrics = load_sample_data("declining")
```

**Output:**
```
Trend: #TechTok
Status: DECLINING (Decline Probability: 72%)
Severity: WARNING

Root Causes (ranked by confidence):
1. Engagement Decay (85% confidence)
   Users are interacting less with content (fewer likes, comments, shares, retweets).

2. Content Saturation (72% confidence)
   The trend has become oversaturated with repetitive content.

3. Creator Disengagement (65% confidence)
   Content creators are posting less frequently.

Recommended Actions:
- [HIGH] Launch engagement campaign with creator partnerships
- [HIGH] Refresh trend with new creative angles
- [MEDIUM] Set up daily monitoring dashboards
```

---

### Example 2: Growing Trend Analysis

```python
metrics = load_sample_data("growing")
result = analyzer.analyze(metrics)
```

**Status:** GROWING
**Decline Probability:** 0.05 (5%)
**Recommended Actions:** Monitor and capitalize on momentum

---

### Example 3: Batch Analysis

```python
from schemas import TrendMetricsInput

trends = [
    TrendMetricsInput(trend_name="Trend1", x={...}),
    TrendMetricsInput(trend_name="Trend2", reddit={...}),
]

# Via Python
results = [analyzer.analyze(t.model_dump(exclude_none=True)) for t in trends]

# Via API
response = requests.post(
    "http://localhost:8000/batch-analyze",
    json=[t.model_dump() for t in trends]
)
```

---

## 🧮 Confidence Score Calculation

Confidence scores are calculated based on:

1. **Evidence availability:** More platforms with data = higher confidence
2. **Metric consistency:** Multiple metrics supporting same cause = higher confidence
3. **Threshold validation:** Metrics exceeding known thresholds = higher confidence
4. **Cross-platform corroboration:** Same cause detected on multiple platforms = higher confidence

**Formula (simplified):**
```
cause_confidence = (evidence_count * 0.4) + (platform_count * 0.3) + (data_quality * 0.3)
```

---

## 🎨 Business Language Explanations

Every detected cause includes a **business_explanation** field written in plain English, avoiding jargon:

- **NOT:** "Engagement velocity delta < -0.15 threshold exceeded"
- **YES:** "Users are interacting less with content (fewer likes, comments, shares, retweets). This suggests waning interest or reduced visibility."

---

## ⚙️ Configuration

### Adjust Detection Thresholds

Edit the `MetricThresholds` dataclass in [utils.py](utils.py):

```python
@dataclass
class MetricThresholds:
    engagement_decay_threshold: float = -0.10  # -10% weekly
    content_saturation_unique_ratio: float = 0.30  # <30% unique
    creator_disengagement_threshold: float = -0.25  # -25% posting
    # ... etc
```

### Adjust Confidence Threshold

```python
analyzer = TrendAnalyzer(min_confidence_threshold=0.5)  # Only report >50% confidence
```

---

## 🔒 Data Privacy

- **No data persistence:** All analyses are stateless per request
- **No external API calls:** Uses provided metrics only
- **No hallucination:** Causes detected only when metrics support them
- **No personally identifiable information:** Analyzes aggregate metrics only

---

## 📈 Time-Based Trend Tracking (Future Extension)

Currently, the system analyzes snapshots. To extend for trend tracking:

```python
# Future: Track same trend over time
analyses_over_time = [
    analyzer.analyze(metrics_week1),
    analyzer.analyze(metrics_week2),
    analyzer.analyze(metrics_week3),
]

trajectory = merge_trend_analyses(analyses_over_time)
# Returns: momentum, emerging_causes, acceleration indicators
```

---

## 🛠️ Development

### Running Tests

```bash
# Generate sample data
python sample_data.py

# Run analysis on samples
python -c "from trend_analyzer import TrendAnalyzer; from sample_data import load_sample_data; \
    a = TrendAnalyzer(); print(a.analyze(load_sample_data('declining')))"
```

### Adding New Cause Types

1. Add method `_detect_new_cause()` to `TrendAnalyzer` class
2. Call method in `_detect_all_causes()`
3. Add cause type to `CAUSE_TYPES` dictionary
4. Test with sample data

### Extending Output Schema

1. Modify `TrendAnalysisOutput` in [schemas.py](schemas.py)
2. Update response models
3. Update API endpoint documentation

---

## ❓ FAQ

**Q: Can I use this without the FastAPI wrapper?**
A: Yes! Import `TrendAnalyzer` directly and call `.analyze(metrics)`.

**Q: What if I don't have data from all platforms?**
A: The system works with any subset. Include only available data; confidence will adjust accordingly.

**Q: How accurate are the confidence scores?**
A: Confidence reflects evidence quality, not prediction accuracy. A 0.9 confidence cause is well-supported by metrics but may not perfectly predict outcomes.

**Q: Can I modify the cause types?**
A: Yes, edit `_detect_*` methods in [trend_analyzer.py](trend_analyzer.py) and add custom logic.

**Q: Is this suitable for production?**
A: Yes, with proper monitoring. FastAPI provides async support, validation, and error handling.

---

## 📚 References

### Input Metrics Sources

- **X (Twitter):** Twitter API v2, TweetDeck analytics, RapidAPI
- **Reddit:** PRAW (Python Reddit API Wrapper), Pushshift, Subreddit analytics
- **TikTok:** Apify, TikTok Analytics, TikTok API
- **Google Trends:** PyTrends, Google Trends website

### Metric Collection Tips

- Collect metrics on **weekly basis** for trend tracking
- Use **consistent time windows** (e.g., last 7 days vs previous 7 days)
- Include **at least 2 platforms** for meaningful analysis
- Validate metrics for **data quality** before analysis

---

## 📝 License

This project is provided as-is for educational and analytical purposes.

---

## 🤝 Contributing

To improve the engine:

1. Add new decline cause detection methods
2. Refine confidence scoring algorithms
3. Expand recovery strategy recommendations
4. Add support for additional platforms
5. Improve business language explanations

---

## 📧 Support

For issues or questions:
1. Check the FAQ section above
2. Review sample data and examples
3. Test with `GET /sample-analysis` endpoint
4. Check API logs for error details

---

**Happy trend analyzing! 📊**
