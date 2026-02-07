#!/usr/bin/env python3
"""
STARTUP CHECKLIST - Twitter Trend Intelligence Engine with AI Explanations

Follow these steps to get everything running.
"""

def print_step(num, title, description=""):
    """Print a formatted step."""
    print(f"\n{'='*80}")
    print(f"STEP {num}: {title}")
    print(f"{'='*80}")
    if description:
        print(f"\n{description}\n")

def print_substep(letter, action):
    """Print a formatted substep."""
    print(f"  {letter}. {action}")

def print_code(code):
    """Print formatted code."""
    print(f"\n  $ {code}\n")

# Main checklist
print("\n" + "="*80)
print("TWITTER TREND INTELLIGENCE ENGINE - STARTUP CHECKLIST")
print("="*80)

print_step(1, "ENVIRONMENT SETUP", 
    "Configure your environment with required API keys and settings.")

print("  Option A: Using Environment Variables")
print_code("export FEATHERLESS_API_KEY='rc_16258f4d33f9df27a5a977ef7010dee1344c6fb68e073e5e749f83c20c780b6c'")
print_code("export TWITTER_API_KEY='67d16668demsh8563ec142db49dap16b0c2jsnf8fe97893ba1'")
print_code("export APP_ENV='development'")

print("  Option B: Using .env File")
print("  Create '.env' in trend-analyzer/ directory with:")
print("""
  FEATHERLESS_API_KEY=rc_16258f4d33f9df27a5a977ef7010dee1344c6fb68e073e5e749f83c20c780b6c
  TWITTER_API_KEY=67d16668demsh8563ec142db49dap16b0c2jsnf8fe97893ba1
  APP_ENV=development
  MIN_CONFIDENCE_THRESHOLD=0.3
""")

print_step(2, "INSTALL DEPENDENCIES",
    "Install required Python packages from requirements.txt")

print_code("pip install -r requirements.txt")

print("  Key packages being installed:")
print("  • fastapi==0.104.1 (REST framework)")
print("  • uvicorn==0.24.0 (ASGI server)")
print("  • pydantic==2.5.0 (Data validation)")
print("  • openai==1.3.8 (Featherless AI client)")
print("  • requests==2.31.0 (HTTP library)")

print_step(3, "VERIFY INSTALLATION",
    "Check that all dependencies installed correctly.")

print_code("python -c \"import fastapi; import pydantic; import openai; print('✓ All dependencies installed')\"")

print_step(4, "QUICK API TEST (OPTIONAL)",
    "Test core analysis without starting the server.")

print("  Run this Python code to test:")
print("""
  from trend_analyzer import TrendAnalyzer
  from sample_data import load_sample_data
  
  analyzer = TrendAnalyzer()
  sample = load_sample_data("declining")
  result = analyzer.analyze(sample)
  
  print(f"Trend Status: {result['trend_status']}")
  print(f"Decline Probability: {result['decline_probability']:.2%}")
""")

print_code("python")

print_step(5, "TEST AI EXPLANATIONS (OPTIONAL)",
    "Test Featherless AI integration.")

print("  Run this Python code:")
print("""
  from explanation_engine import TrendAnalysisExplainer
  from trend_analyzer import TrendAnalyzer
  from sample_data import load_sample_data
  
  analyzer = TrendAnalyzer()
  explainer = TrendAnalysisExplainer()
  
  sample = load_sample_data("declining")
  analysis = analyzer.analyze(sample)
  explanations = explainer.explain_decline_causes(analysis)
  
  for cause, explanation in explanations.items():
      print(f"{cause}:\\n  {explanation}\\n")
""")

print_code("python")

print_step(6, "START THE API SERVER",
    "Launch the FastAPI application.")

print("  Development Mode (with auto-reload):")
print_code("python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000")

print("  Production Mode (multiple workers):")
print_code("python -m uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4")

print("  Expected output:")
print("""
  INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
  INFO:     Started server process [xxxx]
  INFO:     Waiting for application startup.
  INFO:     Application startup complete.
""")

print_step(7, "ACCESS THE API",
    "Open your browser and test the API documentation.")

print("  Interactive API Documentation (Swagger UI):")
print("  ► http://localhost:8000/docs")
print("")
print("  Alternative Documentation (ReDoc):")
print("  ► http://localhost:8000/redoc")
print("")
print("  API Root Information:")
print("  ► http://localhost:8000/")

print_step(8, "TEST ENDPOINTS",
    "Try the endpoints using curl or the interactive docs.")

print("  Test 1: Health Check")
print_code("curl http://localhost:8000/health")

print("  Test 2: Sample Analysis (Declining Trend)")
print_code("curl 'http://localhost:8000/sample-analysis?sample_type=declining'")

print("  Test 3: Sample Analysis (Growing Trend)")
print_code("curl 'http://localhost:8000/sample-analysis?sample_type=growing'")

