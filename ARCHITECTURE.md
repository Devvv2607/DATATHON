# System Architecture & Implementation Guide

## 🏗️ System Overview

The Creative Recovery & Growth Agent is a sophisticated multi-component system that transforms trend intelligence into actionable social media content strategies.

```
UPSTREAM TREND INTELLIGENCE
         ↓
    ┌────────────────────────────────┐
    │  CreativeRecoveryAgent         │
    │  (Main Orchestrator)           │
    └──────┬──────────────┬──────────┘
           │              │
    ┌──────▼─────┐  ┌─────▼──────────────┐
    │  Groq API  │  │  TrendsAnalyzer    │
    │  Module    │  │  Module            │
    └────────────┘  └────────────────────┘
           │              │
           │         PyTrends ──→ Google Trends
           │              │
           │              ▼ (Groq Enhancement)
           │         Trend Insights
           │              │
           └──────┬───────┘
                  ▼
         JSON OUTPUT (3R+3C+2X)
                  ↓
    DOWNSTREAM SYSTEMS
    - Content Posting
    - Creator Dashboard
    - API Integrations
```

## 📦 File Structure

```
comeback/
├── .env                      # API keys & secrets
├── requirements.txt          # Python dependencies
├── README.md                 # Full documentation
│
├── agent.py                  # Main agent orchestrator
├── groq_integration.py       # Groq API wrapper
├── trends_integration.py     # PyTrends + Groq wrapper
│
├── quickstart.py             # 30-second example
├── demo.py                   # Full feature demonstration
└── venv/                     # Python virtual environment
```

## 🔧 Core Components

### 1. GroqContentGenerator (`groq_integration.py`)

**Purpose**: Generate creative content using Groq's LLM

**Key Methods**:
- `generate_comeback_content()` - Red/Orange alert content
- `generate_growth_content()` - Green/Yellow alert content

**Inputs**:
- trend_name (str)
- decline_drivers or growth_opportunities (List[str])
- related_topics (List[str])

**Output** (Structured JSON):
```json
{
  "reels": [3 video ideas],
  "captions": [3 hooks/captions],
  "remixes": [2 format ideas]
}
```

**Model Used**: `llama-3.3-70b-versatile`
- Fast inference (~1-3 seconds)
- Supports JSON constraints
- Multi-language support

### 2. TrendsAnalyzer (`trends_integration.py`)

**Purpose**: Fetch and enhance trend data with AI insights

**Key Methods**:
- `get_trending_hashtags()` - Extract trending hashtags
- `get_related_topics()` - Get related search queries
- `analyze_trend()` - Complete analysis pipeline
- `_groq_enhance_trends()` - AI-powered insights
- `generate_hashtags_with_groq()` - Smart hashtag categorization

**Data Flow**:
```
PyTrends Fetch → Raw Trend Data → Groq Enhancement → Insights
```

**Output**:
```json
{
  "keyword": "...",
  "hashtags": [...],
  "related_topics": [...],
  "groq_insights": {
    "trend_momentum": "rising|stable|declining",
    "audience_sentiment": "positive|mixed|negative",
    "virality_potential": "high|medium|low",
    "creator_niches": [...],
    "growth_forecast": "..."
  }
}
```

### 3. CreativeRecoveryAgent (`agent.py`)

**Purpose**: Orchestrate the entire content generation pipeline

**Key Methods**:
- `process_trend_alert()` - Main entry point
- `generate_report()` - Human-readable output

**Logic Flow**:
1. Validate alert_level (red/orange/yellow/green)
2. Determine mode (COMEBACK/GROWTH)
3. Fetch trend context from analyzer
4. Route to appropriate content generator
5. Return structured JSON + report

**Mode Selection**:
```python
if alert_level in ["red", "orange"]:
    mode = COMEBACK_MODE
    strategy = "Revive interest with fresh angles"
else:  # green, yellow
    mode = GROWTH_MODE
    strategy = "Accelerate growth with reach expansion"
```

## 🎯 Operating Modes

### COMEBACK MODE (Red 🔴 / Orange 🟠)

**Triggered When**: Trend is declining, saturated, or losing momentum

**Strategy Focus**:
- Combat audience fatigue
- Break through saturation
- Overcome algorithm deprioritization
- Re-engage existing audience

