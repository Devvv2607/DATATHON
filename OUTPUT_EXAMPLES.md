# Brand Trend Revenue Intelligence Agent - Output Examples

This document shows actual output examples from the application in tabular format.

---

## Example 1: Growing Trend Output

```
================================================================================
BRAND TREND REVENUE INTELLIGENCE ANALYSIS
================================================================================
Timestamp: 2026-02-07 19:27:33 UTC

📊 TREND OVERVIEW
--------------------------------------------------------------------------------
Domain:                   fidget spinners
Keyword:                  fidget spinners
Classification:           GROWING
Confidence:               78.2%
Growth Rate:              +8.21% monthly
Current Interest:         59/100
Peak Interest:            100/100

Reasoning:                Trend shows positive momentum with 8.2% monthly 
                          growth. Current interest at 59, peak was 100. Strong 
                          upward trajectory indicates growing market demand.

💡 GROWTH RECOMMENDATIONS
================================================================================

🎯 RECOMMENDED ACTIONS
--------------------------------------------------------------------------------
#   Action                              Priority   Reach        Conversion
--------------------------------------------------------------------------------
1   Scale fidget spinners campaigns     HIGH       20-30%       12-18% lift
2   Create fidget spinners-specific co  HIGH       15-25%       10-15% lift
3   Optimize conversion funnel          MEDIUM     10-15%       15-20% lift

📝 ACTION DETAILS
--------------------------------------------------------------------------------
1. Scale fidget spinners campaigns
   Increase investment in fidget spinners-related marketing

2. Create fidget spinners-specific content
   Develop content targeting fidget spinners audience

3. Optimize conversion funnel
   Refine landing pages for fidget spinners traffic

💰 BUDGET STRATEGY
--------------------------------------------------------------------------------
Recommendation:           Increase budget by 25%
Scaling Percentage:       20-30%
Rationale:                Strong growth momentum at 8.2% monthly

📝 CONTENT ANGLES
--------------------------------------------------------------------------------
  1. Trending fidget spinners topics
  2. fidget spinners best practices
  3. Latest fidget spinners innovations

📈 ESTIMATED IMPACT
--------------------------------------------------------------------------------
Reach Increase:           25-35%
Conversion Impact:        15-20% lift
Revenue Potential:        20-30% increase

================================================================================
```

---

## Example 2: Declining Trend Output

```
================================================================================
BRAND TREND REVENUE INTELLIGENCE ANALYSIS
================================================================================
Timestamp: 2026-02-07 19:29:23 UTC

📊 TREND OVERVIEW
--------------------------------------------------------------------------------
Domain:                   fashion
Keyword:                  declining trend example
Classification:           DECLINING
Confidence:               82.0%
Growth Rate:              -8.50% monthly
Current Interest:         40/100
Peak Interest:            70/100

Reasoning:                Trend shows negative momentum with -8.5% monthly 
                          decline. Current interest at 40, down from peak of 70. 
                          Declining trajectory suggests waning market interest.

🔍 RELATED QUERIES
--------------------------------------------------------------------------------
  1. related query 1
  2. related query 2
  3. related query 3

⚠️  DECLINE ANALYSIS & PIVOT STRATEGY
================================================================================

🚨 RISK ASSESSMENT
--------------------------------------------------------------------------------
Days Until Collapse:           180 days (~6 months)
Projected Marketing Burn:      $6,500.00
Recommendation:                TRY REVIVAL

🔧 REVIVAL CONDITIONS (If Attempting Revival)
--------------------------------------------------------------------------------
  1. Significant external event drives renewed interest
  2. New product innovation

🔄 ALTERNATIVE TRENDS TO PIVOT TOWARD
--------------------------------------------------------------------------------
#   Keyword                        Growth       Difficulty   Relevance
--------------------------------------------------------------------------------
1   emerging alternative 1         +15.0%       MEDIUM       Growing interest in related sp
2   innovative alternative 2       +12.0%       LOW          New developments in the field

🎯 PIVOT STRATEGY
--------------------------------------------------------------------------------
Approach:       Gradually shift from declining trend to emerging alternatives
Timeline:       2-3 months

Key Actions:
  1. Research alternative trends
  2. Test content with new keywords
  3. Reallocate 20% of budget

================================================================================
```

---

## Example 3: Stable Trend Output

