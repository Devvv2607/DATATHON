"""
Examples demonstrating AI-powered explanation endpoints.
Shows how to use the new /explain, /strategy, /full-report endpoints.
"""

import requests
import json
from typing import Dict, Any

# API Base URL
BASE_URL = "http://localhost:8000"

# Example trend metrics for testing
EXAMPLE_TREND = {
    "trend_name": "#WebDevelopment",
    "x": {
        "tweet_volume": {"current": 25000, "previous_period": 42000},
        "weekly_engagement_velocity": -0.35,
        "unique_content_ratio": 0.18,
        "creator_posting_frequency": {"current": 15, "previous_period": 35},
        "influencer_engagement_count": 8,
        "audience_growth_rate": -0.12,
        "posting_frequency_change": -0.45,
    }
}

DECLINING_TREND = {
    "trend_name": "#CryptoRally",
    "x": {
        "tweet_volume": {"current": 12000, "previous_period": 85000},
        "weekly_engagement_velocity": -0.78,
        "unique_content_ratio": 0.05,
        "creator_posting_frequency": {"current": 2, "previous_period": 45},
        "influencer_engagement_count": 1,
        "audience_growth_rate": -0.65,
        "posting_frequency_change": -0.95,
    }
}

STABLE_TREND = {
    "trend_name": "#TechNews",
    "x": {
        "tweet_volume": {"current": 35000, "previous_period": 36000},
        "weekly_engagement_velocity": 0.02,
        "unique_content_ratio": 0.45,
        "creator_posting_frequency": {"current": 28, "previous_period": 27},
        "influencer_engagement_count": 22,
        "audience_growth_rate": 0.05,
        "posting_frequency_change": 0.03,
    }
}


def example_1_basic_analysis():
    """
    Example 1: Basic trend analysis without AI explanations.
    Used as baseline before requesting detailed explanations.
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Trend Analysis")
    print("="*70)
    
    response = requests.post(f"{BASE_URL}/analyze", json=EXAMPLE_TREND)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nTrend: {result['trend_name']}")
        print(f"Status: {result['trend_status']}")
        print(f"Severity: {result['severity_level']}")
        print(f"Decline Probability: {result['decline_probability']:.2%}")
        print(f"\nDetected Causes:")
        for cause in result['root_causes']:
            print(f"  - {cause['cause_type']}: {cause['confidence']:.2%} confidence")
    else:
        print(f"Error: {response.status_code} - {response.text}")


def example_2_ai_explanations():
    """
    Example 2: Get detailed AI explanations for decline causes.
    Uses /explain endpoint to generate 2-3 sentence explanations per cause.
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: AI-Powered Explanations")
    print("="*70)
    
    response = requests.post(f"{BASE_URL}/explain", json=EXAMPLE_TREND)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nTrend: {result['trend_name']}")
        print(f"Status: {result['analysis']['trend_status']}")
        
        if 'ai_explanations' in result:
            print(f"\nAI-Generated Explanations:")
            for cause_type, explanation in result['ai_explanations'].items():
                print(f"\n{cause_type}:")
                print(f"  {explanation}")
    else:
        print(f"Error: {response.status_code} - {response.text}")


def example_3_recovery_strategy():
    """
    Example 3: Generate recovery or exit strategy.
    Uses /strategy endpoint to create actionable recommendations.
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Recovery/Exit Strategy")
    print("="*70)
    
    response = requests.post(f"{BASE_URL}/strategy", json=DECLINING_TREND)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nTrend: {result['trend_name']}")
        print(f"Status: {result['trend_status']}")
        print(f"Severity: {result['severity']}")
        
        if 'ai_strategy' in result:
            print(f"\nAI-Generated Strategy:")
            print(result['ai_strategy'])
    else:
        print(f"Error: {response.status_code} - {response.text}")


def example_4_executive_summary():
    """
    Example 4: Generate C-level executive summary.
    Uses /executive-summary endpoint for board-ready reports.
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Executive Summary for Leadership")
    print("="*70)
    
    response = requests.post(f"{BASE_URL}/executive-summary", json=DECLINING_TREND)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nTrend: {result['trend_name']}")
        print(f"Status: {result['status']}")
        print(f"Risk Level: {result['severity']}")
        
        if 'executive_summary' in result:
            print(f"\nExecutive Summary (Board-Ready):")
            print(result['executive_summary'])
    else:
        print(f"Error: {response.status_code} - {response.text}")