print("  Test 4: AI Explanations (requires FEATHERLESS_API_KEY)")
print_code("""curl -X POST 'http://localhost:8000/explain' \\
  -H 'Content-Type: application/json' \\
  -d '{
    "trend_name": "#TechTok",
    "x": {
      "tweet_volume": {"current": 45000, "previous_period": 52000},
      "weekly_engagement_velocity": -0.15,
      "unique_content_ratio": 0.25
    }
  }'""")

print_step(9, "EXPLORE THE SYSTEM",
    "Learn about all features with examples and documentation.")

print("  Run the interactive demo (8 comprehensive demos):")
print_code("python demo_all_features.py")

print("  Run all API examples (10 different scenarios):")
print_code("python examples_ai_endpoints.py")

print("  Run specific example (e.g., Example 5: Full Report):")
print_code("python examples_ai_endpoints.py 5")

print("  Original usage examples:")
print_code("python examples.py")

print_step(10, "READ DOCUMENTATION",
    "Understand the system architecture and capabilities.")

print("  Quick Start & Reference:")
print("  ► Read: README_AI_ENDPOINTS.md")
print("  ► Quick Reference: QUICK_REFERENCE.md")
print("")
print("  Advanced Patterns & Workflows:")
print("  ► Read: AI_INTEGRATION_GUIDE.md")
print("")
print("  Original Project Documentation:")
print("  ► Read: README.md")
print("  ► Read: TWITTER_ONLY_GUIDE.md")

print_step(11, "INTEGRATION & DEPLOYMENT (OPTIONAL)",
    "For production use cases.")

print("  Docker Deployment:")
print("  • Create Dockerfile with Python 3.11 base")
print("  • Install requirements.txt")
print("  • Run: python -m uvicorn api:app --host 0.0.0.0")
print("")
print("  Cloud Deployment:")
print("  • AWS ECS, Lambda, EC2")
print("  • Google Cloud Run, App Engine")
print("  • Azure App Service, Container Instances")
print("  • Heroku, Railway, PaaS")
print("")
print("  Database Integration:")
print("  • PostgreSQL for historical data")
print("  • Redis for caching results")
print("  • Elasticsearch for search")

print_step(12, "TROUBLESHOOTING",
    "Common issues and solutions.")

print("  Problem: 'ModuleNotFoundError: No module named fastapi'")
print("  Solution: Run: pip install -r requirements.txt")
print("")
print("  Problem: 'AI service not available (503 error)'")
print("  Solution: Check FEATHERLESS_API_KEY is set correctly")
print("")
print("  Problem: 'CORS error in browser'")
print("  Solution: CORS is enabled in api.py, check console for details")
print("")
print("  Problem: Analysis returns low confidence")
print("  Solution: Provide more X metrics in request")
print("")
print("  For more help:")
print("  ► See: AI_INTEGRATION_GUIDE.md (Troubleshooting section)")
print("  ► Run: demo_all_features.py (Example 10 shows error handling)")

print_step(13, "NEXT STEPS",
    "What to do after getting everything running.")

print("  For Development:")
print("  • Customize prompts in explanation_engine.py")
print("  • Adjust MIN_CONFIDENCE_THRESHOLD in config.py")
print("  • Add new endpoints for specific use cases")
print("  • Implement caching for expensive operations")
print("")
print("  For Production:")
print("  • Set up database for trend history")
print("  • Implement authentication and rate limiting")
print("  • Set up monitoring and alerting")
print("  • Configure logging aggregation")
print("  • Deploy to cloud platform")
print("")
print("  For Enhancement:")
print("  • Add competitor tracking")
print("  • Build visualization dashboard")
print("  • Implement trend prediction ML model")
print("  • Create mobile app for alerts")
print("  • Add more platform integrations")

# Final summary
print("\n" + "="*80)
print("SETUP COMPLETE!")
print("="*80)

print("""
You now have a fully functional Twitter Trend Intelligence Engine with:

✅ Core trend analysis with 8 decline detectors
✅ AI-powered explanations via Featherless AI
✅ Strategic recommendations (recovery/exit)
✅ Executive summaries for leadership
✅ REST API with 12 endpoints
✅ Real Twitter/X API integration
✅ Comprehensive documentation
✅ Multiple usage examples
✅ Interactive demonstration

Quick Links:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
API Documentation:    http://localhost:8000/docs
API Root:             http://localhost:8000/
Health Check:         curl http://localhost:8000/health
Sample Analysis:      curl 'http://localhost:8000/sample-analysis?sample_type=declining'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Files to Review:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 README_AI_ENDPOINTS.md     ← Start here!
📄 QUICK_REFERENCE.md         ← API quick reference
📄 AI_INTEGRATION_GUIDE.md    ← Detailed workflows
📄 COMPLETION_SUMMARY.txt     ← What was built

Scripts to Run:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🐍 demo_all_features.py       ← Interactive 8-part demo
🐍 examples_ai_endpoints.py   ← 10 usage examples
🐍 examples.py                ← Original 12 examples

Start the Server:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
python -m uvicorn api:app --reload

Then open: http://localhost:8000/docs

Happy analyzing! 🚀
""")

print("="*80)