```
================================================================================
BRAND TREND REVENUE INTELLIGENCE ANALYSIS
================================================================================
Timestamp: 2026-02-07 19:25:31 UTC

📊 TREND OVERVIEW
--------------------------------------------------------------------------------
Domain:                   fashion
Keyword:                  fashion
Classification:           STABLE
Confidence:               61.6%
Growth Rate:              -4.61% monthly
Current Interest:         86/100
Peak Interest:            100/100

Reasoning:                Trend shows stable momentum with -4.6% monthly change. 
                          Current interest at 86, maintaining relatively 
                          consistent levels. Stable trajectory indicates 
                          sustained but not growing demand.

📋 RECOMMENDATION
--------------------------------------------------------------------------------
Trend is STABLE. Monitor for changes and maintain current strategy.

================================================================================
```

---

## Key Sections Explained

### 📊 Trend Overview
- **Domain**: The business category you entered
- **Keyword**: The specific trend being analyzed
- **Classification**: GROWING, DECLINING, or STABLE
- **Confidence**: How confident the system is in the classification (0-100%)
- **Growth Rate**: Monthly percentage change (positive = growing, negative = declining)
- **Current Interest**: Current search interest level (0-100)
- **Peak Interest**: Highest search interest level in the period (0-100)

### For Growing Trends:

#### 🎯 Recommended Actions
- Prioritized list of actions to capitalize on growth
- Shows expected reach increase and conversion impact
- Priority levels: HIGH, MEDIUM, LOW

#### 💰 Budget Strategy
- Specific budget increase recommendation
- Scaling percentage range
- Rationale based on growth momentum

#### 📝 Content Angles
- Suggested content topics to create
- Aligned with trending keywords

#### 📈 Estimated Impact
- Expected reach increase percentage
- Conversion lift estimate
- Revenue potential increase

### For Declining Trends:

#### 🚨 Risk Assessment
- **Days Until Collapse**: Estimated time before trend becomes unprofitable
- **Projected Marketing Burn**: Money you'll waste if you continue ($$$)
- **Recommendation**: EXIT or TRY REVIVAL

#### 🔄 Alternative Trends
- 2-3 rising trends to pivot toward
- Growth rate for each alternative
- Entry difficulty assessment
- Relevance to your domain

#### 🎯 Pivot Strategy
- Clear approach for transitioning
- Timeline (typically 2-3 months)
- Specific action steps

#### 🔧 Revival Conditions
- Scenarios where revival might work
- Only shown if recommendation is "TRY REVIVAL"

### For Stable Trends:

#### 📋 Recommendation
- Simple guidance to monitor and maintain
- Watch for changes in trend direction

---

## How to Run

```bash
# Activate virtual environment
activate_venv.bat

# Run the application
cd src
python main.py

# Enter your domain when prompted
Domain: fashion
```

The application will analyze trends and display results in this tabular format.

---

## Output Format Options

The application currently outputs in **table format** by default. This provides:
- ✅ Easy-to-read structure
- ✅ Clear visual hierarchy
- ✅ Highlighted key metrics
- ✅ Professional presentation

If you need JSON output for programmatic use, you can modify the `ResponseFormatter` initialization in `src/pipeline.py`:

```python
# For table output (default)
self.formatter = ResponseFormatter(output_format="table")

# For JSON output
self.formatter = ResponseFormatter(output_format="json")
```

---

## Understanding the Numbers

### Growth Rate Thresholds
- **> +5%**: Growing trend - Scale and invest
- **-5% to +5%**: Stable trend - Monitor and maintain
- **< -5%**: Declining trend - Consider pivot or exit
- **< -20%**: Severe decline - Exit immediately

### Marketing Burn Calculation
The projected marketing burn is calculated based on:
- Current decline rate
- Days until the trend becomes unprofitable
- Assumed monthly marketing spend ($1,000 base)
- Adjusted for severity of decline

**Example**: If your actual monthly marketing spend is $5,000, multiply the projected burn by 5.

### Confidence Levels
- **> 80%**: High confidence - Act decisively
- **60-80%**: Medium confidence - Proceed with monitoring
- **< 60%**: Lower confidence - Gather more data

---

## Next Steps Based on Output

### If You See GROWING:
1. ✅ Implement the top 2-3 recommended actions immediately
2. ✅ Increase budget by the suggested percentage
3. ✅ Create content using the suggested angles
4. ✅ Monitor weekly to ensure momentum continues

### If You See DECLINING:
1. ⚠️ Calculate your actual marketing burn (multiply by your budget/1000)
2. ⚠️ Evaluate if revival conditions are realistic
3. ⚠️ Research the alternative trends suggested
4. ⚠️ Begin implementing the pivot strategy within 1 week
5. ⚠️ Reallocate budget gradually (20% per month)

### If You See STABLE:
1. ➡️ Maintain current marketing strategy
2. ➡️ Run the analysis monthly to catch changes early
3. ➡️ Test small optimizations (10-15% of budget)
4. ➡️ Be ready to scale or pivot based on changes
