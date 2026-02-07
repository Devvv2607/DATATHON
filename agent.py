"""
Creative Recovery & Growth Agent
Main orchestrator for content generation based on trend alerts
"""

import os
import json
from typing import Dict, Any, List
from dotenv import load_dotenv
from groq_integration import GroqContentGenerator
from trends_integration import TrendsAnalyzer

# Load environment variables
load_dotenv()

class CreativeRecoveryAgent:
    """
    Creative Recovery & Growth Agent for social media trends
    Operates in COMEBACK MODE (red/orange) and GROWTH MODE (green/yellow)
    """
    
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")
        
        self.groq_gen = GroqContentGenerator(api_key)
        self.trends_analyzer = TrendsAnalyzer(groq_api_key=api_key)
    
    def process_trend_alert(
        self,
        trend_name: str,
        alert_level: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Process trend alert and generate strategic content
        
        Args:
            trend_name: Name of the trend
            alert_level: "red", "orange", "yellow", or "green"
            context: Additional context (decline_drivers, opportunities, etc.)
        
        Returns:
            Structured JSON with content ideas
        """
        
        if alert_level not in ["red", "orange", "yellow", "green"]:
            raise ValueError("alert_level must be: red, orange, yellow, or green")
        
        # Get trend analysis
        try:
            trend_analysis = self.trends_analyzer.analyze_trend(trend_name)
            related_topics = trend_analysis.get("related_topics", [])
        except Exception as e:
            print(f"Warning: Could not fetch live trends: {e}")
            related_topics = []
        
        # Determine mode
        is_comeback_mode = alert_level in ["red", "orange"]
        
        result = {
            "trend_name": trend_name,
            "alert_level": alert_level,
            "mode": "COMEBACK MODE" if is_comeback_mode else "GROWTH MODE",
            "generated_at": "2026-02-07",
        }
        
        if is_comeback_mode:
            # COMEBACK MODE
            decline_drivers = context.get("decline_drivers", [
                "audience fatigue",
                "market saturation",
                "trend decay"
            ]) if context else ["audience fatigue", "market saturation", "trend decay"]
            
            content = self.groq_gen.generate_comeback_content(
                trend_name=trend_name,
                decline_drivers=decline_drivers,
                related_topics=related_topics or ["comeback", "revival", "nostalgia"]
            )
            
            result.update({
                "decline_drivers": decline_drivers,
                "content_strategy": "Revive interest with fresh angles and audience re-engagement",
                "content": content
            })
        
        else:
            # GROWTH MODE
            growth_opportunities = context.get("growth_opportunities", [
                "emerging audience segment",
                "new platform traction",
                "cross-niche potential"
            ]) if context else ["emerging audience segment", "new platform traction", "cross-niche potential"]
            
            content = self.groq_gen.generate_growth_content(
                trend_name=trend_name,
                growth_opportunities=growth_opportunities,
                related_topics=related_topics or ["growth", "expansion", "scaling"]
            )
            
            result.update({
                "growth_opportunities": growth_opportunities,
                "content_strategy": "Accelerate growth with strategic reach expansion",
                "content": content
            })
        
        return result
    
    def generate_report(self, alert_data: Dict[str, Any]) -> str:
        """
        Generate a readable report from processed trend alert
        """
        report = f"""
╔════════════════════════════════════════════════════════════════╗
║           CREATIVE RECOVERY & GROWTH STRATEGY REPORT            ║
╚════════════════════════════════════════════════════════════════╝

TREND: {alert_data.get('trend_name', 'Unknown')}
ALERT LEVEL: {alert_data.get('alert_level', 'Unknown').upper()}
MODE: {alert_data.get('mode', 'Unknown')}
GENERATED: {alert_data.get('generated_at', 'Unknown')}

────────────────────────────────────────────────────────────────

{json.dumps(alert_data.get('content', {}), indent=2)}

────────────────────────────────────────────────────────────────
"""
        return report


def main():
    """Test the agent with dummy scenarios"""
    
    agent = CreativeRecoveryAgent()
    
    # Test Scenario 1: COMEBACK MODE (red alert)
    print("\n" + "="*70)
    print("TEST 1: COMEBACK MODE - Trending Format Decline")
    print("="*70)
    
    comeback_alert = agent.process_trend_alert(
        trend_name="Dance Challenge Format",
        alert_level="red",
        context={
            "decline_drivers": [
                "Over-saturation of dance trends",
                "Audience fatigue with repetitive moves",
                "Algorithm deprioritizing format"
            ]
        }
    )
    
    print(agent.generate_report(comeback_alert))
    print("\nRaw JSON:")
    print(json.dumps(comeback_alert, indent=2))
    
    # Test Scenario 2: GROWTH MODE (green alert)
    print("\n" + "="*70)
    print("TEST 2: GROWTH MODE - AI Meme Trend Rising")
    print("="*70)
    
    growth_alert = agent.process_trend_alert(
        trend_name="AI Meme",
        alert_level="green",
        context={
            "growth_opportunities": [
                "Untapped Gen Z audience segment",
                "Cross-platform virality potential",
                "Meme culture meets AI discussion"
            ]
        }
    )
    
    print(agent.generate_report(growth_alert))
    print("\nRaw JSON:")
    print(json.dumps(growth_alert, indent=2))
    
    # Test Scenario 3: COMEBACK MODE (orange alert)
    print("\n" + "="*70)
    print("TEST 3: COMEBACK MODE - Underperforming Shorts")
    print("="*70)
    
    orange_alert = agent.process_trend_alert(
        trend_name="Motivational Shorts",
        alert_level="orange",
        context={
            "decline_drivers": [
                "Overused motivational tropes",
                "Audience skepticism toward generic inspiration",
                "CTR dropping 25% MoM"
            ]
        }
    )
    
    print(agent.generate_report(orange_alert))
    print("\nRaw JSON:")
    print(json.dumps(orange_alert, indent=2))
    
    # Test Scenario 4: GROWTH MODE (yellow alert)
    print("\n" + "="*70)
    print("TEST 4: GROWTH MODE - Niche Gaming Trend Emerging")
    print("="*70)
    
    yellow_alert = agent.process_trend_alert(
        trend_name="Retro Gaming Nostalgia",
        alert_level="yellow",
        context={
            "growth_opportunities": [
                "Millennial audience engagement surge",
                "Nostalgia content performing above average",
                "Opportunity for collabs with gaming creators"
            ]
        }
    )
    
    print(agent.generate_report(yellow_alert))
    print("\nRaw JSON:")
    print(json.dumps(yellow_alert, indent=2))


if __name__ == "__main__":
    main()
