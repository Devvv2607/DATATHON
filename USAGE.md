# Brand Trend Revenue Intelligence Agent - Usage Guide

## Quick Start

1. **Activate virtual environment**:
   ```bash
   venv\Scripts\activate
   ```

2. **Run the application**:
   ```bash
   python -m src.main
   ```

3. **Enter your domain** when prompted (e.g., "clothing", "technology", "food")

## Example Output

The system will:
- Discover trending topics in your domain
- Analyze trend momentum
- Classify trends as growing, stable, or declining
- Provide actionable recommendations

### Growing Trend Example
```json
{
  "trend_classification": {
    "category": "growing",
    "growth_rate": 12.5
  },
  "recommendations": {
    "type": "growth",
    "actions": [
      {
        "title": "Scale campaigns",
        "expected_reach_increase": "20-30%",
        "expected_conversion_impact": "12-18% lift"
      }
    ],
    "budget_strategy": {
      "recommendation": "Increase budget by 25%",
      "scaling_percentage": "20-30%"
    }
  }
}
```

### Declining Trend Example
```json
{
  "trend_classification": {
    "category": "declining",
    "growth_rate": -15.2
  },
  "recommendations": {
    "type": "decline",
    "days_until_collapse": 45,
    "projected_marketing_burn": 2500.00,
    "recommendation": "EXIT",
    "alternative_trends": [
      {
        "keyword": "emerging technology trends",
        "growth_rate": 15.0
      }
    ]
  }
}
```

## Configuration

Edit `.env` to customize:
- `GROWTH_THRESHOLD`: Minimum growth rate for "growing" classification (default: 5.0%)
- `DECLINE_THRESHOLD`: Maximum growth rate for "declining" classification (default: -5.0%)
- `MIN_TRENDS_REQUIRED`: Minimum trends to discover (default: 3)

## Troubleshooting

**Error: GROQ_API_KEY not found**
- Make sure `.env` file exists with your GROQ API key
- Or set environment variable: `set GROQ_API_KEY=your_key_here`

**Error: No trends found**
- Try a different domain name
- Check your internet connection
- Google Trends may be rate limiting - wait a few minutes

**Slow response**
- First run may be slower as it fetches trend data
- GROQ API calls may take 5-10 seconds
- Fallback recommendations are used if GROQ times out

## Features

✅ Automatic trend discovery using Google Trends
✅ Growth slope calculation with linear regression
✅ Trend classification (growing/stable/declining)
✅ AI-powered recommendations via GROQ
✅ Structured JSON output
✅ Error handling and fallback strategies
✅ Terminal-based interface

## Next Steps

- Run with different domains to see various trend patterns
- Integrate JSON output into your marketing dashboard
- Use recommendations to guide budget allocation decisions
- Monitor trends over time to track changes
