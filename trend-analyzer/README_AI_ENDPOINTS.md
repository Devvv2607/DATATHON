# Twitter Trend Intelligence Engine

A comprehensive Python system for analyzing Twitter/X trends, detecting decline causes, and generating AI-powered insights and strategic recommendations.

## 🎯 Overview

The Twitter Trend Intelligence Engine provides:

1. **Core Trend Analysis** - Detects 8 types of trend decline with confidence scoring
2. **AI-Powered Explanations** - Uses Featherless AI/DeepSeek to generate detailed insights
3. **Strategic Recommendations** - Generates recovery or exit strategies
4. **Executive Reporting** - Board-ready summaries and comprehensive reports
5. **Real Twitter API Integration** - Fetches live trending data via RapidAPI
6. **REST API Service** - FastAPI endpoints for all functionality

## 🏗️ Architecture

```
┌──────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ Twitter API  │────▶│ TrendAnalyzer    │────▶│ Explanation     │────▶ HTTP
│ (RapidAPI)   │     │ (8 detectors)    │     │ Engine (AI)     │     Response
└──────────────┘     └──────────────────┘     └─────────────────┘
     Raw Data         Analysis Results        LLM-Generated
                                            Explanations/Strategies
```

## 📦 Components

| File | Purpose |
|------|---------|
| `trend_analyzer.py` | Core analysis engine with 8 decline detectors |
| `explanation_engine.py` | AI-powered insights using Featherless AI |
| `twitter_api.py` | Twitter/X API client via RapidAPI |
| `config.py` | Configuration and credential management |
| `schemas.py` | Pydantic validation models |
| `api.py` | FastAPI REST service with 12+ endpoints |
| `sample_data.py` | Pre-loaded test data (3 scenarios) |
| `utils.py` | Helper functions |

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

Set environment variables:

```bash
export FEATHERLESS_API_KEY="your_api_key"
export TWITTER_API_KEY="your_api_key"
export APP_ENV="development"
```

Or create `.env` file:

```
FEATHERLESS_API_KEY=your_key_here
TWITTER_API_KEY=your_key_here
APP_ENV=development
```

### Start Server

```bash
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### Access API

- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Root**: http://localhost:8000/

## 📊 API Endpoints

### Analysis Endpoints (Fast, No AI)

| Method | Endpoint | Purpose | Speed |
|--------|----------|---------|-------|
| POST | `/analyze` | Analyze trend for decline | 100-200ms |
| GET | `/sample-analysis` | Test with sample data | 100-200ms |
| POST | `/batch-analyze` | Analyze multiple trends | ~100ms per trend |

### AI-Powered Endpoints

| Method | Endpoint | Purpose | Speed |
|--------|----------|---------|-------|
| POST | `/explain` | Detailed cause explanations | 2-5s |
| POST | `/strategy` | Recovery strategy | 3-8s |
| POST | `/executive-summary` | Executive summary | 2-4s |
| POST | `/full-report` | Complete report | 5-15s |

### Utility Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Health check |
| GET | `/sample-metrics-schema` | Schema documentation |
| GET | `/api-docs-markdown` | API docs |

## 💡 Usage Examples

### Example 1: Basic Analysis

```python
import requests

response = requests.post("http://localhost:8000/analyze", json={
    "trend_name": "#TechTok",
    "x": {
        "tweet_volume": {"current": 45000, "previous_period": 52000},
        "weekly_engagement_velocity": -0.15,
        "unique_content_ratio": 0.25
    }
})

result = response.json()
print(f"Status: {result['trend_status']}")
print(f"Decline Probability: {result['decline_probability']:.2%}")
```

### Example 2: Get AI Explanations

```python
response = requests.post("http://localhost:8000/explain", json={
    "trend_name": "#TechTok",
    "x": {
        "tweet_volume": {"current": 45000, "previous_period": 52000},
        "weekly_engagement_velocity": -0.15,
        "unique_content_ratio": 0.25
    }
})

result = response.json()
for cause_type, explanation in result['ai_explanations'].items():
    print(f"{cause_type}: {explanation}")
```

### Example 3: Generate Strategy

```python
response = requests.post("http://localhost:8000/strategy", json={
    "trend_name": "#CryptoRally",
    "x": {
        "tweet_volume": {"current": 12000, "previous_period": 85000},
        "weekly_engagement_velocity": -0.78,
        "unique_content_ratio": 0.05
    }
})

