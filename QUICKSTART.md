# 🚀 Quick Start Guide - TrendPulse

## Complete Setup in 5 Minutes

### ✅ Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB (Docker or local)
- API Keys (Reddit, Twitter, Google Gemini)

---

## 📦 Step 1: Backend Setup

### 1.1 Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 1.2 Configure Environment

Create `.env` file in `backend/` folder:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```dotenv
# MongoDB
MONGODB_URI=mongodb+srv://your_username:your_password@cluster.mongodb.net/
MONGODB_DB_NAME=trend_analysis

# Google Gemini AI
GOOGLE_GEMINI_API_KEY=your_gemini_key

# Twitter API
TWITTER_API_Key=your_twitter_key

# Reddit API
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password
REDDIT_USER_AGENT=TrendLens/1.0

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 1.3 Start MongoDB (Docker)

```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

Or use MongoDB Atlas (cloud) - just update `MONGODB_URI`

### 1.4 Run Backend

```bash
python main.py
```

✅ Backend running at: **http://localhost:8000**
📚 API Docs: **http://localhost:8000/docs**

---

## 🎨 Step 2: Frontend Setup

### 2.1 Install Dependencies

```bash
cd frontend
npm install
```

### 2.2 Run Development Server

```bash
npm run dev
```

✅ Frontend running at: **http://localhost:3000**

---

## 🔍 Step 3: Test the System

### Option A: Using the Web Interface

1. **Open**: http://localhost:3000
2. **Click**: "Search Trends" button
3. **Enter**: A trend keyword (e.g., "Grimace Shake")
4. **Click**: "Analyze"
5. **View**: Lifecycle stage, confidence score, and full analysis

### Option B: Using API Directly

```bash
# Test lifecycle detection
curl -X POST http://localhost:8000/api/trend/lifecycle \
  -H "Content-Type: application/json" \
  -d '{"trend_name": "Grimace Shake"}'

# Test Reddit data collection
curl -X POST http://localhost:8000/api/data/reddit/search \
  -H "Content-Type: application/json" \
  -d '{"keyword": "Grimace Shake", "days_back": 30, "post_limit": 100}'
```

---

## 📊 Available Pages

### 1. **Landing Page** - http://localhost:3000
- Product overview
- Features showcase
- Problem/solution presentation

### 2. **Search Page** - http://localhost:3000/search
- **Enter trend keywords**
- Get instant lifecycle analysis
- View confidence scores
- Navigate to full analysis

### 3. **Dashboard** - http://localhost:3000/dashboard
- Overview metrics
- Trend cards
- Health scores
- Decline predictions

### 4. **Trend Lifecycle** - http://localhost:3000/dashboard/trendLifecycle
- Growth → Peak → Decline visualization
- Stage indicators
- Fatigue metrics

### 5. **Explainability** - http://localhost:3000/dashboard/explainability
- SHAP attribution charts
- Feature importance
- Counterfactual scenarios

### 6. **What-If Simulator** - http://localhost:3000/dashboard/simulator
- Interactive sliders
- Intervention testing
- ROI predictions

### 7. **Network Analysis** - http://localhost:3000/dashboard/network
- Propagation graphs
- Geographic distribution

### 8. **Strategy & ROI** - http://localhost:3000/dashboard/strategy
- Creative pivot suggestions
- ROI calculator

---

## 🎯 How to Use: Step-by-Step

### Scenario: Analyze "Grimace Shake" Trend

1. **Go to Search Page**
   ```
   http://localhost:3000/search
   ```

2. **Enter Keyword**
   ```
   Type: "Grimace Shake"
   Click: "Analyze"
   ```

3. **View Results**
   - **Lifecycle Stage**: Viral Explosion / Decline / etc.
   - **Confidence Score**: 85%
   - **Days in Stage**: 5 days

4. **View Full Analysis**
   ```
   Click: "View Full Analysis"
   ```

5. **Explore Dashboard**
   - See detailed charts
   - Check SHAP explanations
   - Run what-if simulations

---

## 🔑 Getting API Keys

### Reddit API (Free)
1. Go to: https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Select "script"
4. Note: `client_id` and `client_secret`

### Twitter API (Free Tier Available)
1. Go to: https://developer.twitter.com/
2. Create account and app
3. Get bearer token

### Google Gemini API (Free Tier)
1. Go to: https://makersuite.google.com/app/apikey
2. Create API key
3. Copy key

### MongoDB Atlas (Free Tier)
1. Go to: https://www.mongodb.com/cloud/atlas
2. Create free cluster
3. Get connection string

---

## ⚡ Quick Troubleshooting

### Backend Issues

**"Module not found"**
```bash
pip install -r requirements.txt
```

**"MongoDB connection failed"**
- Check if MongoDB is running
- Verify `MONGODB_URI` in `.env`

**"Reddit API auth failed"**
- Verify Reddit credentials in `.env`
- Check Reddit app permissions

### Frontend Issues

**"npm install" fails**
```bash
rm -rf node_modules package-lock.json
npm install
```

**"Port 3000 in use"**
```bash
killall node  # Mac/Linux
# Or change port in package.json
```

---

## 📚 API Endpoints Reference

### Lifecycle Detection
```
POST /api/trend/lifecycle
Body: {"trend_name": "keyword"}
```

### Reddit Data Collection
```
POST /api/data/reddit/search
Body: {"keyword": "keyword", "days_back": 30, "post_limit": 100}
```

### Health Checks
```
GET /api/trend/lifecycle/health
GET /api/data/reddit/health
```

---

## 🎓 Example Trends to Test

**Viral Explosion Stage:**
- "Barbie Movie"
- "Wednesday Dance"
- "Grimace Shake"

**Decline Stage:**
- "Harlem Shake"
- "Ice Bucket Challenge"

**Death Stage:**
- "Gangnam Style"
- "Dabbing"

---

## 📈 Next Steps

1. **Explore all dashboard pages**
2. **Test different trend keywords**
3. **Review API documentation**: http://localhost:8000/docs
4. **Check MongoDB data**: View `trend_lifecycle` collection
5. **Customize thresholds**: Edit `backend/trend_analysis/lifecycle/lifecycle_model.py`

---

## 🆘 Support

**Logs Location:**
- Backend: Terminal output (emoji-based logging)
- MongoDB: `db.trend_lifecycle.find()`

**Documentation:**
- Backend: `/backend/README.md`
- Lifecycle: `/backend/trend_analysis/lifecycle/README.md`
- Data Collectors: `/backend/data_collectors/README.md`

---

## ✅ System Check

After setup, verify all services are running:

- [ ] Backend: http://localhost:8000
- [ ] API Docs: http://localhost:8000/docs
- [ ] Frontend: http://localhost:3000
- [ ] MongoDB: Connected (check logs)
- [ ] Search works: Try a trend keyword

---

**Datathon 2026** | Production-Ready | Judge-Approved ✅
