"""
Visualization Generation Module
Converts feature outputs to chart-ready JSON formats for frontend rendering
"""

import json


def generate_signal_contribution_chart(signal_breakdown: dict, title: str = "Signal Contributions") -> dict:
    """
    Convert signal breakdown to stacked bar chart JSON format.
    
    Args:
        signal_breakdown: Dict with signal scores
        title: Chart title
    
    Returns:
        Chart.js compatible JSON object
    """
    try:
        signals = []
        values = []
        colors = ["#FF6B6B", "#FFA500", "#FFD93D", "#6BCB77"]
        
        for i, (signal, value) in enumerate(signal_breakdown.items()):
            signals.append(signal.replace("_", " ").title())
            values.append(float(value))
        
        return {
            "type": "bar",
            "title": title,
            "labels": signals,
            "datasets": [
                {
                    "label": "Signal Score",
                    "data": values,
                    "backgroundColor": colors[:len(signals)],
                    "borderColor": "#333",
                    "borderWidth": 1
                }
            ],
            "options": {
                "responsive": True,
                "scales": {
                    "y": {
                        "min": 0,
                        "max": 100,
                        "title": {"display": True, "text": "Signal Score"}
                    }
                }
            }
        }
    except Exception as e:
        return {"error": str(e)}


def generate_countdown_visualization(days_remaining: int, window_stage: str) -> dict:
    """
    Convert decline window to countdown visualization.
    
    Args:
        days_remaining: Days until critical
        window_stage: "urgent" | "warning" | "stable"
    
    Returns:
        Countdown visualization JSON
    """
    try:
        color_map = {
            "urgent": "#FF6B6B",
            "warning": "#FFA500",
            "stable": "#6BCB77"
        }
        
        return {
            "type": "countdown",
            "days": max(0, days_remaining),
            "stage": window_stage,
            "color": color_map.get(window_stage, "#666"),
            "trend_arrow": "↓" if window_stage == "urgent" else "→",
            "urgency_level": 100 if window_stage == "urgent" else (60 if window_stage == "warning" else 20),
            "visual_progress_bar": {
                "current": max(0, 100 - (days_remaining * 15)),
                "max": 100,
                "label": f"{days_remaining} days remaining"
            }
        }
    except Exception as e:
        return {"error": str(e)}


def generate_timeline_visualization(campaigns: list, stage: str) -> dict:
    """
    Convert campaign timing to timeline visualization.
    
    Args:
        campaigns: List of campaign recommendations
        stage: Lifecycle stage (1-5)
    
    Returns:
        Timeline visualization JSON
    """
    try:
        stage_names = {
            1: "Emerging (48-72h)",
            2: "Viral (24-48h)",
            3: "Plateau (24-48h)",
            4: "Decline (12-24h)",
            5: "Dead (inactive)"
        }
        
        timeline_items = []
        for i, campaign in enumerate(campaigns):
            timeline_items.append({
                "phase": i + 1,
                "title": campaign if isinstance(campaign, str) else campaign.get("title", f"Phase {i+1}"),
                "duration_hours": 24 + (i * 12),
                "status": "active" if i == 0 else "planned"
            })
        
        return {
            "type": "timeline",
            "stage": stage_names.get(stage, f"Stage {stage}"),
            "phases": timeline_items,
            "total_duration_hours": sum(item["duration_hours"] for item in timeline_items),
            "visual_width_percent": (len(timeline_items) * 20) + 20
        }
    except Exception as e:
        return {"error": str(e)}