result = response.json()
print(f"Trend Status: {result['trend_status']}")
print(f"Recommended Strategy:\n{result['ai_strategy']}")
```

## 🔍 Decline Cause Types

The analyzer detects 8 types of trend decline:

1. **Engagement Decay** - Posts receive fewer interactions
2. **Content Saturation** - Too much repetitive content
3. **Creator Disengagement** - Original creators stop posting
4. **Influencer Dropoff** - High-follower accounts disengage
5. **Posting Frequency Collapse** - Overall volume drops sharply
6. **Algorithmic Visibility Reduction** - Algorithm suppresses content
7. **Audience Fatigue** - Audience tired of topic
8. **Temporal Relevance Loss** - Topic no longer timely

## 📈 Output Format

### Analysis Response

```json
{
  "trend_name": "#TechTok",
  "trend_status": "DECLINING",
  "decline_probability": 0.65,
  "severity_level": "WARNING",
  "root_causes": [
    {
      "cause_type": "Engagement Decay",
      "confidence": 0.75,
      "severity_contribution": 0.35,
      "evidence": ["engagement_velocity_decreased"],
      "affected_platforms": ["x"],
      "business_explanation": "..."
    }
  ],
  "cross_platform_summary": {...},
  "recommended_actions": [...],
  "confidence_in_analysis": 0.82
}
```

## 🧪 Testing

### Run Sample Analysis

```bash
curl "http://localhost:8000/sample-analysis?sample_type=declining"
```

### Run Examples

```bash
# Run all examples
python examples_ai_endpoints.py

# Run specific example
python examples_ai_endpoints.py 1  # Example 1
python examples_ai_endpoints.py 7  # Example 7
```

### Run Full Demo

```bash
python demo_all_features.py
```

## 📚 Documentation

- **[AI Integration Guide](AI_INTEGRATION_GUIDE.md)** - Detailed workflows and patterns
- **[Quick Reference](QUICK_REFERENCE.md)** - API endpoint reference
- **[Examples](examples_ai_endpoints.py)** - 10 comprehensive examples
- **[Full Demo](demo_all_features.py)** - Interactive demonstration

## 🔧 Configuration

### config.py

```python
from config import get_config

config = get_config()  # Auto-detects APP_ENV
print(config.TWITTER_API_KEY)
print(config.MIN_CONFIDENCE_THRESHOLD)
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FEATHERLESS_API_KEY` | AI API key | Required for AI features |
| `TWITTER_API_KEY` | Twitter API key | Required for live data |
| `TWITTER_API_HOST` | Twitter API host | api.twitter-api.io |
| `APP_ENV` | Environment | development |
| `MIN_CONFIDENCE_THRESHOLD` | Cause threshold | 0.3 |
| `LOG_LEVEL` | Logging level | INFO |

## 📊 Performance Metrics

| Operation | Speed | Use Case |
|-----------|-------|----------|
| /analyze | 100-200ms | Real-time monitoring |
| /explain | 2-5s | Detailed insights |
| /strategy | 3-8s | Decision support |
| /full-report | 5-15s | Comprehensive docs |

## 🛠️ Deployment

### Docker

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run with multiple workers
python -m uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4

# Or with Gunicorn
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app
```

## 🔐 Security

- API keys stored in environment variables (not in code)
- Input validation via Pydantic schemas
- CORS enabled for cross-origin requests
- Error handling prevents information leakage

## 🐛 Troubleshooting

### AI Service Unavailable (503)

1. Check `FEATHERLESS_API_KEY` is set correctly
2. Verify API key is valid at https://api.featherless.ai
3. Check network connectivity
4. Review logs for detailed errors

### Analysis Returns Low Confidence

1. Provide more X metrics (more data = better analysis)
2. Adjust `MIN_CONFIDENCE_THRESHOLD` in config.py
3. Review `/sample-analysis` for expected data format

### Twitter API Errors

1. Verify `TWITTER_API_KEY` is correct
2. Check RapidAPI subscription status
3. Monitor rate limits
4. Verify IP whitelist if applicable

## 📈 Scaling

### Quick Performance Improvement

```python
# Cache results for identical inputs
from functools import lru_cache

@lru_cache(maxsize=1000)
def analyze_cached(trend_name: str, metrics_hash: str):
    return analyzer.analyze(metrics_dict)
```

### Production Scaling

1. Run multiple API instances behind load balancer
2. Implement Redis caching for expensive operations
3. Use async task queue (Celery) for `/full-report`
4. Implement database for historical tracking
5. Add monitoring and alerting

## 🔮 Future Enhancements

- [ ] Trend prediction with ML
- [ ] Database integration (PostgreSQL)
- [ ] Historical trend tracking
- [ ] Visualization dashboard
- [ ] Webhook notifications
- [ ] Competitor analysis features
- [ ] Trend recommendation engine
- [ ] Mobile app for alerts
- [ ] Multi-user support with authentication
- [ ] Advanced reporting templates

## 📄 License

This project is part of the Twitter Trend Intelligence system.

## 🤝 Contributing

Contributions welcome! Areas for enhancement:

1. Additional decline detection algorithms
2. More AI prompt templates
3. Enhanced visualization
4. Performance optimizations
5. Additional platform integrations

## 📞 Support

For issues, questions, or suggestions:

1. Check documentation in [AI_INTEGRATION_GUIDE.md](AI_INTEGRATION_GUIDE.md)
2. Review [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for API details
3. Run [demo_all_features.py](demo_all_features.py) for full overview
4. Check logs in uvicorn output

---

**Built with:** Python • FastAPI • Pydantic • OpenAI • Featherless AI
