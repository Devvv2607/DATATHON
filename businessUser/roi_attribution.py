"""
Feature 4: ROI Attribution & Content Performance
Shows which content is profitable and which loses money
"""

import logging

logger = logging.getLogger(__name__)


def analyze_roi(content_items: list) -> dict:
    """
    Analyze ROI for content on the trend.
    
    Args:
        content_items: [
            {
                "content_id": str,
                "content_name": str,
                "reach": int,
                "revenue": float,
                "cost": float
            }
        ]
    
    Returns:
        {
            "roi_analysis": [
                {
                    "content_id": str,
                    "content_name": str,
                    "reach": int,
                    "revenue": float,
                    "cost": float,
                    "net_roi": float,
                    "roi_status": "profitable|breakeven|loss",
                    "roi_percentage": float
                }
            ],
            "summary": {
                "total_revenue": float,
                "total_cost": float,
                "net_profit": float,
                "profitable_count": int,
                "loss_count": int
            }
        }
    """
    try:
        roi_items = []
        total_revenue = 0
        total_cost = 0
        profitable_count = 0
        loss_count = 0
        
        for item in content_items:
            content_id = item.get("content_id", "unknown")
            content_name = item.get("content_name", "")
            reach = item.get("reach", 0)
            revenue = item.get("revenue", 0)
            cost = item.get("cost", 0)
            
            net_roi = revenue - cost
            roi_pct = (net_roi / cost * 100) if cost > 0 else 0
            
            if net_roi > 0:
                roi_status = "profitable"
                profitable_count += 1
            elif net_roi == 0:
                roi_status = "breakeven"
            else:
                roi_status = "loss"
                loss_count += 1
            
            roi_items.append({
                "content_id": content_id,
                "content_name": content_name,
                "reach": reach,
                "revenue": round(revenue, 2),
                "cost": round(cost, 2),
                "net_roi": round(net_roi, 2),
                "roi_status": roi_status,
                "roi_percentage": round(roi_pct, 1)
            })
            
            total_revenue += revenue
            total_cost += cost
        
        net_profit = total_revenue - total_cost
        
        return {
            "roi_analysis": roi_items,
            "summary": {
                "total_revenue": round(total_revenue, 2),
                "total_cost": round(total_cost, 2),
                "net_profit": round(net_profit, 2),
                "profitable_count": profitable_count,
                "loss_count": loss_count
            }
        }
    
    except Exception as e:
        logger.error(f"✗ Error analyzing ROI: {e}")
        return {
            "roi_analysis": [],
            "summary": {
                "total_revenue": 0,
                "total_cost": 0,
                "net_profit": 0,
                "profitable_count": 0,
                "loss_count": 0
            }
        }
