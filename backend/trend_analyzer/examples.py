"""
Comprehensive examples showing how to use the Trend Analyzer.
Run this file directly or import individual examples.
"""

import json
from trend_analyzer import TrendAnalyzer
from sample_data import load_sample_data, SAMPLE_TREND_DATA, SAMPLE_TREND_GROWING, SAMPLE_TREND_COLLAPSED
from utils import (
    generate_executive_summary,
    export_analysis_report,
    detect_platform_health,
    merge_trend_analyses,
)


def example_1_basic_analysis():
    """Example 1: Basic trend analysis from sample data."""
    print("=" * 80)
    print("EXAMPLE 1: Basic Trend Analysis (Declining Trend)")
    print("=" * 80)
    
    analyzer = TrendAnalyzer()
    metrics = load_sample_data("declining")
    
    result = analyzer.analyze(metrics)
    
    print(json.dumps(result, indent=2))
    print()


def example_2_executive_summary():
    """Example 2: Generate executive summary."""
    print("=" * 80)
    print("EXAMPLE 2: Executive Summary")
    print("=" * 80)
    
    analyzer = TrendAnalyzer()
    metrics = load_sample_data("declining")
    result = analyzer.analyze(metrics)
    
    summary = generate_executive_summary(result)
    print(summary)
    print()


def example_3_export_formats():
    """Example 3: Export analysis in different formats."""
    print("=" * 80)
    print("EXAMPLE 3: Export in Multiple Formats")
    print("=" * 80)
    
    analyzer = TrendAnalyzer()
    metrics = load_sample_data("declining")
    result = analyzer.analyze(metrics)
    
    # JSON export
    print("\n--- JSON Export ---\n")
    json_report = export_analysis_report(result, format="json")
    print(json_report[:500] + "..." if len(json_report) > 500 else json_report)
    
    # Markdown export
    print("\n--- Markdown Export (first 1000 chars) ---\n")
    md_report = export_analysis_report(result, format="markdown")
    print(md_report[:1000] + "..." if len(md_report) > 1000 else md_report)
    
    # CSV export
    print("\n--- CSV Export ---\n")
    csv_report = export_analysis_report(result, format="csv")
    print(csv_report)
    print()


def example_4_growing_trend():
    """Example 4: Analyze a growing trend."""
    print("=" * 80)
    print("EXAMPLE 4: Growing Trend Analysis")
    print("=" * 80)
    
    analyzer = TrendAnalyzer()
    metrics = load_sample_data("growing")
    result = analyzer.analyze(metrics)
    
    print(f"Trend: {result['trend_name']}")
    print(f"Status: {result['trend_status']}")
    print(f"Decline Probability: {result['decline_probability']:.0%}")
    print(f"Severity: {result['severity_level']}")
    print(f"\nRoot Causes Detected: {len(result['root_causes'])}")
    
    if not result['root_causes']:
        print("✅ No significant decline causes detected.")
    
    print(f"\nRecommended Actions:")
    for action in result['recommended_actions'][:3]:
        print(f"- [{action['priority']}] {action['description'][:70]}...")
    print()


def example_5_collapsed_trend():
    """Example 5: Analyze a collapsed trend."""
    print("=" * 80)
    print("EXAMPLE 5: Collapsed Trend Analysis")
    print("=" * 80)
    
    analyzer = TrendAnalyzer()
    metrics = load_sample_data("collapsed")
    result = analyzer.analyze(metrics)
    
    print(f"Trend: {result['trend_name']}")
    print(f"Status: {result['trend_status']}")
    print(f"Decline Probability: {result['decline_probability']:.0%}")
    print(f"Severity: {result['severity_level']}")
    
    print(f"\nTop Root Causes:")
    for i, cause in enumerate(result['root_causes'][:3], 1):
        print(f"\n{i}. {cause['cause_type']} ({cause['confidence']:.0%} confidence)")
        print(f"   Platforms: {', '.join(cause['affected_platforms'])}")
        print(f"   Evidence: {cause['evidence'][0] if cause['evidence'] else 'N/A'}")
        print(f"   Business Impact: {cause['business_explanation'][:100]}...")
    print()


