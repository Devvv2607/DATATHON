"""
Explanation Templates - Lifecycle-Stage Aware
Maps lifecycle stages to contextual explanation templates
"""

# Explanation templates per lifecycle stage and signal
STAGE_CONTEXT = {
    1: {  # EMERGING
        "stage_name": "Emerging",
        "sensitivity": "Low - Early trends are inherently volatile",
        "signal_templates": {
            "engagement_drop": "Engagement dipped {pct}% - normal volatility during emergence",
            "velocity_decline": "Growth rate slowed to {value} - typical in early phases",
            "creator_decline": "Creator participation declined {pct}% - expected as trend tests market interest",
            "quality_decline": "Content quality declined {pct}% - early content often varies in quality"
        }
    },
    2: {  # VIRAL (Very Sensitive)
        "stage_name": "Viral",
        "sensitivity": "High - Explosive growth phase demands close monitoring",
        "signal_templates": {
            "engagement_drop": "Engagement fell {pct}% - CRITICAL SIGNAL during viral acceleration phase",
            "velocity_decline": "Growth momentum dropped to {value} - suggests peak may be approaching",
            "creator_decline": "Creator exodus of {pct}% - high-profile creators abandoning signals major shift",
            "quality_decline": "Content quality declined {pct}% - quality collapse on viral trends triggers rapid decay"
        }
    },
    3: {  # PLATEAU (Balanced)
        "stage_name": "Plateau",
        "sensitivity": "Medium - Peak has stabilized, watch for decline signals",
        "signal_templates": {
            "engagement_drop": "Engagement declined {pct}% - stabilization may be breaking into decline phase",
            "velocity_decline": "Growth velocity flattened at {value} - consistent with plateau dynamics",
            "creator_decline": "Creator participation dropped {pct}% - some erosion expected at plateau",
            "quality_decline": "Content quality declined {pct}% - plateau trends sensitive to quality shifts"
        }
    },
    4: {  # DECLINE (Forgiving)
        "stage_name": "Decline",
        "sensitivity": "Low - Trend expected to lose momentum; stabilization is positive",
        "signal_templates": {
            "engagement_drop": "Engagement declined {pct}% - acceleration of expected decline pattern",
            "velocity_decline": "Negative growth at {value} - expected during natural decline phase",
            "creator_decline": "Creator exodus of {pct}% - expected as trend loses relevance",
            "quality_decline": "Content quality dropped {pct}% - typical of declining-phase trends"
        }
    },
    5: {  # DEAD (Minimal)
        "stage_name": "Dead",
        "sensitivity": "Very Low - Trend has concluded; minimal signals expected",
        "signal_templates": {
            "engagement_drop": "Engagement at {pct}% of peak - trend has concluded",
            "velocity_decline": "No significant growth {value} - expected for dead trends",
            "creator_decline": "Minimal creator activity {pct}% - trend no longer relevant",
            "quality_decline": "Sparse content {pct}% - few creators still posting"
        }
    }
}

# Risk score interpretation
RISK_INTERPRETATION = {
    "green": {
        "range": "0-30",
        "meaning": "Healthy trend - no immediate decline signals",
        "action": "Monitor regularly"
    },
    "yellow": {
        "range": "30-57",
        "meaning": "Watch closely - early warning signals detected",
        "action": "Increase monitoring frequency"
    },
    "orange": {
        "range": "57-80",
        "meaning": "At risk - multiple decline signals firing",
        "action": "Investigate root causes, consider intervention"
    },
    "red": {
        "range": "80-100",
        "meaning": "Critical - trend in advanced decline",
        "action": "Immediate action required"
    }
}

# Signal importance ranking (for determining which signals to highlight)
SIGNAL_IMPORTANCE = {
    "engagement_drop": 1.0,      # Most important
    "velocity_decline": 0.95,    # Nearly as important
    "creator_decline": 0.85,     # Important
    "quality_decline": 0.80      # Less critical but still relevant
}
