# ⚙️ Backend - TrendPredict API

FastAPI-powered backend with ML-ready architecture for trend analysis and decline prediction.

## 📁 Structure

```
backend/
├── main.py                          # FastAPI application
├── config.py                        # Configuration & settings
├── requirements.txt                 # Python dependencies
│
├── shared/
│   ├── __init__.py
│   └── utils.py                    # Common utilities
│
└── trend_analysis/
    ├── __init__.py
    ├── router.py                   # API endpoints
    ├── service.py                  # Business logic
    ├── schema.py                   # Pydantic models
    │
    └── ml/
        ├── __init__.py
        ├── feature_engineering.py  # Feature extraction
        ├── decline_model.py        # ML predictions
        ├── explainability.py       # SHAP/XAI
        └── simulation.py           # What-if analysis
```

## 🚀 Setup

### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Server
```bash
# Development (with auto-reload)
python main.py

# Production (with uvicorn)
uvicorn main:app --host 0.0.0.0 --port 8000
```

Server runs on: `http://localhost:8000`

## 📋 API Documentation

### Interactive Docs
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Health Check
```bash
curl http://localhost:8000/health
```

## 🔌 API Endpoints

### Trends

#### `GET /api/trends`
Get list of trends with filters
```python
# Query parameters
{
  "platforms": ["twitter", "instagram"],  # Optional
  "status": "growing",                    # Optional
  "limit": 20                            # Default: 20
}
```

#### `GET /api/trends/{trend_id}`
Get detailed trend information
```python
Response: TrendDetails {
  id, name, description, platforms, status,
  engagement_history, sentiment_history,
  top_hashtags, top_influencers,
  geographic_spread
}
```

#### `POST /api/trends/predict/decline`
Predict decline probability
```python
# Query parameter: trend_id
Response: DeclinePrediction {
  trend_id,
  decline_probability: 0.72,
  is_declining: true,
  days_until_decline: 12,
  confidence_level: "high"
}
```

#### `GET /api/trends/explain/{trend_id}`
Get XAI explanation
```python
Response: ExplanationResponse {
  summary,
  detailed_explanation,
  feature_attributions: [
    {feature: "Audience Saturation", impact: 0.28, ...}
  ],
  counterfactuals,
  recommendations
}
```

#### `POST /api/trends/simulate`
Simulate interventions
```python
Request: SimulationRequest {
  trend_id: "trend_1",
  interventions: {
    "add_influencers": 5,
    "increase_content_novelty": 0.2
  },
  forecast_days: 30
}

Response: SimulationResponse {
  baseline: {...},
  with_intervention: {...},
  impact: {health_improvement, engagement_lift, ...},
  roi_prediction: {...}
}
```

## 🧠 ML Modules

### Feature Engineering (`ml/feature_engineering.py`)

**Purpose**: Extract ML-ready features from raw data

**Key Features**:
- `engagement_rate`: User interaction percentage
- `sentiment_score`: Positive sentiment ratio
- `content_diversity`: Shannon entropy of content
- `audience_saturation`: Target audience penetration
- `novelty_score`: Content originality
- `influencer_penetration`: Influencer-driven traffic %

**Future Integration**:
```python
# Connect to social APIs
from twitter_api import get_trend_data
from nlp_model import analyze_sentiment

# Real feature extraction
features = engineer.extract_features(
    raw_data=get_trend_data(trend_id),
    sentiment=analyze_sentiment(posts)
)
```

### Decline Model (`ml/decline_model.py`)

**Current**: Mock predictions with realistic distributions

**Production Roadmap**:
```python
# Train XGBoost model
import xgboost as xgb

model = xgb.XGBClassifier(
    max_depth=6,
    learning_rate=0.1,
    n_estimators=100
)

model.fit(X_train, y_train)

# Save model
import joblib
joblib.dump(model, 'models/decline_classifier.pkl')

# Load and predict
model = joblib.load('models/decline_classifier.pkl')
prediction = model.predict_proba(features)[0][1]
```

### Explainability (`ml/explainability.py`)

**XAI Methods**:
- **SHAP Values**: Feature attribution
- **Counterfactuals**: What-if scenarios
- **Natural Language**: GPT-powered explanations

**Production Integration**:
```python
import shap

# Generate SHAP values
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(features)

# Visualize
shap.summary_plot(shap_values, features)
```

### Simulation (`ml/simulation.py`)

**Intervention Types**:
1. **add_influencers**: Bring in N influencers
2. **increase_content_novelty**: Boost novelty by %
3. **expand_platforms**: Launch on new platforms
4. **boost_engagement**: Increase ad spend

**Causal Inference** (Future):
```python
from dowhy import CausalModel

# Define causal graph
model = CausalModel(
    data=historical_data,
    treatment='add_influencers',
    outcome='health_score',
    common_causes=['sentiment', 'saturation']
)

# Estimate causal effect
causal_estimate = model.estimate_effect()
```

## 🗄️ Data Models

### Pydantic Schemas (`schema.py`)

**Benefits**:
- Automatic validation
- Type safety
- API documentation generation
- JSON serialization

**Example**:
```python
class TrendOverview(BaseModel):
    id: str
    name: str
    platforms: List[PlatformType]
    status: TrendStatus
    metrics: TrendMetrics
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "trend_1",
                "name": "#AIRevolution2026",
                "platforms": ["twitter", "instagram"],
                "status": "peak"
            }
        }
```

## ⚙️ Configuration

### Environment Variables
Create `.env` file:
```bash
# Server
HOST=0.0.0.0
PORT=8000
DEBUG=true

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# Database (future)
DATABASE_URL=postgresql://user:pass@localhost/trends

# APIs (future)
TWITTER_API_KEY=your_key
OPENAI_API_KEY=your_key
```

### Settings (`config.py`)
```python
from config import settings

# Access settings
settings.HOST         # "0.0.0.0"
settings.PORT         # 8000
settings.DEBUG        # True
settings.ALLOWED_ORIGINS  # List of origins
```

## 🧪 Testing

### Run Tests
```bash
pytest tests/ -v
```

### Test Coverage
```bash
pytest --cov=trend_analysis tests/
```

### Example Test
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_trends():
    response = client.get("/api/trends")
    assert response.status_code == 200
    assert "trends" in response.json()
```

## 📊 Database Integration

### Current: Mock Data in Memory

### Future: PostgreSQL + SQLAlchemy

```python
# models.py
from sqlalchemy import Column, String, Float, DateTime
from database import Base

class Trend(Base):
    __tablename__ = "trends"
    
    id = Column(String, primary_key=True)
    name = Column(String, index=True)
    health_score = Column(Float)
    created_at = Column(DateTime)
```

## 🔒 Security

### CORS Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Authentication (Future)
```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

@router.get("/trends")
async def get_trends(credentials = Depends(security)):
    # Verify JWT token
    pass
```

## 🚀 Deployment

### Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Railway/Render
```bash
# Install Railway CLI
npm i -g railway

# Deploy
railway up
```

## 📈 Performance

### Optimization Tips
1. **Caching**: Use Redis for frequently accessed data
2. **Database Indexing**: Index on `id`, `status`, `created_at`
3. **Async Operations**: Use `async def` for I/O operations
4. **Background Tasks**: Offload ML inference to Celery

### Monitoring
```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

## 🐛 Debugging

### Enable Debug Logs
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Profile Performance
```python
from fastapi import Request
import time

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    response.headers["X-Process-Time"] = str(duration)
    return response
```

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [XGBoost](https://xgboost.readthedocs.io/)
- [SHAP](https://shap.readthedocs.io/)

---

Built for scalability | ML-ready | Production-grade
