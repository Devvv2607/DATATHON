"""
Business Domain Configuration
Supports multiple business verticals with domain-specific analysis
"""

BUSINESS_DOMAINS = {
    "fashion_retail": {
        "name": "Fashion & Retail",
        "categories": ["Clothing", "Shoes", "Accessories", "Jewelry", "Bags"],
        "metrics": ["sales_volume", "style_virality", "seasonal_demand", "influencer_impact"],
        "trends": ["#SustainableFashion", "#StreetStyle", "#LuxuryFashion"]
    },
    "food_beverage": {
        "name": "Food & Beverage",
        "categories": ["Restaurants", "Food Delivery", "Beverages", "Snacks", "Healthy Food"],
        "metrics": ["order_volume", "taste_rating", "delivery_speed", "price_perception"],
        "trends": ["#FoodTrends", "#HealthyEating", "#VeganFood"]
    },
    "technology": {
        "name": "Technology",
        "categories": ["Software", "Hardware", "AI/ML", "Cloud Services", "Cybersecurity"],
        "metrics": ["adoption_rate", "developer_interest", "market_disruption", "innovation_score"],
        "trends": ["#AIRevolution2026", "#WebThreeDev", "#HealthTech"]
    },
    "beauty_cosmetics": {
        "name": "Beauty & Cosmetics",
        "categories": ["Skincare", "Makeup", "Haircare", "Fragrance", "Wellness"],
        "metrics": ["brand_loyalty", "ingredient_trends", "celebrity_endorsement", "sustainability"],
        "trends": ["#CleanBeauty", "#SkincareRoutine", "#MakeupTrends"]
    },
    "fitness_wellness": {
        "name": "Fitness & Wellness",
        "categories": ["Gyms", "Yoga", "Supplements", "Mental Health", "Wearables"],
        "metrics": ["membership_growth", "engagement_rate", "health_outcomes", "app_downloads"],
        "trends": ["#MindfulLiving", "#FitnessGoals", "#WellnessJourney"]
    },
    "entertainment": {
        "name": "Entertainment",
        "categories": ["Movies", "Music", "Gaming", "Streaming", "Events"],
        "metrics": ["viewership", "viral_potential", "audience_retention", "social_buzz"],
        "trends": ["#MetaverseLife", "#GamingCommunity", "#StreamingWars"]
    },
    "automotive": {
        "name": "Automotive",
        "categories": ["Electric Vehicles", "Luxury Cars", "SUVs", "Auto Parts", "Mobility"],
        "metrics": ["sales_growth", "environmental_impact", "tech_features", "brand_perception"],
        "trends": ["#EVRevolution", "#SustainableTransport", "#AutonomousVehicles"]
    },
    "real_estate": {
        "name": "Real Estate",
        "categories": ["Residential", "Commercial", "Rentals", "Smart Homes", "Co-working"],
        "metrics": ["property_value", "occupancy_rate", "location_desirability", "roi_timeline"],
        "trends": ["#RemoteWork", "#SmartHomes", "#UrbanLiving"]
    },
    "education": {
        "name": "Education",
        "categories": ["Online Learning", "EdTech", "Certifications", "Tutoring", "Skills Training"],
        "metrics": ["enrollment_rate", "completion_rate", "skill_demand", "job_placement"],
        "trends": ["#EdTech", "#LifelongLearning", "#SkillDevelopment"]
    },
    "travel_hospitality": {
        "name": "Travel & Hospitality",
        "categories": ["Hotels", "Airlines", "Tourism", "Experiences", "Travel Tech"],
        "metrics": ["booking_rate", "customer_satisfaction", "seasonal_demand", "destination_popularity"],
        "trends": ["#TravelGoals", "#SustainableTravel", "#WorkFromAnywhere"]
    }
}


def get_domain_specific_content(domain_key: str, trend_data: dict) -> dict:
    """
    Generate domain-specific content analysis
    
    Args:
        domain_key: Key from BUSINESS_DOMAINS
        trend_data: Raw trend data from trend_analysis module
    
    Returns:
        Domain-specific ROI analysis with relevant metrics
    """
    domain = BUSINESS_DOMAINS.get(domain_key, BUSINESS_DOMAINS["technology"])
    
    # Map generic trends to domain-specific insights
    content_items = []
    for category in domain["categories"]:
        # Simulate category-specific content performance
        content_items.append({
            "content_id": f"{domain_key}_{category.lower().replace(' ', '_')}",
            "content_name": f"{category} Campaign",
            "reach": trend_data.get("metrics", {}).get("engagement_rate", 5.0) * 2000,
            "revenue": trend_data.get("metrics", {}).get("viral_coefficient", 1.5) * 1000,
            "cost": 200 + (len(category) * 10),  # Variable cost by category complexity
            "category": category,
            "domain": domain["name"]
        })
    
    return {
        "domain": domain["name"],
        "domain_key": domain_key,
        "categories": domain["categories"],
        "relevant_metrics": domain["metrics"],
        "trending_hashtags": domain["trends"],
        "content_items": content_items
    }
