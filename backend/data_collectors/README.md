# Data Collectors Module

## 🎯 Overview

Centralized data collection from social media platforms (Reddit, Twitter, Google Trends) for trend analysis.

## 📁 Structure

```
backend/data_collectors/
├── __init__.py
└── reddit_collector.py    # Reddit API integration
```

## 🔌 Reddit Collector

### Endpoint

**POST /api/data/reddit/search**

Collect Reddit posts and comments for a trend keyword.

### Request

```json
{
  "keyword": "Grimace Shake",
  "days_back": 30,
  "post_limit": 100,
  "fetch_comments": true,
  "subreddits": null
}
```

### Response

```json
{
  "success": true,
  "keyword": "Grimace Shake",
  "summary": {
    "total_posts": 87,
    "total_comments": 1234,
    "date_range": "Last 30 days",
    "top_subreddits": [
      {"name": "memes", "post_count": 23},
      {"name": "funny", "post_count": 18}
    ],
    "avg_score": 145.2,
    "avg_comments_per_post": 14.2
  },
  "posts": [...]
}
```

### Features

✅ **Search Scope**
- All of Reddit (r/all)
- Specific subreddits (optional)

✅ **Data Collected**
- Post title, text, metadata
- Scores, upvote ratios
- Comment counts
- Timestamps (UTC + formatted)
- Top comments (configurable limit)

✅ **Analysis Ready**
- Daily aggregations
- Engagement metrics
- Subreddit distributions
- Time-series data

### Integration with Lifecycle Module

The Reddit collector is automatically used by the lifecycle detection module:

```python
# In lifecycle/feature_engineering.py
reddit_signals = await extract_reddit_signals(trend_name)
# Uses PRAW client to fetch Reddit data
```

## 🚀 Quick Start

### 1. Environment Setup

```bash
# .env file
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password
REDDIT_USER_AGENT=TrendLens/1.0
```

### 2. Test Endpoint

```bash
curl -X POST http://localhost:8000/api/data/reddit/search \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "Grimace Shake",
    "days_back": 30,
    "post_limit": 100,
    "fetch_comments": true
  }'
```

### 3. Health Check

```bash
curl http://localhost:8000/api/data/reddit/health
```

## 📊 Use Cases

### 1. Standalone Data Collection
Use the API endpoint directly to collect Reddit data for any keyword.

### 2. Lifecycle Analysis Integration
Automatically called by the lifecycle detection module to extract Reddit signals.

### 3. Trend Research
Explore trends by analyzing top subreddits, engagement patterns, and discussion growth.

## 🔧 Configuration

### Post Limits
```python
DEFAULT_DAYS_BACK = 30
DEFAULT_POST_LIMIT = 100  # Max posts per request
TOP_COMMENTS_LIMIT = 50   # Top comments per post
```

### Time Filters
- `week` - Last 7 days
- `month` - Last 30 days
- `year` - Last 365 days

## 🛡️ Error Handling

- **Authentication Failed**: Check Reddit credentials
- **Rate Limit**: PRAW handles rate limiting automatically
- **No Results**: Returns empty arrays with success=true

## 📈 Response Optimization

- **Text Truncation**: Post text limited to 500 chars, comments to 300 chars
- **Comment Filtering**: Only top N comments by score
- **Metadata Only**: Full text available but can be disabled

## 🔗 Frontend Integration

Use the search page to trigger data collection:

1. User enters trend keyword
2. Frontend calls `/api/trend/lifecycle`
3. Backend calls Reddit collector internally
4. Results displayed in UI

## 📝 Example Usage

### Python (Requests)

```python
import requests

response = requests.post(
    "http://localhost:8000/api/data/reddit/search",
    json={
        "keyword": "Grimace Shake",
        "days_back": 30,
        "post_limit": 100,
        "fetch_comments": True
    }
)

data = response.json()
print(f"Collected {data['summary']['total_posts']} posts")
```

### JavaScript (Fetch)

```javascript
const response = await fetch('http://localhost:8000/api/data/reddit/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    keyword: 'Grimace Shake',
    days_back: 30,
    post_limit: 100,
    fetch_comments: true
  })
});

const data = await response.json();
console.log(`Collected ${data.summary.total_posts} posts`);
```

## 🎯 Future Enhancements

- [ ] Twitter/X collector
- [ ] Google Trends collector (already in lifecycle module)
- [ ] Sentiment analysis integration
- [ ] Real-time streaming
- [ ] Data caching with Redis
- [ ] Batch processing for multiple keywords

---

**Built for Datathon 2026** | Production-ready | Real Reddit API Integration ✅
