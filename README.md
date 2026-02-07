# Creative Recovery & Growth Agent 🎬

A sophisticated AI-powered agent that converts trend intelligence into actionable social media content strategies. Powered by **Groq API** for fast, intelligent analysis and **PyTrends** for real-time trend data.

## Overview

This system helps creators and marketers respond strategically to social media trends by generating high-performing content ideas, hooks, captions, and remix formats.

### Two Operating Modes

| Mode | Alert Levels | Purpose |
|------|--------------|---------|
| **COMEBACK MODE** | 🔴 Red, 🟠 Orange | Revive declining trends with fresh angles |
| **GROWTH MODE** | 🟢 Green, 🟡 Yellow | Accelerate growth on rising trends |

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│         Trend Intelligence (Upstream System)             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ CreativeRecoveryAgent │
         └────────┬──────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
  ┌──────────────┐   ┌─────────────────────┐
  │  Groq API    │   │  TrendsAnalyzer     │
  │ (Content Gen)│   │  (PyTrends + Groq)  │
  └──────────────┘   └─────────────────────┘
        │                   │
        └─────────┬─────────┘
                  │
                  ▼
    ┌─────────────────────────────┐
    │   Structured JSON Output    │
    │  - 3 Reel Ideas             │
    │  - 3 Captions/Hooks         │
    │  - 2 Remix Formats          │
    └─────────────────────────────┘
```

## Components

### 1. **groq_integration.py**
- `GroqContentGenerator` class
- Generates creative content using Groq API (llama-3.3-70b-versatile)
- Supports COMEBACK MODE and GROWTH MODE
- Returns structured JSON with:
  - 3 reel video ideas
  - 3 engaging captions/hooks (English + Hinglish)
  - 2 remix formats

### 2. **trends_integration.py**
- `TrendsAnalyzer` class
- Fetches live data from Google Trends via PyTrends
- Groq-enhanced analysis:
  - Trend momentum assessment
  - Audience sentiment analysis
  - Best content angles
  - Creator niche identification
  - Virality potential scoring
- Intelligent hashtag categorization (viral/niche/reach)

### 3. **agent.py**
- `CreativeRecoveryAgent` main class
- Orchestrates the entire pipeline
- Accepts trend alerts with alert levels
- Routes to appropriate mode (COMEBACK/GROWTH)
- Generates comprehensive reports

## Installation

```bash
# Clone or navigate to project
cd comeback

# Create virtual environment
python -m venv venv

# Activate venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Create `.env` file with your Groq API key:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Usage

### Basic Example

```python
from agent import CreativeRecoveryAgent

agent = CreativeRecoveryAgent()

# Process a trend alert
result = agent.process_trend_alert(
    trend_name="Dance Challenge Format",
    alert_level="red",  # Declining trend
    context={
        "decline_drivers": [
            "Over-saturation",
            "Audience fatigue",
            "Algorithm changes"
        ]
    }
)

# Get actionable content
print(result['content']['reels'])      # 3 video ideas
print(result['content']['captions'])   # 3 hooks/captions
print(result['content']['remixes'])    # 2 format ideas
```

### Advanced: Trend Analysis with Intelligence

```python
from trends_integration import TrendsAnalyzer

analyzer = TrendsAnalyzer(groq_api_key="your_key")

# Get Groq-enhanced trend analysis
analysis = analyzer.analyze_trend("AI Meme")
print(analysis['groq_insights'])  # Trend momentum, sentiment, etc.

# Get intelligent hashtag categories
hashtags = analyzer.generate_hashtags_with_groq("AI Meme")
print(hashtags['categorized_hashtags'])
```

### Run Full Demo

```bash
python demo.py
```

## Output Structure

### COMEBACK MODE (Red/Orange Alert)

```json
{
  "trend_name": "Dance Challenge Format",
  "alert_level": "red",
  "mode": "COMEBACK MODE",
  "decline_drivers": ["Over-saturation", "Audience fatigue"],
  "content_strategy": "Revive interest with fresh angles",
  "content": {
    "reels": [
      {
        "id": 1,
        "title": "Unconventional Dance Challenge",
        "description": "...",
        "hook": "Get ready to groove to the most unexpected dance fusion!",
        "why_it_works": "By mixing styles, we're reducing over-saturation..."
      }
    ],
    "captions": [
      {
        "id": 1,
        "caption": "Kya hai yeh naya dance craze?",
        "language": "Hinglish"
      }
    ],
    "remixes": [
      {
        "id": 1,
        "format": "Mashup",
        "structure": "Combine two or more popular songs...",
        "example": "Mashup of 'Senorita' and 'Old Town Road'..."
      }
    ]
  }
}
```

