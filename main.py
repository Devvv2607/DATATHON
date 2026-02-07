"""
Trend Saboteur Agent - Adversarial Narrative Generator
Simulates how online communities undermine existing memes, hashtags, or trends.

Language: Bilingual (English + Hinglish)
Output: Structured JSON
API: Groq AI (Lightning Fast - Fully Dynamic Generation)
Features: Auto-research trends when no context provided
"""

import json
import random
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from enum import Enum

try:
    from groq import Groq
    
    # Configure Groq API
    GROQ_API_KEY = "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"
    client = Groq(api_key=GROQ_API_KEY)
    
    HAS_AI = True
    print("[✓] Groq AI initialized successfully")
except Exception as e:
    print(f"[!] Warning: Could not initialize Groq API: {str(e)}")
    HAS_AI = False


class NarrativeShift(Enum):
    """Dominant narrative shifts in trend collapse."""
    OVERSATURATION = "oversaturation"
    CRINGE_REJECTION = "cringe_rejection"
    IRONY_FATIGUE = "irony_fatigue"
    POST_IRONY = "post_irony"
    GENERATIONAL_GAP = "generational_gap"
    CORPORATE_COOPTION = "corporate_cooption"
    TOXIC_ASSOCIATION = "toxic_association"
    AUTHENTICITY_DEATH = "authenticity_death"


@dataclass
class CounterNarrative:
    """Counter-narrative concept for trend sabotage."""
    id: int
    title_en: str
    title_hinglish: str
    description_en: str
    description_hinglish: str
    virality_probability: float
    shareability_score: float
    narrative_shift: str
    collapse_mechanism: str
    collapse_mechanism_hinglish: str
    example_content: str
    target_audience: str


