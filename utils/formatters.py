"""
Formatting utilities for data display and export
"""

import datetime
from typing import Dict, Any
import pandas as pd


class DataFormatter:
    """Handles formatting of data for display and export"""
    
    @staticmethod
    def format_currency(value: float, currency: str = "¥") -> str:
        """
        Format currency values
        
        Args:
            value: Numeric value to format
            currency: Currency symbol
            
        Returns:
            Formatted currency string
        """
        if pd.isna(value):
            return "N/A"
        return f"{currency}{value:,.2f}"
    
    @staticmethod
    def format_percentage(value: float, decimals: int = 2) -> str:
        """
        Format percentage values
        
        Args:
            value: Numeric value to format as percentage
            decimals: Number of decimal places
            
        Returns:
            Formatted percentage string
        """
        if pd.isna(value):
            return "N/A"
        return f"{value:.{decimals}f}%"
    
    @staticmethod
    def format_volume(value: float) -> str:
        """
        Format trading volume with appropriate units
        
        Args:
            value: Volume value
            
        Returns:
            Formatted volume string
        """
        if pd.isna(value) or value == 0:
            return "0"
        
        if value >= 1e8:  # 亿
            return f"{value/1e8:.2f}亿"
        elif value >= 1e4:  # 万
            return f"{value/1e4:.2f}万"
        else:
            return f"{value:.0f}"
    
    @staticmethod
    def format_date_range(start_date: datetime.date, end_date: datetime.date) -> str:
        """
        Format date range for display
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            Formatted date range string
        """
        return f"{start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}"
    
    @staticmethod
    def create_download_filename(prefix: str, codes: list, extension: str = "csv") -> str:
        """
        Create standardized download filename
        
        Args:
            prefix: File prefix
            codes: List of stock codes
            extension: File extension
            
        Returns:
            Formatted filename
        """
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        codes_str = "_".join(codes[:3])  # Limit to first 3 codes
        if len(codes) > 3:
            codes_str += f"_and_{len(codes)-3}_more"
        
        return f"{prefix}_{codes_str}_{timestamp}.{extension}"
    
    @staticmethod
    def format_summary_stats(stats: Dict[str, Any]) -> Dict[str, str]:
        """
        Format summary statistics for display
        
        Args:
            stats: Dictionary of statistics
            
        Returns:
            Dictionary with formatted values
        """
        formatted = {}
        
        for key, value in stats.items():
            if key in ['Start Price', 'End Price', 'Max Price', 'Min Price']:
                formatted[key] = DataFormatter.format_currency(value)
            elif key in ['Total Return (%)', 'Volatility (Annual %)', 'Sharpe Ratio']:
                formatted[key] = DataFormatter.format_percentage(value) if 'Ratio' not in key else f"{value:.3f}"
            elif key == 'Avg Volume':
                formatted[key] = DataFormatter.format_volume(value)
            else:
                formatted[key] = str(value)
        
        return formatted
    
    @staticmethod
    def format_dataframe_for_display(df: pd.DataFrame) -> pd.DataFrame:
        """
        Format DataFrame columns for better display
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with formatted columns
        """
        if df.empty:
            return df
            
        formatted_df = df.copy()
        
        # Format numeric columns
        for col in formatted_df.columns:
            if 'price' in col.lower() or 'close' in col.lower():
                if formatted_df[col].dtype in ['float64', 'int64']:
                    formatted_df[col] = formatted_df[col].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "N/A")
            elif 'volume' in col.lower():
                if formatted_df[col].dtype in ['float64', 'int64']:
                    formatted_df[col] = formatted_df[col].apply(DataFormatter.format_volume)
            elif 'change' in col.lower() and '%' in col:
                if formatted_df[col].dtype in ['float64', 'int64']:
                    formatted_df[col] = formatted_df[col].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else "N/A")
        
        return formatted_df 