def example_6_platform_health():
    """Example 6: Check platform-specific health."""
    print("=" * 80)
    print("EXAMPLE 6: Cross-Platform Health Check")
    print("=" * 80)
    
    analyzer = TrendAnalyzer()
    metrics_dict = load_sample_data("declining")
    result = analyzer.analyze(metrics_dict)
    
    print(f"Trend: {result['trend_name']}\n")
    print("Platform Health Summary:")
    
    for platform, metrics in result['cross_platform_summary'].items():
        if platform == "X":
            print(f"\n🐦 X/Twitter")
            print(f"   Tweet Volume: {metrics['tweet_volume']:,}")
            print(f"   Engagement Velocity: {metrics['engagement_velocity']:.1%} per week")
            print(f"   Status: {metrics['health_status']}")
        
        elif platform == "Reddit":
            print(f"\n🔴 Reddit")
            print(f"   Post Volume: {metrics['post_volume']:,}")
            print(f"   Avg Comments: {metrics['avg_comments']:.1f}")
            print(f"   Status: {metrics['health_status']}")
        
        elif platform == "TikTok":
            print(f"\n🎵 TikTok")
            print(f"   Hashtag Views: {metrics['hashtag_views']:,}")
            print(f"   Video Count: {metrics['video_count']:,}")
            print(f"   Status: {metrics['health_status']}")
        
        elif platform == "Google_Trends":
            print(f"\n🔍 Google Trends")
            print(f"   Interest Score: {metrics['search_interest_score']}/100")
            print(f"   Interest Trend: {metrics['search_interest_slope']:.1%} per day")
            print(f"   Status: {metrics['health_status']}")
    
    print()


def example_7_custom_metrics():
    """Example 7: Analyze custom metrics (not sample data)."""
    print("=" * 80)
    print("EXAMPLE 7: Custom Metrics Analysis")
    print("=" * 80)
    
    custom_metrics = {
        "trend_name": "#CustomTrend",
        "x": {
            "tweet_volume": {"current": 50000, "previous_period": 55000},
            "weekly_engagement_velocity": -0.05,
            "unique_content_ratio": 0.55,
            "posts_per_day": {"current": 3000, "previous_period": 3100},
        },
        "reddit": {
            "posts_volume": {"current": 2000, "previous_period": 2100},
            "subscriber_growth_rate": 0.02,
        },
    }
    
    analyzer = TrendAnalyzer()
    result = analyzer.analyze(custom_metrics)
    
    print(f"Trend: {result['trend_name']}")
    print(f"Status: {result['trend_status']}")
    print(f"Decline Probability: {result['decline_probability']:.0%}")
    print(f"\nAnalysis Confidence: {result['confidence_in_analysis']:.0%}")
    print(f"Root Causes Detected: {len(result['root_causes'])}")
    print()


def example_8_batch_analysis():
    """Example 8: Analyze multiple trends (batch mode simulation)."""
    print("=" * 80)
    print("EXAMPLE 8: Batch Analysis (Multiple Trends)")
    print("=" * 80)
    
    analyzer = TrendAnalyzer()
    
    # Simulate batch analysis of 3 different trends
    sample_types = ["declining", "growing", "collapsed"]
    results = []
    
    for sample_type in sample_types:
        metrics = load_sample_data(sample_type)
        result = analyzer.analyze(metrics)
        results.append(result)
    
    # Print summary
    print("\nBatch Analysis Results:\n")
    print(f"{'Trend Name':<20} {'Status':<15} {'Decline Prob':<15} {'Severity':<15}")
    print("-" * 65)
    
    for result in results:
        trend = result['trend_name'][:19]
        status = result['trend_status']
        decline = f"{result['decline_probability']:.0%}"
        severity = result['severity_level']
        print(f"{trend:<20} {status:<15} {decline:<15} {severity:<15}")
    
    print()


def example_9_confidence_threshold():
    """Example 9: Adjust confidence threshold."""
    print("=" * 80)
    print("EXAMPLE 9: Confidence Threshold Impact")
    print("=" * 80)
    
    metrics = load_sample_data("declining")
    
    print("Results with different confidence thresholds:\n")
    
    for threshold in [0.3, 0.5, 0.7]:
        analyzer = TrendAnalyzer(min_confidence_threshold=threshold)
        result = analyzer.analyze(metrics)
        
        print(f"Threshold: {threshold:.0%}")
        print(f"  Causes detected: {len(result['root_causes'])}")
        if result['root_causes']:
            print(f"  Highest confidence: {result['root_causes'][0]['confidence']:.0%}")
        print()


def example_10_recommendations():
    """Example 10: Focus on recommended actions."""
    print("=" * 80)
    print("EXAMPLE 10: Recommended Actions & Strategies")
    print("=" * 80)
    
    analyzer = TrendAnalyzer()
    metrics = load_sample_data("declining")
    result = analyzer.analyze(metrics)
    
    print(f"Trend: {result['trend_name']}")
    print(f"Severity: {result['severity_level']}\n")
    print("Recommended Recovery Actions:\n")
    
    recovery_actions = [a for a in result['recommended_actions'] if a['action_type'] == 'RECOVERY']
    exit_actions = [a for a in result['recommended_actions'] if a['action_type'] == 'EXIT']
    
    if recovery_actions:
        print("🔧 RECOVERY Actions:\n")
        for action in recovery_actions[:3]:
            print(f"[{action['priority']}] {action['description']}")
            print(f"    → Expected Impact: {action['expected_impact']}")
            print(f"    → Timeframe: {action['timeframe']}")
            print(f"    → Target Platforms: {', '.join(action['platforms_targeted'])}")
            print()
    
    if exit_actions:
        print("\n🚪 EXIT Actions:\n")
        for action in exit_actions:
            print(f"[{action['priority']}] {action['description']}")
            print(f"    → Expected Impact: {action['expected_impact']}")
            print()