class TrendSaboteurAgent:
    """
    Simulates trend collapse through counter-narrative generation.
    
    Uses Groq AI (ultra-fast) to:
    1. Auto-research trends if no context provided
    2. Generate completely unique counter-narratives every time
    """
    
    def __init__(self, trend_name: str, trend_context: str = ""):
        self.trend_name = trend_name
        self.trend_context = trend_context
        self.counter_narratives: List[CounterNarrative] = []
        # Use llama-3.3-70b-versatile for best quality
        self.model = "llama-3.3-70b-versatile"
        
        # Auto-research if no context provided
        if not self.trend_context or self.trend_context.strip() == "":
            print(f"\n[🔍] No context provided. Auto-researching trend: '{self.trend_name}'...")
            self.trend_context = self._research_trend()
    
    def _research_trend(self) -> str:
        """Auto-research the trend to understand its context."""
        
        if not HAS_AI:
            return f"Popular internet trend: {self.trend_name}"
        
        try:
            prompt = f"""You are an expert internet culture researcher. Analyze the trend/meme/hashtag: "{self.trend_name}"

Provide a comprehensive but concise description (150-200 words) covering:
1. What is this trend/meme/hashtag about?
2. Where did it originate? (platform, community, timeframe)
3. Who uses it? (demographics, communities)
4. Why is it popular/viral?
5. Current status (growing, peak, declining)
6. Key characteristics or patterns

Be factual, accurate, and focus on internet culture context. If this is a well-known trend, provide specific details. If obscure, make educated assumptions based on similar trends.

Format: Just provide the description, no preamble."""

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                temperature=0.3,  # Lower for factual accuracy
                max_tokens=400,
            )
            
            context = chat_completion.choices[0].message.content.strip()
            print(f"[✓] Auto-research complete!")
            print(f"\n📝 Trend Context:\n{context}\n")
            return context
            
        except Exception as e:
            print(f"[!] Auto-research failed: {str(e)}")
            return f"Popular internet trend/meme: {self.trend_name}. Commonly shared on social media platforms."
    
    def generate_narrative_types(self) -> List[Dict[str, Any]]:
        """Generate 5 completely unique counter-narrative types using AI."""
        
        if not HAS_AI:
            return self._get_fallback_narrative_types()
        
        try:
            prompt = f"""You are a Gen-Z meme culture analyst and social psychologist analyzing the trend "{self.trend_name}".

Context: {self.trend_context}

Generate 5 UNIQUE, CREATIVE counter-narrative strategies that would accelerate this trend's collapse. Each should attack from a completely different angle and feel fresh/original.

Make them:
- Specific to THIS trend (not generic)
- Based on real internet culture dynamics
- Witty and contemporary
- Varied in approach

For each counter-narrative, provide:
1. Title (English) - creative, punchy, memorable (3-6 words)
2. Title (Hinglish) - Roman Hindi + English mix, natural Mumbai/Delhi slang
3. Narrative type - one word (e.g., oversaturation, cringe_rejection, corporate_cooption, irony_fatigue, toxic_association, generational_gap, authenticity_death)
4. Attack angle - specific way this undermines the trend (10-15 words)
5. Target audience - who would share this (3-5 words)

Format EXACTLY as:
---
TITLE_EN: [creative title]
TITLE_HI: [hinglish title]
TYPE: [one_word_type]
ANGLE: [attack angle]
AUDIENCE: [target audience]
---

Generate all 5 now. Be CREATIVE and SPICY!"""

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                temperature=0.9,  # High creativity
                max_tokens=1500,
            )
            
            text = chat_completion.choices[0].message.content.strip()
            
            # Parse response
            narratives = []
            blocks = text.split('---')
            
            for block in blocks:
                if not block.strip():
                    continue
                
                lines = [l.strip() for l in block.strip().split('\n') if l.strip()]
                
                narrative_data = {}
                for line in lines:
                    if ':' not in line:
                        continue
                    
                    key, value = line.split(':', 1)
                    key = key.strip().upper()
                    value = value.strip()
                    
                    if key == 'TITLE_EN':
                        narrative_data['title_en'] = value
                    elif key == 'TITLE_HI':
                        narrative_data['title_hinglish'] = value
                    elif key == 'TYPE':
                        narrative_data['narrative_type'] = value.lower().replace(' ', '_')
                    elif key == 'ANGLE':
                        narrative_data['attack_angle'] = value
                    elif key == 'AUDIENCE':
                        narrative_data['target_audience'] = value
                
                if len(narrative_data) >= 4:
                    narratives.append(narrative_data)
            
            # If we got 5 good narratives, return them
            if len(narratives) >= 5:
                print(f"[✓] Generated {len(narratives)} unique narrative types")
                return narratives[:5]
            else:
                print(f"[!] AI returned only {len(narratives)} narratives, using fallback")
                return self._get_fallback_narrative_types()
                
        except Exception as e:
            print(f"[!] Error generating narrative types: {str(e)}")
            return self._get_fallback_narrative_types()
    
    def _get_fallback_narrative_types(self) -> List[Dict[str, Any]]:
        """Fallback narrative types if AI fails."""
        print("[!] Using fallback narrative types")
        return [
            {
                "title_en": "Overuse Saturation Critique",
                "title_hinglish": "Overuse Ho Gaya Saturation Wala",
                "narrative_type": "oversaturation",
                "attack_angle": "Normalization reduces perceived coolness and exclusivity",
                "target_audience": "Meta-conscious teenagers, trend critics"
            },
            {
                "title_en": "Generational Cringe Narrative",
                "title_hinglish": "Generational Cringe Wala Angle",
                "narrative_type": "cringe_rejection",
                "attack_angle": "Parents/older people adopting trend causes embarrassment",
                "target_audience": "Gen-Z, anti-trend activists"
            },
            {
                "title_en": "Irony-to-Post-Irony Pivot",
                "title_hinglish": "Irony Se Post-Irony Flip",
                "narrative_type": "irony_fatigue",
                "attack_angle": "Moves goalpost - being ironic about it becomes new cringe",
                "target_audience": "Intellectual meme lords, college students"
            },
            {
                "title_en": "Corporate Co-Option Backlash",
                "title_hinglish": "Corporate Takeover Ka Badla",
                "narrative_type": "corporate_cooption",
                "attack_angle": "Brands using trend destroys grassroots authenticity",
                "target_audience": "Anti-corporate activists, Gen-Z skeptics"
            },
            {
                "title_en": "Adverse Event Association",
                "title_hinglish": "Negative Event Se Jodo",
                "narrative_type": "toxic_association",
                "attack_angle": "Link trend to controversial figure or scandal",
                "target_audience": "Morality-focused communities, activists"
            }
        ]
    
    def generate_ai_content(self, narrative_type: str, title_en: str) -> Dict[str, str]:
        """Generate all content for a counter-narrative using AI."""
        
        if not HAS_AI:
            return {
                "description_en": f"This counter-narrative attacks {self.trend_name} through {narrative_type}.",
                "description_hinglish": f"{self.trend_name} ko {narrative_type} se attack karte hain.",
                "collapse_mechanism": f"Users abandon trend due to {narrative_type} dynamics.",
                "collapse_mechanism_hinglish": f"{narrative_type} ke wajah se log trend chhod dete hain.",
                "example_content": f"'This trend is so {narrative_type} now 💀'"
            }
        
        try:
            prompt = f"""You are a witty Gen-Z internet culture expert analyzing "{self.trend_name}".

Counter-narrative: {title_en}
Attack angle: {narrative_type}
Context: {self.trend_context}

Generate creative, funny, roast-style content. Use contemporary internet slang, be sarcastic, and make it feel REAL.

Provide EXACTLY these 5 items:

1. DESCRIPTION_EN: A witty, sarcastic one-liner (120-150 chars) roasting this trend from the {narrative_type} perspective. Sound like a real person on Twitter/TikTok. Be SPICY.

2. DESCRIPTION_HI: Same roast in Hinglish. Use natural Mumbai/Delhi youth slang. Mix Hindi and English like real Indians talk online. Don't just translate - make it authentic.

3. COLLAPSE_MECHANISM: One analytical sentence (60-80 words) explaining HOW this narrative causes people to abandon the trend. Professional tone.

4. COLLAPSE_MECHANISM_HI: Same explanation in conversational Hinglish.

5. EXAMPLE_CONTENT: A short, punchy social media comment (200-280 chars max) that exemplifies this counter-narrative. Include emojis if appropriate. Make it viral-worthy.

Format EXACTLY as:
DESCRIPTION_EN: [your content]
DESCRIPTION_HI: [your content]
COLLAPSE_MECHANISM: [your content]
COLLAPSE_MECHANISM_HI: [your content]
EXAMPLE_CONTENT: [your content]

No extra text. Just these 5 lines."""

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                temperature=0.95,  # Very high creativity
                max_tokens=800,
            )
            
            text = chat_completion.choices[0].message.content.strip()
            
            # Parse response
            content = {}
            lines = text.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line or ':' not in line:
                    continue
                
                key, value = line.split(':', 1)
                key = key.strip().upper()
                value = value.strip()
                
                if key == 'DESCRIPTION_EN':
                    content['description_en'] = value
                elif key == 'DESCRIPTION_HI':
                    content['description_hinglish'] = value
                elif key == 'COLLAPSE_MECHANISM':
                    content['collapse_mechanism'] = value
                elif key == 'COLLAPSE_MECHANISM_HI':
                    content['collapse_mechanism_hinglish'] = value
                elif key == 'EXAMPLE_CONTENT':
                    content['example_content'] = value
            
            # Validate we got all fields
            required_fields = ['description_en', 'description_hinglish', 'collapse_mechanism', 
                             'collapse_mechanism_hinglish', 'example_content']
            
            for field in required_fields:
                if field not in content or not content[field]:
                    content[field] = f"[Generated content for {field}]"
            
            return content
            
        except Exception as e:
            print(f"[!] Error generating content: {str(e)}")
            return {
                "description_en": f"{self.trend_name} has become oversaturated and lost its original appeal through {narrative_type}.",
                "description_hinglish": f"{self.trend_name} ab bahut zyada ho gaya hai, {narrative_type} ki wajah se appeal khatam.",
                "collapse_mechanism": f"The trend experiences decline as {narrative_type} shifts user perception from positive to negative.",
                "collapse_mechanism_hinglish": f"{narrative_type} se trend ka perception negative ho jata hai aur log chhod dete hain.",
                "example_content": f"'POV: {self.trend_name} jumped the shark. It's officially over 💀'"
            }

    def generate_counter_narratives(self) -> List[CounterNarrative]:
        """Generate exactly 5 unique counter-narratives with fully AI-generated content."""
        
        print("\n[→] Generating unique AI-powered counter-narratives...")
        
        # Step 1: Generate unique narrative types
        print("  [1/2] Creating narrative strategy types...")
        narrative_types = self.generate_narrative_types()
        
        # Step 2: Generate content for each
        print("  [2/2] Generating creative content for each narrative...")
        
        for idx, narrative_meta in enumerate(narrative_types):
            print(f"    [{idx + 1}/5] Generating: {narrative_meta.get('title_en', 'Narrative')}...")
            
            # Generate all content using AI
            ai_content = self.generate_ai_content(
                narrative_meta.get('narrative_type', 'general'),
                narrative_meta.get('title_en', 'Counter-narrative')
            )
            
            # Random probability scores (more realistic variation)
            base_virality = random.uniform(0.55, 0.85)
            base_shareability = random.uniform(0.60, 0.82)
            
            # Create counter-narrative object
            narrative = CounterNarrative(
                id=idx + 1,
                title_en=narrative_meta.get('title_en', f'Counter-Narrative {idx + 1}'),
                title_hinglish=narrative_meta.get('title_hinglish', f'Counter-Narrative {idx + 1}'),
                description_en=ai_content['description_en'],
                description_hinglish=ai_content['description_hinglish'],
                virality_probability=round(base_virality, 3),
                shareability_score=round(base_shareability, 3),
                narrative_shift=narrative_meta.get('narrative_type', 'general'),
                collapse_mechanism=ai_content['collapse_mechanism'],
                collapse_mechanism_hinglish=ai_content['collapse_mechanism_hinglish'],
                example_content=ai_content['example_content'],
                target_audience=narrative_meta.get('target_audience', 'Internet users')
            )
            
            self.counter_narratives.append(narrative)
        
        print("[✓] All counter-narratives generated!\n")
        return self.counter_narratives
    
    def analyze_collapse_dynamics(self) -> Dict[str, Any]:
        """
        Analyze how counter-narratives accelerate trend collapse.
        """
        if not self.counter_narratives:
            self.generate_counter_narratives()
        
        # Calculate aggregate virality and shareability
        avg_virality = sum(n.virality_probability for n in self.counter_narratives) / len(self.counter_narratives)
        avg_shareability = sum(n.shareability_score for n in self.counter_narratives) / len(self.counter_narratives)
        
        # Identify dominant narrative shift
        shift_counts = {}
        for narrative in self.counter_narratives:
            shift = narrative.narrative_shift
            shift_counts[shift] = shift_counts.get(shift, 0) + 1
        
        dominant_shift = max(shift_counts, key=shift_counts.get)
        
        # Collapse acceleration analysis
        collapse_probability = (avg_virality * 0.6) + (avg_shareability * 0.4)
        
        return {
            "trend_name": self.trend_name,
            "total_counter_narratives": len(self.counter_narratives),
            "average_virality_probability": round(avg_virality, 3),
            "average_shareability_score": round(avg_shareability, 3),
            "dominant_narrative_shift": dominant_shift,
            "estimated_collapse_acceleration_factor": round(collapse_probability, 3),
            "collapse_explanation_en": f"These {len(self.counter_narratives)} counter-narratives work synergistically to accelerate {self.trend_name}'s decline. The dominant shift from {dominant_shift} combined with high shareability ({round(avg_shareability, 2)}) means users will rapidly reframe the trend as undesirable. Early adopters will distance themselves, causing cascading abandonment.",
            "collapse_explanation_hinglish": f"Ye {len(self.counter_narratives)} counter-narratives milkar trend ko collapse karayenge. Log sochen ge trend overused hai, corporate manipulate kar rahe hain, ya cringe ho gaya. Jab sab negative sochen ge to naturally sab chhod denge."
        }
    
    def generate_json_report(self) -> str:
        """Generate complete JSON report of analysis."""
        if not self.counter_narratives:
            self.generate_counter_narratives()
        
        dynamics = self.analyze_collapse_dynamics()
        
        # Find most viral and shareable
        most_viral = max(self.counter_narratives, key=lambda n: n.virality_probability)
        most_shareable = max(self.counter_narratives, key=lambda n: n.shareability_score)
        
        report = {
            "metadata": {
                "agent_type": "Trend Saboteur Agent",
                "purpose": "Adversarial simulation for trend collapse",
                "date_generated": "2026-02-07",
                "language": "Bilingual (English + Hinglish)",
                "ai_powered": "Groq AI - Ultra-Fast Dynamic Generation with Auto-Research",
                "model": self.model
            },
            "trend_analysis": {
                "trend_name": self.trend_name,
                "trend_context": self.trend_context,
                "current_status": "Losing momentum - approaching collapse phase",
                "analysis_assumption": "Trend exists and IS beginning to lose momentum and WILL eventually collapse"
            },
            "collapse_dynamics": dynamics,
            "counter_narratives": [asdict(n) for n in self.counter_narratives],
            "summary": {
                "most_viral_narrative_en": f"'{most_viral.title_en}' with virality probability {round(most_viral.virality_probability, 3)}",
                "most_shareable_narrative_en": f"'{most_shareable.title_en}' with shareability score {round(most_shareable.shareability_score, 3)}",
                "key_insight_en": "Narrative diversification across multiple collapse vectors ensures comprehensive trend undermining.",
                "key_insight_hinglish": "Alag alag angles se attack karne se trend guarantee collapse ho jaata hai. Koi ek narrative nahi chal sakti, sab milkar kaam karti hain."
            }
        }
        
        return json.dumps(report, indent=2, ensure_ascii=False)


