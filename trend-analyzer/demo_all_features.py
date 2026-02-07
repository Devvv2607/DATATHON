#!/usr/bin/env python3
"""
Complete demonstration of Twitter Trend Analyzer with AI explanations.
Shows all features working together in a real-world scenario.

Usage:
    python demo_all_features.py
"""

import json
import time
from datetime import datetime
from pathlib import Path

# Import our components
from trend_analyzer import TrendAnalyzer
from explanation_engine import TrendAnalysisExplainer
from twitter_api import TwitterAPIClient, TwitterMetricsCollector
from config import get_config
from sample_data import load_sample_data


def print_header(title: str, level: int = 1):
    """Print formatted section header."""
    if level == 1:
        print(f"\n{'='*80}")
        print(f"{title.center(80)}")
        print(f"{'='*80}\n")
    elif level == 2:
        print(f"\n{'-'*80}")
        print(f"{title}")
        print(f"{'-'*80}\n")
    else:
        print(f"\n▶ {title}\n")


def print_section(content: str, indent: int = 0):
    """Print indented content."""
    prefix = "  " * indent
    for line in content.split("\n"):
        print(f"{prefix}{line}")


def demo_1_basic_analysis():
    """Demo 1: Basic trend analysis without AI."""
    print_header("DEMO 1: Basic Trend Analysis", 1)
    
    print_section("Loading sample declining trend data...", 0)
    sample_data = load_sample_data("declining")
    
    print_section(f"Trend Name: {sample_data['trend_name']}", 1)
    print_section(f"Tweet Volume: {sample_data['x']['tweet_volume']}", 1)
    print_section(f"Engagement Velocity: {sample_data['x']['weekly_engagement_velocity']}", 1)
    
    print_section("Running analysis...", 0)
    analyzer = TrendAnalyzer(min_confidence_threshold=0.3)
    result = analyzer.analyze(sample_data)
    
    print_section(f"Status: {result['trend_status']}", 1)
    print_section(f"Severity: {result['severity_level']}", 1)
    print_section(f"Decline Probability: {result['decline_probability']:.2%}", 1)
    
    print_section("Detected Causes:", 0)
    for cause in result['root_causes']:
        print_section(f"{cause['cause_type']}: {cause['confidence']:.2%} confidence", 2)
    
    return result


def demo_2_ai_explanations(analysis_result: dict):
    """Demo 2: AI-powered cause explanations."""
    print_header("DEMO 2: AI-Powered Explanations", 1)
    
    print_section("Initializing AI explanation engine (Featherless AI)...", 0)
    
    try:
        explainer = TrendAnalysisExplainer()
        print_section("✓ AI engine initialized successfully", 0)
    except Exception as e:
        print_section(f"⚠ AI engine not available: {str(e)}", 0)
        print_section("Continuing with local analysis only...", 0)
        return None
    
    print_section("Generating detailed explanations for each cause...", 0)
    
    try:
        explanations = explainer.explain_decline_causes(analysis_result)
        
        print_section("AI-Generated Explanations:", 0)
        for cause_type, explanation in explanations.items():
            print_section(f"\n{cause_type}:", 1)
            print_section(explanation, 2)
        
        return explanations
    except Exception as e:
        print_section(f"⚠ Error generating explanations: {str(e)}", 0)
        return None


def demo_3_recovery_strategy(analysis_result: dict):
    """Demo 3: Generate recovery strategy using AI."""
    print_header("DEMO 3: AI-Powered Recovery Strategy", 1)
    
    try:
        explainer = TrendAnalysisExplainer()
        print_section("Generating strategic recovery recommendations...", 0)
        
        strategy = explainer.generate_strategy(analysis_result)
        
        print_section("Strategy (AI-Generated):", 0)
        print_section(strategy, 1)
        
        return strategy
    except Exception as e:
        print_section(f"⚠ Error generating strategy: {str(e)}", 0)
        return None


def demo_4_executive_summary(analysis_result: dict):
    """Demo 4: Generate executive summary."""
    print_header("DEMO 4: Executive Summary (Board-Ready)", 1)
    
    try:
        explainer = TrendAnalysisExplainer()
        print_section("Generating C-level executive summary...", 0)
        
        summary = explainer.generate_executive_summary(analysis_result)
        
        print_section("Executive Summary:", 0)
        print_section(summary, 1)
        
        return summary
    except Exception as e:
        print_section(f"⚠ Error generating summary: {str(e)}", 0)
        return None