**Content Characteristics**:
- Fresh angles on declining trends
- Unconventional approaches
- Emotional/storytelling elements
- Anti-boring hooks
- Format innovations

**Example**:
```
Trend: Dance Challenges (declining)
Alert: RED
Content: Mix ballet + hip-hop fusion, storytelling angle, reverse challenges
Why: Reduces fatigue, adds freshness, reignites interest
```

### GROWTH MODE (Yellow 🟡 / Green 🟢)

**Triggered When**: Trend is rising, emerging, or underexploited

**Strategy Focus**:
- Maximize reach potential
- Capture emerging audiences
- Cross-platform virality
- Early-mover advantage

**Content Characteristics**:
- Aggressive scaling tactics
- Community engagement loops
- UGC (User Generated Content) formats
- Niche audience expansion
- Influencer collaboration angles

**Example**:
```
Trend: AI Memes (rising)
Alert: GREEN
Content: AI meme mashups, challenges, before-after comparisons
Why: Captures Gen Z, cross-platform appeal, participatory elements
```

## 📊 Output Structure

### JSON Schema (Always Consistent)

```json
{
  "trend_name": "string",
  "alert_level": "red|orange|yellow|green",
  "mode": "COMEBACK MODE|GROWTH MODE",
  "generated_at": "YYYY-MM-DD",
  "decline_drivers|growth_opportunities": ["string"],
  "content_strategy": "string",
  "content": {
    "reels": [
      {
        "id": 1,
        "title": "string",
        "description": "string",
        "hook": "string",
        "why_it_works": "string"
      }
    ],
    "captions": [
      {
        "id": 1,
        "caption": "string",
        "language": "english|Hinglish"
      }
    ],
    "remixes": [
      {
        "id": 1,
        "format": "string",
        "structure": "string",
        "example": "string"
      }
    ]
  }
}
```

**Invariants**:
- Always 3 reels
- Always 3 captions
- Always 2 remixes
- Valid JSON format
- No markdown artifacts

## 🔄 Processing Pipeline

### Step 1: Trend Alert Reception
```python
alert = {
    "trend_name": "AI Meme",
    "alert_level": "green",
    "context": { ... }
}
```

### Step 2: Validation & Mode Determination
```python
if alert_level not in ["red", "orange", "yellow", "green"]:
    raise ValueError(...)

is_comeback = alert_level in ["red", "orange"]
```

### Step 3: Trend Context Fetching
```python
trend_analysis = trends_analyzer.analyze_trend(trend_name)
related_topics = trend_analysis.get("related_topics", [])
```

### Step 4: Content Generation via Groq
```python
if is_comeback_mode:
    content = groq_gen.generate_comeback_content(
        trend_name, decline_drivers, related_topics
    )
else:
    content = groq_gen.generate_growth_content(
        trend_name, growth_opportunities, related_topics
    )
```

### Step 5: Report Assembly
```python
result = {
    "trend_name": ...,
    "mode": "COMEBACK MODE" if is_comeback else "GROWTH MODE",
    "content": content,
    "content_strategy": ...,
    ...
}
```

### Step 6: Output & Delivery
```json
{
  "trend_name": "...",
  "content": {
    "reels": [...],      # 3 video ideas
    "captions": [...],   # 3 hooks
    "remixes": [...]     # 2 formats
  }
}
```

## 🌍 Multi-Language Support

### English (Primary)
- Business-focused hooks
- Technical explanations
- Platform-agnostic content

### Hinglish (Secondary)
- Mix of Roman Hindi + English
- Culturally relatable
- Youth-focused tone
- Example: "Kya bolte ho? Content is king!"

**Implementation**:
```python
captions = [
    {"caption": "...", "language": "english"},
    {"caption": "...", "language": "Hinglish"},
    {"caption": "...", "language": "english"}  # or Hinglish
]
```

## 🚀 Integration Points

### Webhook Integration (Flask Example)
```python
@app.route('/api/trends/alert', methods=['POST'])
def handle_trend_alert():
    data = request.json
    result = agent.process_trend_alert(
        trend_name=data['trend_name'],
        alert_level=data['alert_level']
    )
    return jsonify(result)
```

