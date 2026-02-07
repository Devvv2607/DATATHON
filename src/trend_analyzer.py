"""Trend analysis and growth calculation"""
import numpy as np
from scipy import stats
import pandas as pd
from models import TrendData, TrendMetrics


class TrendAnalyzer:
    """Calculates growth metrics from trend data"""
    
    def calculate_growth_slope(self, interest_data: pd.DataFrame) -> float:
        """
        Calculate growth slope using linear regression.
        
        Args:
            interest_data: DataFrame with interest values over time
            
        Returns:
            Growth rate as percentage per month
        """
        if interest_data is None or interest_data.empty:
            return 0.0
        
        # Get the first column (the keyword interest values)
        values = interest_data.iloc[:, 0].values
        
        if len(values) < 2:
            return 0.0
        
        # Create x values (time indices)
        x = np.arange(len(values))
        
        # Perform linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, values)
        
        # Normalize to percentage per month
        # Slope is per day, multiply by 30 for monthly
        mean_interest = np.mean(values)
        if mean_interest == 0:
            return 0.0
        
        # Convert to percentage: (slope * 30 days / mean) * 100
        growth_rate = (slope * 30 / mean_interest) * 100
        
        return float(growth_rate)
    
    def analyze_trend_momentum(self, trend_data: TrendData) -> TrendMetrics:
        """
        Analyze trend momentum and calculate metrics.
        
        Args:
            trend_data: TrendData object with historical data
            
        Returns:
            TrendMetrics with calculated values
        """
        interest_df = trend_data.interest_over_time
        
        # Calculate growth slope
        growth_slope = self.calculate_growth_slope(interest_df)
        
        # Get values for additional metrics
        values = interest_df.iloc[:, 0].values
        
        # Calculate average interest
        average_interest = float(np.mean(values)) if len(values) > 0 else 0.0
        
        # Calculate volatility (standard deviation)
        volatility = float(np.std(values)) if len(values) > 1 else 0.0
        
        # Determine trend direction
        if growth_slope > 5:
            trend_direction = "up"
        elif growth_slope < -5:
            trend_direction = "down"
        else:
            trend_direction = "flat"
        
        return TrendMetrics(
            growth_slope=growth_slope,
            current_interest=trend_data.current_interest,
            peak_interest=trend_data.peak_interest,
            average_interest=average_interest,
            volatility=volatility,
            trend_direction=trend_direction
        )