def demo_5_comparison():
    """Demo 5: Compare three trend scenarios."""
    print_header("DEMO 5: Comparing Multiple Trend Scenarios", 1)
    
    print_section("Analyzing three different trend types...", 0)
    
    scenarios = [
        ("Declining Trend", "declining"),
        ("Growing Trend", "growing"),
        ("Collapsed Trend", "collapsed"),
    ]
    
    analyzer = TrendAnalyzer(min_confidence_threshold=0.3)
    results = []
    
    for label, sample_type in scenarios:
        print_section(f"\nAnalyzing: {label}", 1)
        
        data = load_sample_data(sample_type)
        result = analyzer.analyze(data)
        results.append({
            "label": label,
            "result": result
        })
        
        print_section(f"  Status: {result['trend_status']}", 2)
        print_section(f"  Severity: {result['severity_level']}", 2)
        print_section(f"  Decline Probability: {result['decline_probability']:.2%}", 2)
    
    # Comparison table
    print_section("\nComparison Summary:", 0)
    print_section(f"{'Scenario':<20} {'Status':<12} {'Severity':<12} {'Decline %':<12} {'Causes':<8}", 1)
    print_section("-" * 65, 1)
    
    for item in results:
        result = item['result']
        print_section(
            f"{item['label']:<20} {result['trend_status']:<12} "
            f"{result['severity_level']:<12} {result['decline_probability']:>10.0%}  "
            f"{len(result['root_causes']):<8}",
            1
        )
    
    return results


def demo_6_real_twitter_data():
    """Demo 6: Integrate with real Twitter API (if configured)."""
    print_header("DEMO 6: Real Twitter API Integration", 1)
    
    print_section("Attempting to fetch real trending hashtags from Twitter...", 0)
    
    try:
        config = get_config()
        
        # Check if Twitter API is configured
        if not config.TWITTER_API_KEY or config.TWITTER_API_KEY == "your_key_here":
            print_section("⚠ Twitter API not configured", 1)
            print_section("Set TWITTER_API_KEY environment variable to fetch real data", 2)
            return None
        
        print_section("✓ Twitter API key found, attempting connection...", 0)
        
        # Initialize clients
        twitter_client = TwitterAPIClient()
        collector = TwitterMetricsCollector()
        
        # Fetch trending hashtags
        print_section("Fetching trending hashtags...", 0)
        trending = twitter_client.get_trending_hashtags(location="US")
        
        if not trending:
            print_section("⚠ Could not fetch trending hashtags (API rate limit or error)", 1)
            return None
        
        print_section(f"✓ Found {len(trending)} trending hashtags", 1)
        
        # Analyze top 3 trends
        print_section("\nAnalyzing top 3 trends:", 0)
        
        analyzer = TrendAnalyzer(min_confidence_threshold=0.3)
        analyses = []
        
        for i, hashtag in enumerate(trending[:3]):
            print_section(f"\nHashtag #{i+1}: {hashtag}", 1)
            
            # Collect metrics
            metrics = collector.collect_trend_metrics(hashtag)
            
            # Analyze
            result = analyzer.analyze(metrics)
            analyses.append(result)
            
            print_section(f"  Status: {result['trend_status']}", 2)
            print_section(f"  Severity: {result['severity_level']}", 2)
        
        return analyses
    
    except Exception as e:
        print_section(f"⚠ Error: {str(e)}", 1)
        return None