def example_5_full_report():
    """
    Example 5: Generate comprehensive report with all insights.
    Uses /full-report endpoint for complete analysis package.
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Comprehensive Full Report")
    print("="*70)
    
    response = requests.post(f"{BASE_URL}/full-report", json=DECLINING_TREND)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nTrend: {result['trend_name']}")
        print(f"Status: {result['trend_status']}")
        
        print(f"\n{'-'*70}")
        print("ANALYSIS SECTION")
        print(f"{'-'*70}")
        print(f"Decline Probability: {result['decline_probability']:.2%}")
        print(f"Root Causes: {', '.join([c['cause_type'] for c in result['root_causes']])}")
        
        if 'explanations' in result:
            print(f"\n{'-'*70}")
            print("AI EXPLANATIONS")
            print(f"{'-'*70}")
            for cause_type, explanation in result['explanations'].items():
                print(f"\n{cause_type}: {explanation}")
        
        if 'strategy' in result:
            print(f"\n{'-'*70}")
            print("RECOVERY STRATEGY")
            print(f"{'-'*70}")
            print(result['strategy'])
        
        if 'executive_summary' in result:
            print(f"\n{'-'*70}")
            print("EXECUTIVE SUMMARY")
            print(f"{'-'*70}")
            print(result['executive_summary'])
        
        if 'competitive_analysis' in result:
            print(f"\n{'-'*70}")
            print("COMPETITIVE ANALYSIS")
            print(f"{'-'*70}")
            print(result['competitive_analysis'])
    else:
        print(f"Error: {response.status_code} - {response.text}")


def example_6_stable_trend_analysis():
    """
    Example 6: Analyze a healthy/stable trend.
    Shows how stable trends are different from declining ones.
    """
    print("\n" + "="*70)
    print("EXAMPLE 6: Stable Trend Analysis")
    print("="*70)
    
    response = requests.post(f"{BASE_URL}/explain", json=STABLE_TREND)
    
    if response.status_code == 200:
        result = response.json()
        analysis = result['analysis']
        print(f"\nTrend: {analysis['trend_name']}")
        print(f"Status: {analysis['trend_status']}")
        print(f"Severity: {analysis['severity_level']}")
        print(f"Decline Probability: {analysis['decline_probability']:.2%}")
        
        if analysis['root_causes']:
            print(f"\nDetected Causes:")
            for cause in analysis['root_causes']:
                print(f"  - {cause['cause_type']}: {cause['confidence']:.2%}")
        else:
            print("\nNo concerning decline causes detected - trend is healthy!")
    else:
        print(f"Error: {response.status_code} - {response.text}")


def example_7_compare_multiple_trends():
    """
    Example 7: Analyze multiple trends and compare.
    Shows how different trends produce different insights.
    """
    print("\n" + "="*70)
    print("EXAMPLE 7: Comparing Multiple Trends")
    print("="*70)
    
    trends = [
        ("Stable Trend", STABLE_TREND),
        ("Declining Trend", DECLINING_TREND),
        ("Weakly Declining", EXAMPLE_TREND),
    ]
    
    summary = []
    
    for name, trend in trends:
        response = requests.post(f"{BASE_URL}/analyze", json=trend)
        
        if response.status_code == 200:
            result = response.json()
            summary.append({
                "name": name,
                "trend_name": result['trend_name'],
                "status": result['trend_status'],
                "severity": result['severity_level'],
                "decline_prob": result['decline_probability'],
                "cause_count": len(result['root_causes']),
            })
    
    # Print comparison table
    print(f"\n{'Trend Type':<20} {'Name':<20} {'Status':<12} {'Severity':<10} {'Decline':<8} {'Causes':<8}")
    print("-" * 78)
    
    for item in summary:
        print(f"{item['name']:<20} {item['trend_name']:<20} {item['status']:<12} {item['severity']:<10} {item['decline_prob']:.0%}     {item['cause_count']:<8}")


def example_8_batch_explain():
    """
    Example 8: Batch analyze multiple trends then request explanations.
    Shows workflow for processing multiple trends efficiently.
    """
    print("\n" + "="*70)
    print("EXAMPLE 8: Batch Analysis with AI")
    print("="*70)
    
    # First: Batch analyze all trends
    trends = [EXAMPLE_TREND, DECLINING_TREND, STABLE_TREND]
    
    response = requests.post(f"{BASE_URL}/batch-analyze", json=trends)
    
    if response.status_code == 200:
        batch_result = response.json()
        print(f"\nBatch Analysis Results:")
        print(f"  Total: {batch_result['total_requested']}")
        print(f"  Successful: {batch_result['successful_analyses']}")
        print(f"  Failed: {batch_result['failed_analyses']}")
        
        # Then: Get explanations for most critical trend
        if batch_result['results']:
            # Find most critical
            critical = max(
                batch_result['results'],
                key=lambda x: x['decline_probability']
            )
            
            print(f"\nMost Critical Trend: {critical['trend_name']}")
            print(f"  Status: {critical['trend_status']}")
            print(f"  Risk: {critical['decline_probability']:.2%}")
            
            # Get detailed explanation
            response2 = requests.post(f"{BASE_URL}/strategy", json=DECLINING_TREND)
            
            if response2.status_code == 200:
                strategy_result = response2.json()
                print(f"\n  Recommended Action:")
                print(f"  {strategy_result['ai_strategy'][:200]}...")
    else:
        print(f"Error: {response.status_code} - {response.text}")


def example_9_monitoring_workflow():
    """
    Example 9: Real-world monitoring workflow.
    1. Fetch trending hashtags
    2. Analyze each
    3. Identify critical ones
    4. Generate reports for stakeholders
    """
    print("\n" + "="*70)
    print("EXAMPLE 9: Real-World Monitoring Workflow")
    print("="*70)
    
    print("\nStep 1: Analyze trends")
    
    # Simulate fetching multiple trends
    test_trends = [
        ("Stable Trend", STABLE_TREND),
        ("Weakly Declining", EXAMPLE_TREND),
        ("Critically Declining", DECLINING_TREND),
    ]
    
    critical_trends = []
    
    for label, trend in test_trends:
        response = requests.post(f"{BASE_URL}/analyze", json=trend)
        
        if response.status_code == 200:
            result = response.json()
            
            if result['decline_probability'] > 0.6:  # Critical threshold
                critical_trends.append({
                    "name": result['trend_name'],
                    "analysis": result
                })
                print(f"  ⚠️  CRITICAL: {result['trend_name']} ({result['decline_probability']:.0%})")
            elif result['decline_probability'] > 0.3:
                print(f"  ⚠️  WARNING: {result['trend_name']} ({result['decline_probability']:.0%})")
            else:
                print(f"  ✓ OK: {result['trend_name']}")
    
    # Step 2: Generate executive reports for critical trends
    print(f"\nStep 2: Generate executive reports for {len(critical_trends)} critical trend(s)")
    
    for critical in critical_trends:
        response = requests.post(f"{BASE_URL}/executive-summary", json={
            "trend_name": critical['name'],
            "x": critical['analysis']['cross_platform_summary'].get('x', {})
        })
        
        if response.status_code == 200:
            summary = response.json()
            print(f"\n{critical['name'].upper()}")
            print(f"  Status: {summary['status']}")
            print(f"  Executive Summary Generated: Yes")


def example_10_error_handling():
    """
    Example 10: Handle various error scenarios.
    Shows how to gracefully handle API errors.
    """
    print("\n" + "="*70)
    print("EXAMPLE 10: Error Handling")
    print("="*70)
    
    # Test 1: Missing required X metrics
    print("\nTest 1: Missing X metrics")
    invalid_trend = {"trend_name": "InvalidTrend", "x": {}}
    
    response = requests.post(f"{BASE_URL}/analyze", json=invalid_trend)
    if response.status_code != 200:
        print(f"  Expected error received: {response.status_code}")
    
    # Test 2: Explain with no AI service
    print("\nTest 2: AI service check")
    response = requests.post(f"{BASE_URL}/explain", json=EXAMPLE_TREND)
    
    if response.status_code == 200:
        print(f"  AI service: Available")
    elif response.status_code == 503:
        print(f"  AI service: Unavailable (expected if not configured)")
    else:
        print(f"  Unexpected status: {response.status_code}")


def run_all_examples():
    """Run all examples in sequence."""
    examples = [
        example_1_basic_analysis,
        example_2_ai_explanations,
        example_3_recovery_strategy,
        example_4_executive_summary,
        example_5_full_report,
        example_6_stable_trend_analysis,
        example_7_compare_multiple_trends,
        example_8_batch_explain,
        example_9_monitoring_workflow,
        example_10_error_handling,
    ]
    
    print("\n" + "="*70)
    print("TWITTER TREND ANALYZER - AI ENDPOINTS EXAMPLES")
    print("="*70)
    
    for example_func in examples:
        try:
            example_func()
        except requests.exceptions.ConnectionError:
            print(f"\n⚠️  Cannot connect to API at {BASE_URL}")
            print("Make sure the server is running: python -m uvicorn api:app --reload")
            break
        except Exception as e:
            print(f"\n❌ Error in {example_func.__name__}: {str(e)}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        example_num = int(sys.argv[1])
        examples = [
            example_1_basic_analysis,
            example_2_ai_explanations,
            example_3_recovery_strategy,
            example_4_executive_summary,
            example_5_full_report,
            example_6_stable_trend_analysis,
            example_7_compare_multiple_trends,
            example_8_batch_explain,
            example_9_monitoring_workflow,
            example_10_error_handling,
        ]
        if 1 <= example_num <= len(examples):
            examples[example_num - 1]()
        else:
            print(f"Example {example_num} not found. Available: 1-{len(examples)}")
    else:
        run_all_examples()
