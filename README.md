# Early Decline Signal Detection Engine
## Feature #2 - Hackathon Implementation

**Status**: ✅ Production-Ready | **Response**: <200ms | **Architecture**: Deterministic & Explainable

---

## 🎯 What This Does

Detects **early warning signs** that a trend is about to decline — before volume crashes.

Answers: **"Is this trend starting to die — and why?"**

---

## 🧩 4 Independent Signals

Each signal = 0-100 score. All explainable, no ML black-boxes.

| Signal | What It Detects | Why It Matters |
|--------|-----------------|----------------|
| **#1: Engagement Drop** | Volume drops 10-40% | Audience fatigue |
| **#2: Velocity Decline** | Growth slowing (deceleration) | **EARLIEST indicator** |
| **#3: Creator Decline** | Creators abandoning trend | They leave before audiences |
| **#4: Quality Decline** | Posts become spammy/low-effort | Predicts long-term death |

**Output**: Weighted average → **Decline Risk Score (0-100)**

---

## 📥 Input Format

From Feature #1 (or fallback):
```json
{
  "trend_id": "12345",
  "trend_name": "Grimace Shake",
  "lifecycle_stage": 2,        // 1=Emergence, 2=Viral, 3=Plateau, 4=Decline, 5=Death
  "stage_name": "Viral Explosion",
  "days_in_stage": 5,
  "confidence": 0.85
}
```

From database (daily metrics):
```json
[
  {
    "date": "2026-02-07",
    "total_engagement": 5000,
    "views": 50000,
    "posts_count": 100,
    "creators_count": 50,
    "avg_creator_followers": 10000,
    "avg_comments_per_post": 15,
    "avg_engagement_per_post": 50
  },
  ...
]
```

---

## 📤 Output Format

```json
{
  "trend_id": "12345",
  "decline_risk_score": 67.5,          // 0-100
  "alert_level": "orange",             // green/yellow/orange/red
  "signal_breakdown": {
    "engagement_drop": 72,
    "velocity_decline": 65,
    "creator_decline": 58,
    "quality_decline": 45
  },
  "timestamp": "2026-02-07T14:30:00Z",
  "confidence": "high",                // high/medium/low
  "data_quality": "complete"           // complete/degraded
}
```

---

## 🚀 Quick Start

### 1. Install
```bash
pip install -r requirements.txt
```

### 2. Configure
```bash
cp .env.example .env
# Edit .env with your MongoDB Atlas connection string
```

### 3. Run
```bash
python -m uvicorn decline_signals.main:app --reload --port 8000
```

Swagger docs: http://localhost:8000/docs

---

## 🔄 How Lifecycle Awareness Works

**Same metric means different things at different stages:**

| Metric | Emergence | Viral | Plateau | Decline |
|--------|-----------|-------|---------|---------|
| 20% engagement drop | ✓ Normal | 🚨 ALARMING | ⚠️ Concern | Expected |
| 50 new creators | ⚠️ Okay | ⚠️ Slowing | Normal | Concerning |

**Sensitivity Levels**:
- **Viral stage**: Very high sensitivity (10%+ drop = 100 points)
- **Plateau stage**: Medium sensitivity (15%+ drop = 75 points)
- **Emergence stage**: Low sensitivity (40%+ drop = 20 points)

All thresholds in `config.py` - **no code changes needed** to tune.

---

## 🛡️ Feature #1 Fallback (Critical!)

**Problem**: If Feature #1 API is down, original code returns lifecycle_stage=0 → downstream thinks trend is "everlasting"

**Solution (Option B)**: 
- If Feature #1 fails → assume stage 3 (Plateau)
- Compute signals normally with medium sensitivity
- Return `data_quality: "degraded"` so downstream knows to be cautious
- **System keeps working even if Feature #1 is down**

```python
if lifecycle_info is None:
    lifecycle_stage = 3        # Plateau
    data_quality = "degraded"  # Tell downstream
```

---

## 📊 API Endpoints

### Detect Decline Signals (PRIMARY)
```http
POST /api/trends/{trend_id}/decline-signals
Content-Type: application/json

{
  "trend_id": "grimace_shake",
  "trend_name": "Grimace Shake",
  "lifecycle_info": {...},           // May be null if Feature #1 down
  "daily_metrics": [...]
}
```

**Response**: `DeclineSignalResponse` (see above)

### Get Signal History
```http
GET /api/trends/{trend_id}/decline-signals/history?limit=30
```

