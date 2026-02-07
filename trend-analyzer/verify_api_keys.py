#!/usr/bin/env python3
"""
API Key Verification Script
Verifies that Twitter and Featherless AI keys are configured and working.
"""

import sys
from config import get_config

def verify_api_keys():
    """Verify API keys are configured."""
    
    print("\n" + "="*80)
    print("API KEY VERIFICATION")
    print("="*80 + "\n")
    
    config = get_config()
    
    # Check Twitter API Key
    print("1️⃣  TWITTER API KEY")
    print("-" * 80)
    
    twitter_key = config.TWITTER_API_KEY
    if twitter_key and twitter_key != "your_key_here":
        key_display = twitter_key[:20] + "..." + twitter_key[-10:]
        print(f"   ✅ CONFIGURED: {key_display}")
        print(f"   Host: {config.TWITTER_API_HOST}")
    else:
        print("   ❌ NOT CONFIGURED")
        print("   Set TWITTER_API_KEY environment variable")
        return False
    
    # Check Featherless AI Key
    print("\n2️⃣  FEATHERLESS AI KEY")
    print("-" * 80)
    
    featherless_key = config.FEATHERLESS_API_KEY
    if featherless_key and featherless_key != "your_key_here":
        key_display = featherless_key[:20] + "..." + featherless_key[-10:]
        print(f"   ✅ CONFIGURED: {key_display}")
        print(f"   URL: {config.FEATHERLESS_API_URL}")
        print(f"   Model: {config.FEATHERLESS_MODEL}")
    else:
        print("   ❌ NOT CONFIGURED")
        print("   Set FEATHERLESS_API_KEY environment variable")
        return False
    
    # Other Configuration
    print("\n3️⃣  OTHER CONFIGURATION")
    print("-" * 80)
    print(f"   Min Confidence Threshold: {config.MIN_CONFIDENCE_THRESHOLD}")
    print(f"   Default Location: {config.DEFAULT_LOCATION}")
    print(f"   Log Level: {config.LOG_LEVEL}")
    
    return True

def test_twitter_client():
    """Test Twitter API client initialization."""
    
    print("\n4️⃣  TWITTER API CLIENT")
    print("-" * 80)
    
    try:
        from twitter_api import TwitterAPIClient
        
        client = TwitterAPIClient()
        print("   ✅ Twitter API client initialized successfully")
        return True
    except Exception as e:
        print(f"   ⚠️  Warning: {str(e)}")
        return False

def test_explanation_engine():
    """Test Featherless AI client initialization."""
    
    print("\n5️⃣  FEATHERLESS AI ENGINE")
    print("-" * 80)
    
    try:
        from explanation_engine import TrendAnalysisExplainer
        
        explainer = TrendAnalysisExplainer()
        print("   ✅ Featherless AI client initialized successfully")
        return True
    except Exception as e:
        print(f"   ⚠️  Warning: {str(e)}")
        print("   This is expected if API key is invalid or service is unavailable")
        return False

def test_core_analyzer():
    """Test core trend analyzer."""
    
    print("\n6️⃣  TREND ANALYZER")
    print("-" * 80)
    
    try:
        from trend_analyzer import TrendAnalyzer
        from sample_data import load_sample_data
        
        analyzer = TrendAnalyzer()
        sample = load_sample_data("declining")
        result = analyzer.analyze(sample)
        
        print(f"   ✅ Analyzer works correctly")
        print(f"      Sample trend: {result['trend_name']}")
        print(f"      Status: {result['trend_status']}")
        print(f"      Confidence: {result['confidence_in_analysis']:.0%}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def main():
    """Run all verification tests."""
    
    all_passed = True
    
    # Verify keys
    if not verify_api_keys():
        all_passed = False
    
    # Test clients
    if not test_twitter_client():
        all_passed = False
    
    if not test_explanation_engine():
        all_passed = False
    
    if not test_core_analyzer():
        all_passed = False
    
    # Summary
    print("\n" + "="*80)
    if all_passed:
        print("✅ ALL CHECKS PASSED - SYSTEM READY!")
        print("="*80)
        print("\nYou can now:")
        print("  1. Start the API server: python -m uvicorn api:app --reload")
        print("  2. Try examples: python examples_ai_endpoints.py")
        print("  3. Run demo: python demo_all_features.py")
        return 0
    else:
        print("⚠️  SOME CHECKS FAILED - SEE ABOVE FOR DETAILS")
        print("="*80)
        return 1

if __name__ == "__main__":
    sys.exit(main())