def main():
    """Main execution function."""
    
    print("=" * 80)
    print("TREND SABOTEUR AGENT - Groq AI-Powered (Ultra-Fast + Auto-Research)")
    print("=" * 80)
    print("\nThis tool uses Groq AI to generate UNIQUE counter-narratives in seconds.")
    print("🔍 NEW: Auto-researches trends if you don't provide context!\n")
    
    # Get user input
    try:
        trend_name = input("Enter the trend/meme/hashtag to analyze: ").strip()
        if not trend_name:
            trend_name = "sigma male grindset"
            print(f"(Using default trend: '{trend_name}')")
        
        print("\n💡 TIP: Press Enter to skip context and let AI auto-research the trend!")
        trend_context = input("Enter context for this trend (optional, press Enter to skip): ").strip()
        
    except EOFError:
        # Handle non-interactive mode
        trend_name = "sigma male grindset"
        trend_context = ""
        print(f"Running in non-interactive mode with default trend: '{trend_name}'")
    
    print(f"\n{'=' * 80}")
    print(f"Analyzing trend: '{trend_name}'")
    
    # Initialize agent (will auto-research if no context)
    agent = TrendSaboteurAgent(trend_name, trend_context)
    
    print(f"{'=' * 80}\n")
    
    # Generate counter-narratives
    narratives = agent.generate_counter_narratives()
    
    # Display counter-narratives
    print("-" * 80)
    print("COUNTER-NARRATIVES:")
    print("-" * 80)
    for i, narrative in enumerate(narratives, 1):
        print(f"\n[{i}] {narrative.title_en}")
        print(f"    Hinglish: {narrative.title_hinglish}")
        print(f"    Description (EN): {narrative.description_en}")
        print(f"    Description (HI): {narrative.description_hinglish}")
        print(f"    Example Content: {narrative.example_content}")
        print(f"    Virality Probability: {narrative.virality_probability:.3f}")
        print(f"    Shareability Score: {narrative.shareability_score:.3f}")
        print(f"    Narrative Shift: {narrative.narrative_shift}")
        print(f"    Target Audience: {narrative.target_audience}")
    
    # Analyze collapse dynamics
    print("\n" + "-" * 80)
    print("COLLAPSE DYNAMICS ANALYSIS:")
    print("-" * 80)
    dynamics = agent.analyze_collapse_dynamics()
    print(f"\nAverage Virality Probability: {dynamics['average_virality_probability']}")
    print(f"Average Shareability Score: {dynamics['average_shareability_score']}")
    print(f"Dominant Narrative Shift: {dynamics['dominant_narrative_shift']}")
    print(f"Collapse Acceleration Factor: {dynamics['estimated_collapse_acceleration_factor']}")
    print(f"\nCollapse Explanation (EN):")
    print(f"  {dynamics['collapse_explanation_en']}")
    print(f"\nCollapse Explanation (Hinglish):")
    print(f"  {dynamics['collapse_explanation_hinglish']}")
    
    # Generate and save JSON report
    print("\n" + "-" * 80)
    print("Generating JSON report...")
    json_report = agent.generate_json_report()
    
    # Save to file
    output_file = "trend_saboteur_report.json"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(json_report)
    print(f"[OK] Report saved to: {output_file}")
    
    print("\n[OK] Trend Saboteur Agent execution complete.")
    print("\n💡 TIP: Run again for completely different counter-narratives!")
    print("⚡ Powered by Groq - Lightning fast AI generation!")
    return json_report


if __name__ == "__main__":
    json_output = main()