def example_11_temporal_analysis():
    """Example 11: Track trend changes over time (multi-period analysis)."""
    print("=" * 80)
    print("EXAMPLE 11: Trend Trajectory Over Time (Multi-Period)")
    print("=" * 80)
    
    analyzer = TrendAnalyzer()
    
    # Simulate analyzing same trend at different time periods
    # Week 1: Growing
    metrics_week1 = load_sample_data("growing")
    result_week1 = analyzer.analyze(metrics_week1)
    
    # Week 2: Stable
    metrics_week2 = load_sample_data("declining")  # Simulating transition
    metrics_week2["trend_name"] = result_week1["trend_name"]
    result_week2 = analyzer.analyze(metrics_week2)
    
    # Week 3: Collapsed
    metrics_week3 = load_sample_data("collapsed")
    metrics_week3["trend_name"] = result_week1["trend_name"]
    result_week3 = analyzer.analyze(metrics_week3)
    
    analyses = [result_week1, result_week2, result_week3]
    
    # Analyze trajectory
    trajectory = merge_trend_analyses(analyses)
    
    print(f"Trend: {result_week1['trend_name']}")
    print(f"Analysis Period: {trajectory['total_analyses']} weeks\n")
    
    print("Weekly Progression:")
    for i, result in enumerate(analyses, 1):
        print(f"  Week {i}: {result['trend_status']} (Decline: {result['decline_probability']:.0%})")
    
    print(f"\nTrend Momentum: {trajectory['momentum_direction'].upper()}")
    print(f"Momentum Score: {trajectory['momentum']:.3f}")
    
    if trajectory['emerging_causes']:
        print("\nEmerging Problem Areas:")
        for cause in trajectory['emerging_causes'][:3]:
            print(f"  ⚠️  {cause['cause_type']}: {cause['confidence_change']:+.1%}")
    
    print()


def example_12_json_io():
    """Example 12: Input/Output JSON handling."""
    print("=" * 80)
    print("EXAMPLE 12: JSON Input/Output File Handling")
    print("=" * 80)
    
    from sample_data import save_json_to_file, load_json_from_file
    
    # Save sample data to file
    print("Saving sample data to JSON files...")
    save_json_to_file(SAMPLE_TREND_DATA, "sample_declining.json")
    save_json_to_file(SAMPLE_TREND_GROWING, "sample_growing.json")
    save_json_to_file(SAMPLE_TREND_COLLAPSED, "sample_collapsed.json")
    print("✅ Files saved\n")
    
    # Load and analyze
    print("Loading and analyzing from file...")
    metrics = load_json_from_file("sample_declining.json")
    
    analyzer = TrendAnalyzer()
    result = analyzer.analyze(metrics)
    
    # Save result
    save_json_to_file(result, "analysis_result.json")
    print("✅ Analysis result saved to 'analysis_result.json'\n")
    
    # Display summary
    print(f"Analysis Summary:")
    print(f"  Trend: {result['trend_name']}")
    print(f"  Status: {result['trend_status']}")
    print(f"  Causes: {len(result['root_causes'])}")
    print()


# Main execution
if __name__ == "__main__":
    import sys
    
    examples = {
        "1": ("Basic Analysis", example_1_basic_analysis),
        "2": ("Executive Summary", example_2_executive_summary),
        "3": ("Export Formats", example_3_export_formats),
        "4": ("Growing Trend", example_4_growing_trend),
        "5": ("Collapsed Trend", example_5_collapsed_trend),
        "6": ("Platform Health", example_6_platform_health),
        "7": ("Custom Metrics", example_7_custom_metrics),
        "8": ("Batch Analysis", example_8_batch_analysis),
        "9": ("Confidence Threshold", example_9_confidence_threshold),
        "10": ("Recommendations", example_10_recommendations),
        "11": ("Temporal Analysis", example_11_temporal_analysis),
        "12": ("JSON I/O", example_12_json_io),
    }
    
    if len(sys.argv) > 1:
        # Run specific example
        example_num = sys.argv[1]
        if example_num in examples:
            print(f"\n🚀 Running Example {example_num}: {examples[example_num][0]}\n")
            examples[example_num][1]()
        else:
            print(f"❌ Example {example_num} not found.")
            print(f"Available examples: {', '.join(examples.keys())}")
    else:
        # Run all examples
        print("\n" + "=" * 80)
        print("RUNNING ALL EXAMPLES")
        print("=" * 80 + "\n")
        
        for num, (name, func) in examples.items():
            try:
                func()
            except Exception as e:
                print(f"❌ Error in example {num}: {str(e)}\n")
        
        print("=" * 80)
        print("ALL EXAMPLES COMPLETED")
        print("=" * 80)
        print(f"\nRun specific example with: python examples.py <number>")
        print(f"Example numbers: {', '.join(examples.keys())}")