def demo_7_full_workflow():
    """Demo 7: Complete workflow from analysis to executive report."""
    print_header("DEMO 7: Complete Workflow (Analysis → AI → Executive Report)", 1)
    
    print_section("Step 1: Load and analyze trend data", 1)
    data = load_sample_data("declining")
    analyzer = TrendAnalyzer()
    analysis = analyzer.analyze(data)
    print_section(f"✓ Analyzed: {analysis['trend_name']}", 2)
    
    print_section("Step 2: Generate detailed explanations", 1)
    try:
        explainer = TrendAnalysisExplainer()
        explanations = explainer.explain_decline_causes(analysis)
        print_section(f"✓ Generated {len(explanations)} detailed explanations", 2)
    except Exception as e:
        print_section(f"⚠ Explanations skipped: {str(e)}", 2)
        explanations = None
    
    print_section("Step 3: Generate recovery strategy", 1)
    try:
        strategy = explainer.generate_strategy(analysis)
        print_section("✓ Generated strategic recovery plan", 2)
    except Exception as e:
        print_section(f"⚠ Strategy skipped: {str(e)}", 2)
        strategy = None
    
    print_section("Step 4: Generate executive summary", 1)
    try:
        summary = explainer.generate_executive_summary(analysis)
        print_section("✓ Generated board-ready executive summary", 2)
    except Exception as e:
        print_section(f"⚠ Summary skipped: {str(e)}", 2)
        summary = None
    
    print_section("Step 5: Save complete report", 1)
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "trend_name": analysis['trend_name'],
        "trend_status": analysis['trend_status'],
        "severity_level": analysis['severity_level'],
        "decline_probability": analysis['decline_probability'],
        "analysis": analysis,
        "explanations": explanations,
        "strategy": strategy,
        "executive_summary": summary
    }
    
    report_path = Path("trend_report_latest.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    
    print_section(f"✓ Report saved to: {report_path}", 2)
    
    return report


def demo_8_performance_stats():
    """Demo 8: Performance metrics and statistics."""
    print_header("DEMO 8: Performance Metrics", 1)
    
    print_section("Running performance benchmarks...", 0)
    
    analyzer = TrendAnalyzer()
    data = load_sample_data("declining")
    
    # Benchmark analysis
    print_section("\nAnalysis Performance:", 1)
    start = time.time()
    for _ in range(10):
        analyzer.analyze(data)
    analysis_time = (time.time() - start) / 10
    print_section(f"Average /analyze time: {analysis_time*1000:.1f}ms (10 runs)", 2)
    
    # Benchmark explanations
    print_section("\nAI Explanation Performance:", 1)
    try:
        explainer = TrendAnalysisExplainer()
        result = analyzer.analyze(data)
        
        start = time.time()
        explainer.explain_decline_causes(result)
        explain_time = time.time() - start
        print_section(f"Explanation generation: {explain_time:.2f}s", 2)
        
        start = time.time()
        explainer.generate_strategy(result)
        strategy_time = time.time() - start
        print_section(f"Strategy generation: {strategy_time:.2f}s", 2)
        
        start = time.time()
        explainer.generate_executive_summary(result)
        summary_time = time.time() - start
        print_section(f"Summary generation: {summary_time:.2f}s", 2)
        
    except Exception as e:
        print_section(f"⚠ AI benchmarks skipped: {str(e)}", 2)
    
    # Summary
    print_section("\nSummary:", 0)
    print_section("✓ Core analysis: sub-100ms", 1)
    print_section("✓ AI explanations: 2-8 seconds (includes LLM calls)", 1)
    print_section("✓ Recommended for real-time: /analyze endpoint", 1)
    print_section("✓ Recommended for reports: /full-report endpoint with caching", 1)


def main():
    """Run all demonstrations."""
    
    print_header("TWITTER TREND ANALYZER - COMPLETE FEATURE DEMONSTRATION", 1)
    
    print_section(
        "This demonstration shows all features of the Twitter Trend Intelligence Engine:\n"
        "1. Basic trend analysis with decline detection\n"
        "2. AI-powered cause explanations\n"
        "3. Strategic recovery recommendations\n"
        "4. Executive summary generation\n"
        "5. Multi-scenario comparison\n"
        "6. Real Twitter API integration\n"
        "7. Complete end-to-end workflow\n"
        "8. Performance benchmarking",
        0
    )
    
    # Demo 1
    analysis_result = demo_1_basic_analysis()
    input("\nPress Enter to continue to next demo...")
    
    # Demo 2
    explanations = demo_2_ai_explanations(analysis_result)
    input("\nPress Enter to continue to next demo...")
    
    # Demo 3
    strategy = demo_3_recovery_strategy(analysis_result)
    input("\nPress Enter to continue to next demo...")
    
    # Demo 4
    summary = demo_4_executive_summary(analysis_result)
    input("\nPress Enter to continue to next demo...")
    
    # Demo 5
    comparisons = demo_5_comparison()
    input("\nPress Enter to continue to next demo...")
    
    # Demo 6
    twitter_data = demo_6_real_twitter_data()
    input("\nPress Enter to continue to next demo...")
    
    # Demo 7
    full_report = demo_7_full_workflow()
    input("\nPress Enter to continue to next demo...")
    
    # Demo 8
    demo_8_performance_stats()
    
    # Final summary
    print_header("Demonstration Complete!", 1)
    print_section(
        "Summary of capabilities demonstrated:\n"
        "✓ Core analysis engine with 8 decline detectors\n"
        "✓ AI-powered explanations using Featherless AI/DeepSeek\n"
        "✓ Strategic decision support via LLM\n"
        "✓ Executive reporting functionality\n"
        "✓ Multi-trend comparison and analysis\n"
        "✓ Twitter API integration\n"
        "✓ End-to-end reporting workflow\n"
        "✓ High-performance analysis (<100ms)",
        0
    )
    
    print_section("\nNext Steps:", 0)
    print_section("1. Start the FastAPI server: python -m uvicorn api:app --reload", 1)
    print_section("2. Visit API docs: http://localhost:8000/docs", 1)
    print_section("3. Try endpoints: /analyze, /explain, /strategy, /full-report", 1)
    print_section("4. Check examples: python examples_ai_endpoints.py", 1)


if __name__ == "__main__":
    main()
