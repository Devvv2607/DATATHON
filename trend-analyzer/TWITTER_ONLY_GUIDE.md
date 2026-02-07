# Twitter Trend Intelligence Engine - Quick Start

**Version 2.0 - Twitter/X Only Edition**

## What This Does

Analyzes Twitter trends to detect decline causes and provides confidence-scored explanations.

## Core Features

✅ **8 Decline Causes Detected:**
1. Engagement Decay (declining likes/retweets)
2. Content Saturation (repetitive posts)
3. Creator Disengagement (fewer posts)
4. Influencer Dropoff (top accounts stopped)
5. Posting Volume Collapse (massive volume decline)
6. Algorithmic Visibility (reduced reach)
7. Audience Fatigue (negative sentiment)
8. Temporal Relevance Loss (peak was long ago)

✅ **Confidence Scoring:** Each cause gets 0-1 confidence score
✅ **Business Explanations:** Plain English, no jargon
✅ **Actionable Recommendations:** Recovery strategies or exit plans
✅ **Stateless Analysis:** Each request independent

## Quick Start

### Installation
```bash
cd trend-analyzer
pip install -r requirements.txt
```

### Run API Server
```bash
python -m uvicorn api:app --reload --port 8000
```

Visit: http://localhost:8000/docs (Swagger UI)

### Analyze a Trend (Python)
```python
from trend_analyzer import TrendAnalyzer
from sample_data import load_sample_data

analyzer = TrendAnalyzer()
metrics = load_sample_data("declining")
result = analyzer.analyze(metrics)

print(result["trend_status"])          # DECLINING
print(result["decline_probability"])   # 0.72
print(result["root_causes"])           # List of detected causes
```

### Analyze a Trend (HTTP)
```bash
curl http://localhost:8000/sample-analysis?sample_type=declining

# Or post custom metrics:
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "trend_name": "MyTrend",
    "x": {
      "tweet_volume": {"current": 45000, "previous_period": 52000},
      "weekly_engagement_velocity": -0.15
    }
  }'
```

## Input Format

```json
{
  "trend_name": "string (required)",
  "x": {
    "tweet_volume": {"current": number, "previous_period": number},
    "weekly_engagement_velocity": number,
    "unique_content_ratio": number (0-1),
    "posts_per_day": {"current": number, "previous_period": number},
    "reach_per_tweet": {"current": number, "previous_period": number},
    "impression_velocity": number,
    "top_accounts_participation": {"current": number, "previous_period": number},
    "top_influencer_engagement": {"current": number, "previous_period": number},
    "sentiment_score": {"current": number, "previous_period": number},
    "days_since_peak": number
  }
}
```

**All X metrics are optional but provide more data = higher confidence.**

## Output Format

```json
{
  "trend_name": "string",
  "analysis_timestamp": "ISO datetime",
  "trend_status": "GROWING|STABLE|DECLINING|COLLAPSED",
  "decline_probability": 0.0-1.0,
  "severity_level": "STABLE|WARNING|CRITICAL|COLLAPSED",
  "root_causes": [
    {
      "cause_type": "string",
      "confidence": 0.0-1.0,
      "severity_contribution": 0.0-1.0,
      "evidence": ["string"],
      "affected_platforms": ["X"],
      "business_explanation": "string"
    }
  ],
  "cross_platform_summary": {
    "X": {
      "tweet_volume": number,
      "engagement_velocity": number,
      "health_status": "string"
    }
  },
  "recommended_actions": [
    {
      "action_type": "RECOVERY|EXIT",
      "priority": "HIGH|MEDIUM|LOW",
      "description": "string",
      "expected_impact": "string",
      "timeframe": "string",
      "platforms_targeted": ["X"]
    }
  ],
  "confidence_in_analysis": 0.0-1.0
}
```

## Examples

### Declining Trend
```python
metrics = load_sample_data("declining")
result = analyzer.analyze(metrics)
# Status: DECLINING (72% probability)
# Severity: WARNING
# Top causes: Engagement Decay (85%), Content Saturation (72%), Creator Disengagement (65%)
```

### Growing Trend
```python
metrics = load_sample_data("growing")
result = analyzer.analyze(metrics)
# Status: GROWING (5% decline probability)
# Severity: STABLE
# Root causes: None (or minimal)
```

### Collapsed Trend
```python
metrics = load_sample_data("collapsed")
result = analyzer.analyze(metrics)
# Status: COLLAPSED (95% decline probability)
# Severity: COLLAPSED
# Top causes: Multiple critical issues detected
```

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/analyze` | POST | Analyze custom metrics |
| `/sample-analysis` | GET | Analyze sample data |
| `/batch-analyze` | POST | Analyze multiple trends |
| `/sample-metrics-schema` | GET | View example input |

## Metrics Guide

### tweet_volume
Number of tweets with hashtag/trend

### weekly_engagement_velocity
% change per week: -0.15 = 15% decline, 0.10 = 10% growth

### unique_content_ratio
0-1: How much content is novel (0.22 = 22% unique, high saturation)

### posts_per_day
Total posts per day (current vs previous period)

### reach_per_tweet
Average impressions per tweet

### impression_velocity
% change in daily impressions

### top_accounts_participation
How many top/verified accounts are posting (current vs previous)

### top_influencer_engagement
Total engagement from top accounts

### sentiment_score
-1 to 1: Negative sentiment (-0.08) = audience dislike

### days_since_peak
How long since trend peaked (relevance loss indicator)

## Files

- `trend_analyzer.py` - Core analysis engine
- `api.py` - FastAPI server
- `schemas.py` - Input/output data models
- `sample_data.py` - Test data
- `utils.py` - Helper functions
- `examples.py` - Usage examples

## Configuration

Adjust confidence threshold:
```python
analyzer = TrendAnalyzer(min_confidence_threshold=0.5)  # Only report >50% confidence
```

## Limitations

- Twitter/X data only (other platforms removed in v2.0)
- Stateless: No trend tracking across multiple analyses
- Requires at least 1 X metric to analyze

## Next Steps

1. Connect to live X API (v2)
2. Add time-series tracking
3. Implement webhook notifications
4. Add visualization dashboard

---

**Questions?** Check `README.md` for full documentation.