def generate_alternative_trends_chart(alternatives: list) -> dict:
    """
    Convert alternative trends to comparison chart JSON.
    
    Args:
        alternatives: List of alternative trend options
    
    Returns:
        Comparison chart JSON
    """
    try:
        keywords = []
        growth_rates = []
        revenues = []
        relevance_scores = []
        difficulty_map = {"low": 1, "medium": 2, "high": 3}
        
        for alt in alternatives[:5]:
            keywords.append(alt.get("keyword", "")[:20])
            growth_rates.append(alt.get("growth_rate", 0))
            revenues.append(alt.get("estimated_monthly_revenue", 0) / 1000)  # Convert to thousands
            relevance_scores.append(alt.get("relevance_score", 0))
        
        return {
            "type": "bubble",
            "title": "Alternative Trends Comparison",
            "datasets": [
                {
                    "label": f"{kw} (Growth: {gr}%)",
                    "data": [{
                        "x": relevance_scores[i],
                        "y": growth_rates[i],
                        "r": revenues[i] / 2
                    }],
                    "backgroundColor": f"rgba({100 + i*30}, {150 - i*20}, 200, 0.6)"
                }
                for i, kw in enumerate(keywords)
            ],
            "options": {
                "scales": {
                    "x": {"title": "Relevance Score (0-100)"},
                    "y": {"title": "Growth Rate (%)"}
                }
            }
        }
    except Exception as e:
        return {"error": str(e)}


def generate_quadrant_chart(risk_x: float, opportunity_y: float) -> dict:
    """
    Convert investment decision to quadrant visualization (for existing investment_decision feature).
    
    Args:
        risk_x: Risk score (0-100)
        opportunity_y: ROI/Opportunity score
    
    Returns:
        Quadrant chart JSON
    """
    try:
        quadrants = {
            "low_risk_high_roi": {"name": "SCALE", "color": "#6BCB77", "icon": "📈"},
            "high_risk_high_roi": {"name": "TACTICAL ONLY", "color": "#FFD93D", "icon": "⚡"},
            "low_risk_low_roi": {"name": "MONITOR", "color": "#4ECDC4", "icon": "👁"},
            "high_risk_low_roi": {"name": "EXIT", "color": "#FF6B6B", "icon": "❌"}
        }
        
        current_quadrant = "low_risk_low_roi"
        if risk_x < 50 and opportunity_y > 0:
            current_quadrant = "low_risk_high_roi"
        elif risk_x >= 50 and opportunity_y > 0:
            current_quadrant = "high_risk_high_roi"
        elif risk_x >= 50 and opportunity_y <= 0:
            current_quadrant = "high_risk_low_roi"
        
        return {
            "type": "quadrant",
            "current_position": current_quadrant,
            "x_axis": "Risk Level",
            "y_axis": "Opportunity (ROI)",
            "data_point": {"x": risk_x, "y": opportunity_y},
            "quadrants": quadrants,
            "recommendation": quadrants[current_quadrant]["name"],
            "recommendation_icon": quadrants[current_quadrant]["icon"],
            "recommendation_color": quadrants[current_quadrant]["color"]
        }
    except Exception as e:
        return {"error": str(e)}


def generate_pivot_roadmap(key_actions: list, timeline_months: int, priority_level: str) -> dict:
    """
    Convert pivot strategy to Gantt-style roadmap visualization.
    
    Args:
        key_actions: List of strategic actions
        timeline_months: Timeline in months
        priority_level: Priority level
    
    Returns:
        Roadmap visualization JSON
    """
    try:
        priority_colors = {
            "URGENT": "#FF6B6B",
            "HIGH": "#FFA500",
            "MEDIUM": "#FFD93D",
            "LOW": "#6BCB77"
        }
        
        roadmap_phases = []
        days_per_action = (timeline_months * 30) // max(len(key_actions), 1)
        
        for i, action in enumerate(key_actions):
            roadmap_phases.append({
                "phase": i + 1,
                "title": action[:50],
                "start_day": i * days_per_action,
                "duration_days": days_per_action,
                "status": "active" if i == 0 else "planned",
                "owner": "Product Team"
            })
        
        return {
            "type": "roadmap",
            "title": "Pivot Strategy Roadmap",
            "timeline_months": timeline_months,
            "priority": priority_level,
            "priority_color": priority_colors.get(priority_level, "#666"),
            "phases": roadmap_phases,
            "total_duration_days": timeline_months * 30
        }
    except Exception as e:
        return {"error": str(e)}