### Database Integration
```python
# Save generated content
db.content.insert_one({
    "trend_id": trend_id,
    "generated_content": result['content'],
    "timestamp": datetime.now()
})
```

### Queue Integration (Celery)
```python
@celery_app.task
def generate_content_async(trend_name, alert_level):
    result = agent.process_trend_alert(trend_name, alert_level)
    # Push to downstream system
    return result
```

## ⚙️ Configuration

### Environment Variables (.env)
```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Python Version
- Tested on: Python 3.10+
- Required: Python 3.8+

### Performance Tuning
```python
# Temperature (creativity vs consistency)
temperature = 0.8  # Higher = more creative

# Max tokens (response length)
max_tokens = 2000  # Adjust based on needs

# Rate limiting
time.sleep(1)  # Between requests
```

## 🛡️ Error Handling

### Groq API Errors
```python
try:
    response = groq_client.chat.completions.create(...)
except groq.BadRequestError as e:
    # Model decommissioned, use fallback
    return {"error": str(e)}
except groq.RateLimitError:
    # Implement exponential backoff
    time.sleep(2 ** retry_count)
```

### PyTrends Errors
```python
try:
    trends = pytrends.related_queries()
except Exception as e:
    # Fallback to dummy data
    return ["#dummy_trend"]
```

### JSON Parsing
```python
try:
    parsed = json.loads(response_text)
except json.JSONDecodeError:
    # Groq sometimes returns non-JSON, retry
    return retry_generate_content()
```

## 📈 Performance Metrics

| Component | Time | Notes |
|-----------|------|-------|
| Groq Content Generation | 1-3s | Depends on API load |
| PyTrends Fetch | 2-5s | Network dependent |
| Trend Groq Enhancement | 1-2s | Parallel possible |
| Total Pipeline | 5-8s | Can be optimized |

## 🔄 Batch Processing

```python
trends = [
    {"name": "Trend1", "alert": "red"},
    {"name": "Trend2", "alert": "green"},
    {"name": "Trend3", "alert": "orange"}
]

results = []
for trend in trends:
    result = agent.process_trend_alert(trend['name'], trend['alert'])
    results.append(result)
    
    # Rate limit: 1 request/second
    time.sleep(1)
```

## 🧪 Testing

### Unit Test Example
```python
def test_comeback_mode():
    result = agent.process_trend_alert(
        trend_name="Test Trend",
        alert_level="red"
    )
    
    assert result['mode'] == "COMEBACK MODE"
    assert len(result['content']['reels']) == 3
    assert len(result['content']['captions']) == 3
    assert len(result['content']['remixes']) == 2
```

## 📚 API Reference

### agent.process_trend_alert()
```python
result = agent.process_trend_alert(
    trend_name: str,           # Required: Trend name
    alert_level: str,          # Required: "red"|"orange"|"yellow"|"green"
    context: Dict = None       # Optional: Additional context
) -> Dict[str, Any]
```

### trends_analyzer.analyze_trend()
```python
analysis = analyzer.analyze_trend(
    keyword: str               # Trend keyword
) -> Dict[str, Any]           # With groq_insights
```

### trends_analyzer.generate_hashtags_with_groq()
```python
hashtags = analyzer.generate_hashtags_with_groq(
    keyword: str               # Trend keyword
) -> Dict[str, Any]           # With categorized hashtags
```

## 🎓 Usage Examples

### Minimal Example (3 lines)
```python
from agent import CreativeRecoveryAgent
agent = CreativeRecoveryAgent()
result = agent.process_trend_alert("Dance Challenges", "red")
```

### Full Example (with context)
```python
result = agent.process_trend_alert(
    trend_name="AI Art Trends",
    alert_level="green",
    context={
        "growth_opportunities": ["Gen Z", "Art education", "Monetization"]
    }
)
print(result['content']['reels'][0]['hook'])
```

### Batch Example
```python
trends = [
    ("Trend1", "red"),
    ("Trend2", "green"),
    ("Trend3", "yellow")
]

for name, level in trends:
    result = agent.process_trend_alert(name, level)
    print(f"Generated {len(result['content']['reels'])} ideas for {name}")
```

---

**System Version**: 1.0.0
**Last Updated**: 2026-02-07
**Python Version**: 3.10+
**API**: Groq llama-3.3-70b-versatile