### Get Latest Signal
```http
GET /api/trends/{trend_id}/decline-signals/latest
```

### Health Check
```http
GET /health
```

---

## 🧪 Testing

### With curl (declining trend)
```bash
curl -X POST http://localhost:8000/api/trends/test/decline-signals \
  -H "Content-Type: application/json" \
  -d '{
    "trend_id": "test",
    "trend_name": "Test Trend",
    "lifecycle_info": {
      "trend_id": "test",
      "trend_name": "Test Trend",
      "lifecycle_stage": 2,
      "stage_name": "Viral",
      "days_in_stage": 5,
      "confidence": 0.85
    },
    "daily_metrics": [...]
  }'
```

### With Python (mock data)
```python
from mock_data import generate_declining_trend

request = generate_declining_trend()
# Use request.dict() to send to API
```

### Interactive Testing
Open http://localhost:8000/docs and use Swagger UI

---

## 📁 Project Structure

```
decline_signals/
├── main.py              ← FastAPI app (start here)
├── config.py            ← Lifecycle-aware thresholds
├── models.py            ← Request/response schemas
├── database.py          ← MongoDB Atlas connection
├── lifecycle_handler.py  ← Fallback logic (Feature #1)
├── aggregator.py        ← Combine signals
├── utils.py             ← Helpers
└── signals/
    ├── engagement_drop.py    ← Signal 1
    ├── velocity_decline.py   ← Signal 2
    └── quality_decline.py    ← Signals 3 & 4
```

---

## 🔗 Integration Points

**Consumes**:
- Feature #1 API: Lifecycle classification (fallback to stage 3)
- MongoDB Atlas: Daily metrics for trends

**Provides**:
- Decline risk scores
- Signal breakdown
- Historical data
- Health endpoint

---

## 💡 Key Design Decisions

1. **Signals are independent** - Each testable in isolation
2. **Lifecycle-aware thresholds** - Config-driven, no code changes
3. **Graceful fallback** - Works when Feature #1 is down
4. **No ML** - Pure rule-based, 100% explainable
5. **Fast** - <200ms response time
6. **Single MongoDB document** - All trend data in one place

---

## ⚙️ Configuration

Edit `config.py` to adjust sensitivity:

```python
ENGAGEMENT_DROP_THRESHOLDS = {
    "very_high": {              # Viral stage
        "drop_percent": 10,     # Need 10%+ to trigger
        "max_score": 100,
    },
    ...
}

SIGNAL_WEIGHTS = {
    "velocity_decline": 0.35,   # Most important
    "engagement_drop": 0.3,
    "creator_decline": 0.25,
    "quality_decline": 0.1,
}
```

---

## 🚨 Alert Levels

- **GREEN (0-30)**: Healthy, no concerns
- **YELLOW (30-60)**: Watch, minor warning signs  
- **ORANGE (60-80)**: Significant decline risk
- **RED (80-100)**: Critical, action needed

---

## 📝 Example Responses

### Declining Trend (Alert: ORANGE)
```json
{
  "decline_risk_score": 72,
  "alert_level": "orange",
  "signal_breakdown": {
    "engagement_drop": 80,
    "velocity_decline": 75,
    "creator_decline": 60,
    "quality_decline": 55
  },
  "confidence": "high"
}
```

### Healthy Trend (Alert: GREEN)
```json
{
  "decline_risk_score": 15,
  "alert_level": "green",
  "signal_breakdown": {
    "engagement_drop": 0,
    "velocity_decline": 5,
    "creator_decline": 10,
    "quality_decline": 0
  },
  "confidence": "high"
}
```

### Feature #1 Down (Fallback Active)
```json
{
  "decline_risk_score": 45,
  "alert_level": "yellow",
  "confidence": "low",
  "data_quality": "degraded"  ← ⚠️ Tells downstream to be cautious
}
```

---

## 🚀 Ready for Judge Demo

✅ **Deterministic**: No randomness, same input = same output
✅ **Fast**: <200ms response
✅ **Explainable**: 4 interpretable signals
✅ **Robust**: Works without Feature #1
✅ **Business-Relevant**: Detects trend peaking before crash
✅ **Production-Grade**: Clean code, proper logging, error handling

---

## Notes

- MongoDB Atlas setup: Friend handles this
- Feature #1 integration: Automatic fallback to stage 3 if unavailable
- Other features: Can consume decline_risk_score from this API
