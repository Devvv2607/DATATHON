"""
Risk vs Opportunity Quadrant Chart Generator
Renders visualization-ready data for frontend dashboard
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime


def generate_quadrant_chart(investment_decision: dict, trend_name: str = "Trend"):
    """
    Generate Risk vs Opportunity quadrant chart image.
    
    Args:
        investment_decision: Output from get_investment_decision()
        trend_name: Name of the trend being analyzed
    
    Returns:
        matplotlib figure object
    """
    risk_x = investment_decision["investment_decision"]["risk_x"]
    opportunity_y = investment_decision["investment_decision"]["opportunity_y"]
    quadrant = investment_decision["investment_decision"]["quadrant"]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Set limits and labels
    ax.set_xlim(0, 100)
    ax.set_ylim(-10000, 30000)
    ax.set_xlabel("Risk Score →", fontsize=14, fontweight="bold")
    ax.set_ylabel("Net ROI ($) →", fontsize=14, fontweight="bold")
    ax.set_title(f"Risk vs Opportunity Quadrant\n{trend_name}", 
                 fontsize=16, fontweight="bold", pad=20)
    
    # Add quadrant dividing lines
    ax.axvline(x=57, color="gray", linestyle="--", linewidth=2, alpha=0.5, label="Risk Threshold (57)")
    ax.axhline(y=0, color="gray", linestyle="--", linewidth=2, alpha=0.5, label="Profitability Threshold")
    ax.grid(True, alpha=0.3)
    
    # Add quadrant backgrounds
    # Scale (Low Risk, High ROI) - GREEN
    scale_quad = patches.Rectangle((0, 0), 57, 30000, 
                                   linewidth=2, edgecolor="green", 
                                   facecolor="lightgreen", alpha=0.15)
    ax.add_patch(scale_quad)
    ax.text(28, 25000, "SCALE\n(Low Risk, High ROI)", 
            ha="center", va="top", fontsize=12, fontweight="bold", color="darkgreen")
    
    # Tactical Only (High Risk, High ROI) - YELLOW
    tactical_quad = patches.Rectangle((57, 0), 43, 30000, 
                                      linewidth=2, edgecolor="orange", 
                                      facecolor="lightyellow", alpha=0.15)
    ax.add_patch(tactical_quad)
    ax.text(78, 25000, "TACTICAL ONLY\n(High Risk, High ROI)", 
            ha="center", va="top", fontsize=12, fontweight="bold", color="darkorange")
    
    # Monitor (Low Risk, Low ROI) - BLUE
    monitor_quad = patches.Rectangle((0, -10000), 57, 10000, 
                                     linewidth=2, edgecolor="blue", 
                                     facecolor="lightblue", alpha=0.15)
    ax.add_patch(monitor_quad)
    ax.text(28, -5000, "MONITOR\n(Low Risk, Low ROI)", 
            ha="center", va="center", fontsize=12, fontweight="bold", color="darkblue")
    
    # Exit (High Risk, Low ROI) - RED
    exit_quad = patches.Rectangle((57, -10000), 43, 10000, 
                                  linewidth=2, edgecolor="red", 
                                  facecolor="lightcoral", alpha=0.15)
    ax.add_patch(exit_quad)
    ax.text(78, -5000, "EXIT\n(High Risk, Low ROI)", 
            ha="center", va="center", fontsize=12, fontweight="bold", color="darkred")
    
    # Plot the actual data point
    colors = {
        "scale": "darkgreen",
        "tactical_only": "darkorange",
        "monitor": "darkblue",
        "exit": "darkred"
    }
    color = colors.get(quadrant, "black")
    
    ax.scatter(risk_x, opportunity_y, s=500, color=color, 
              edgecolor="black", linewidth=3, zorder=5, marker="*")
    
    # Add data point label
    ax.annotate(f"Current Position\nRisk: {risk_x}\nROI: ${opportunity_y:,.0f}",
               xy=(risk_x, opportunity_y), 
               xytext=(risk_x + 10, opportunity_y + 3000),
               fontsize=10, fontweight="bold",
               bbox=dict(boxstyle="round,pad=0.5", facecolor=color, alpha=0.3),
               arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0", lw=2))
    
    # Add legend
    ax.legend(loc="lower left", fontsize=10)
    
    # Styling
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    plt.tight_layout()
    return fig


def generate_quadrant_json(investment_decision: dict, trend_name: str = "Trend") -> str:
    """
    Generate JSON-serializable quadrant chart data for frontend.
    Ready for Chart.js, D3.js, or any JavaScript charting library.
    
    Args:
        investment_decision: Output from get_investment_decision()
        trend_name: Name of the trend
    
    Returns:
        JSON string with chart data
    """
    risk_x = investment_decision["investment_decision"]["risk_x"]
    opportunity_y = investment_decision["investment_decision"]["opportunity_y"]
    quadrant = investment_decision["investment_decision"]["quadrant"]
    
    chart_data = {
        "title": f"Risk vs Opportunity: {trend_name}",
        "axes": {
            "x": {
                "label": "Risk Score (0-100)",
                "min": 0,
                "max": 100,
                "threshold": 57,
                "threshold_label": "Risk Caution Level"
            },
            "y": {
                "label": "Net ROI ($)",
                "min": -10000,
                "max": 30000,
                "threshold": 0,
                "threshold_label": "Profitability Threshold"
            }
        },
        "quadrants": {
            "scale": {
                "label": "SCALE",
                "color": "green",
                "description": "Low Risk, High ROI - Scale aggressively",
                "x_min": 0, "x_max": 57,
                "y_min": 0, "y_max": 30000
            },
            "tactical_only": {
                "label": "TACTICAL ONLY",
                "color": "orange",
                "description": "High Risk, High ROI - Use short-term tactics",
                "x_min": 57, "x_max": 100,
                "y_min": 0, "y_max": 30000
            },
            "monitor": {
                "label": "MONITOR",
                "color": "blue",
                "description": "Low Risk, Low ROI - Continue monitoring",
                "x_min": 0, "x_max": 57,
                "y_min": -10000, "y_max": 0
            },
            "exit": {
                "label": "EXIT",
                "color": "red",
                "description": "High Risk, Low ROI - Exit or restructure",
                "x_min": 57, "x_max": 100,
                "y_min": -10000, "y_max": 0
            }
        },
        "data_point": {
            "x": risk_x,
            "y": opportunity_y,
            "quadrant": quadrant,
            "label": f"Current Position: {quadrant.upper()}",
            "color": {
                "scale": "darkgreen",
                "tactical_only": "darkorange",
                "monitor": "darkblue",
                "exit": "darkred"
            }.get(quadrant, "black")
        },
        "generated_at": datetime.now().isoformat(),
        "recommendation": investment_decision["investment_decision"]["recommended_action"].upper()
    }
    
    return json.dumps(chart_data, indent=2)


def generate_quadrant_svg(investment_decision: dict, trend_name: str = "Trend") -> str:
    """
    Generate SVG code for embedding directly in HTML.
    No dependencies needed, pure SVG.
    """
    risk_x = investment_decision["investment_decision"]["risk_x"]
    opportunity_y = investment_decision["investment_decision"]["opportunity_y"]
    quadrant = investment_decision["investment_decision"]["quadrant"]
    
    # Scale data to SVG coordinates (800x600)
    svg_x = (risk_x / 100) * 700 + 50  # 0-100 risk → 50-750 px
    svg_y = 550 - ((opportunity_y + 10000) / 40000) * 500  # -10k to 30k ROI → 50-550 px
    
    color_map = {
        "scale": "#2ecc71",
        "tactical_only": "#f39c12",
        "monitor": "#3498db",
        "exit": "#e74c3c"
    }
    point_color = color_map.get(quadrant, "#000000")
    
    svg = f"""<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .grid-line {{ stroke: #ccc; stroke-width: 1; }}
      .axis {{ stroke: #333; stroke-width: 2; }}
      .axis-label {{ font-size: 14px; font-weight: bold; }}
      .quadrant-label {{ font-size: 12px; font-weight: bold; }}
      .data-point {{ fill: {point_color}; stroke: black; stroke-width: 2; }}
      .tooltip {{ font-size: 11px; }}
    </style>
  </defs>
  
  <!-- Title -->
  <text x="400" y="30" text-anchor="middle" class="axis-label" font-size="18">
    Risk vs Opportunity: {trend_name}
  </text>
  
  <!-- Scale quadrant (Green) -->
  <rect x="50" y="50" width="350" height="300" fill="#d5f4e6" opacity="0.3" stroke="#2ecc71" stroke-width="2"/>
  <text x="225" y="220" text-anchor="middle" class="quadrant-label" fill="#27ae60">
    SCALE
  </text>
  <text x="225" y="235" text-anchor="middle" class="quadrant-label" fill="#27ae60" font-size="10">
    Low Risk, High ROI
  </text>
  
  <!-- Tactical quadrant (Orange) -->
  <rect x="400" y="50" width="350" height="300" fill="#fef5e7" opacity="0.3" stroke="#f39c12" stroke-width="2"/>
  <text x="575" y="220" text-anchor="middle" class="quadrant-label" fill="#e67e22">
    TACTICAL
  </text>
  <text x="575" y="235" text-anchor="middle" class="quadrant-label" fill="#e67e22" font-size="10">
    High Risk, High ROI
  </text>
  
  <!-- Monitor quadrant (Blue) -->
  <rect x="50" y="350" width="350" height="200" fill="#d6eaf8" opacity="0.3" stroke="#3498db" stroke-width="2"/>
  <text x="225" y="465" text-anchor="middle" class="quadrant-label" fill="#2980b9">
    MONITOR
  </text>
  <text x="225" y="480" text-anchor="middle" class="quadrant-label" fill="#2980b9" font-size="10">
    Low Risk, Low ROI
  </text>
  
  <!-- Exit quadrant (Red) -->
  <rect x="400" y="350" width="350" height="200" fill="#fadbd8" opacity="0.3" stroke="#e74c3c" stroke-width="2"/>
  <text x="575" y="465" text-anchor="middle" class="quadrant-label" fill="#c0392b">
    EXIT
  </text>
  <text x="575" y="480" text-anchor="middle" class="quadrant-label" fill="#c0392b" font-size="10">
    High Risk, Low ROI
  </text>
  
  <!-- Axes -->
  <line x1="50" y1="350" x2="750" y2="350" class="axis"/>
  <line x1="400" y1="50" x2="400" y2="550" class="axis"/>
  
  <!-- Grid lines at thresholds -->
  <line x1="400" y1="50" x2="400" y2="550" class="grid-line" stroke="#f39c12" stroke-width="2" stroke-dasharray="5,5"/>
  <line x1="50" y1="350" x2="750" y2="350" class="grid-line" stroke="#f39c12" stroke-width="2" stroke-dasharray="5,5"/>
  
  <!-- Axis labels -->
  <text x="750" y="375" class="axis-label" font-size="12">Risk Score (0-100) →</text>
  <text x="25" y="50" class="axis-label" font-size="12">ROI ($) ↑</text>
  
  <!-- Scale markers -->
  <text x="40" y="555" font-size="10" text-anchor="end">0</text>
  <text x="750" y="555" font-size="10" text-anchor="start">100</text>
  <text x="40" y="360" font-size="10" text-anchor="end">$0</text>
  <text x="40" y="55" font-size="10" text-anchor="end">$30k</text>
  
  <!-- Data point -->
  <circle cx="{svg_x}" cy="{svg_y}" r="8" class="data-point"/>
  
  <!-- Data point tooltip -->
  <rect x="{svg_x + 15}" y="{svg_y - 30}" width="120" height="50" fill="white" stroke="black" stroke-width="1" rx="5"/>
  <text x="{svg_x + 75}" y="{svg_y - 15}" text-anchor="middle" class="tooltip" font-weight="bold">
    CURRENT
  </text>
  <text x="{svg_x + 75}" y="{svg_y + 0}" text-anchor="middle" class="tooltip">
    Risk: {risk_x}
  </text>
  <text x="{svg_x + 75}" y="{svg_y + 15}" text-anchor="middle" class="tooltip">
    ROI: ${opportunity_y:,.0f}
  </text>
</svg>"""
    
    return svg


if __name__ == "__main__":
    # Example usage
    example_investment = {
        "investment_decision": {
            "recommended_action": "tactical_only",
            "rationale": "High risk but profitable",
            "quadrant": "tactical_only",
            "risk_x": 72.5,
            "opportunity_y": 5600
        }
    }
    
    # Generate static image
    fig = generate_quadrant_chart(example_investment, "Example Trend")
    fig.savefig("quadrant_chart.png", dpi=150, bbox_inches="tight")
    print("✓ Saved: quadrant_chart.png")
    
    # Generate JSON for frontend
    json_data = generate_quadrant_json(example_investment, "Example Trend")
    with open("quadrant_chart.json", "w") as f:
        f.write(json_data)
    print("✓ Saved: quadrant_chart.json")
    
    # Generate SVG for embedding
    svg_code = generate_quadrant_svg(example_investment, "Example Trend")
    with open("quadrant_chart.svg", "w") as f:
        f.write(svg_code)
    print("✓ Saved: quadrant_chart.svg")
    
    print("\nVisualization files generated:")
    print("  1. quadrant_chart.png - Static image")
    print("  2. quadrant_chart.json - Data for JavaScript charts")
    print("  3. quadrant_chart.svg - Embeddable vector graphic")