### GROWTH MODE (Green/Yellow Alert)

Similar structure but optimized for:
- Scaling reach
- Increasing engagement
- Capturing emerging audiences
- Cross-platform virality

## Key Features

✅ **Dual Operating Modes**
- COMEBACK MODE for declining trends
- GROWTH MODE for rising trends

✅ **Multi-Language Support**
- English (primary)
- Hinglish (Roman Hindi + English mix)

✅ **Real-Time Trend Data**
- Google Trends integration via PyTrends
- Live related queries and topics
- Trending hashtag extraction

✅ **AI-Powered Intelligence**
- Groq API for instant analysis
- Trend momentum detection
- Sentiment analysis
- Virality scoring
- Creator niche identification

✅ **Structured Output**
- Always 3 reel ideas
- Always 3 captions/hooks
- Always 2 remix formats
- JSON format for easy integration

✅ **Creator-Focused**
- Realistic, implementable ideas
- Audience psychology insights
- Combat specific decline drivers
- Growth acceleration strategies

## Alert Levels

```
🔴 RED      → COMEBACK MODE (Critical decline)
🟠 ORANGE   → COMEBACK MODE (Moderate decline)
🟡 YELLOW   → GROWTH MODE (Emerging opportunity)
🟢 GREEN    → GROWTH MODE (Strong growth)
```

## API Models Used

- **Groq**: `llama-3.3-70b-versatile` (Fast, intelligent LLM)
- **Trends**: Google Trends (via PyTrends)

## Example Scenarios

### Scenario 1: Dance Challenge Decline (Red Alert)
```python
agent.process_trend_alert(
    trend_name="Dance Challenge Format",
    alert_level="red",
    context={"decline_drivers": ["Over-saturation", "Algorithm changes"]}
)
# Returns 3 fresh dance reel ideas that combat fatigue
```

### Scenario 2: AI Meme Growth (Green Alert)
```python
agent.process_trend_alert(
    trend_name="AI Meme",
    alert_level="green",
    context={"growth_opportunities": ["Gen Z audience", "Cross-platform", "Meme culture"]}
)
# Returns 3 scaling strategies to capitalize on growth
```

### Scenario 3: Batch Processing
```python
trends = [
    {"name": "Skincare Videos", "alert": "orange"},
    {"name": "AI Art", "alert": "green"},
    {"name": "Workout Challenge", "alert": "red"}
]

for trend in trends:
    result = agent.process_trend_alert(trend['name'], trend['alert'])
```

## Dependencies

```
groq==1.0.0              # Groq API client
pytrends==4.9.2          # Google Trends scraper
python-dotenv==1.0.0     # Environment variables
requests==2.31.0         # HTTP requests
pandas>=0.25             # Data processing (via pytrends)
numpy>=1.22.4            # Numerical computing (via pytrends)
```

## Production Integration

### Webhook Handler Example

```python
from flask import Flask, request
from agent import CreativeRecoveryAgent

app = Flask(__name__)
agent = CreativeRecoveryAgent()

@app.route('/webhook/trend-alert', methods=['POST'])
def handle_trend_alert():
    """Receive trend alerts from upstream system"""
    data = request.json
    
    result = agent.process_trend_alert(
        trend_name=data['trend_name'],
        alert_level=data['alert_level'],
        context=data.get('context', {})
    )
    
    # Send to content posting system
    return {"status": "processed", "content_id": result['trend_name']}
```

## Performance

- **Groq Response Time**: ~1-3 seconds per request
- **PyTrends Fetch**: ~2-5 seconds per keyword
- **Total Pipeline**: ~5-8 seconds for full analysis

## Troubleshooting

### Groq API Errors
- Check `GROQ_API_KEY` in `.env`
- Verify API key has required credits
- Model availability: Use `llama-3.3-70b-versatile`

### PyTrends Issues
- Rate limiting: Add delays between requests
- Network: Ensure internet connectivity
- Fallback: Use provided dummy data if offline

### JSON Parsing Errors
- Check Groq response format
- Groq may occasionally return non-JSON - retry
- Implement retry logic with exponential backoff

## Future Enhancements

- [ ] Cache trending data for faster retrieval
- [ ] Multi-language support (Spanish, French, etc.)
- [ ] Video script generation from reels
- [ ] Thumbnail design recommendations
- [ ] Cross-platform optimization (TikTok, YouTube, Instagram)
- [ ] A/B testing framework for caption variants
- [ ] Real-time trend monitoring dashboard
- [ ] Creator performance metrics integration

## License

This project is proprietary. All rights reserved.

---

**Built with** ❤️ for creators, marketers, and growth enthusiasts.

**Powered by** 🚀 Groq AI + PyTrends Intelligence
