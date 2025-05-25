"""
Data processor module for handling data transformations and calculations
"""

from typing import List, Dict
import pandas as pd
import logging

from config import DISPLAY_COLUMNS

logger = logging.getLogger(__name__)


class DataProcessor:
    """Handles data processing operations like normalization and formatting"""
    
    @staticmethod
    def normalize_data(df: pd.DataFrame, codes: List[str]) -> pd.DataFrame:
        """
        Normalize stock prices to 100 at the starting date for comparison
        
        Args:
            df: Stock data DataFrame
            codes: List of stock codes
            
        Returns:
            DataFrame with normalized prices
        """
        if df.empty:
            return df
            
        normalized_df = df.copy()
        
        for code in codes:
            code_data = normalized_df[normalized_df['code'] == code]
            if code_data.empty:
                continue
                
            # Get first day price
            first_day_price = code_data['close'].iloc[0]
            if first_day_price <= 0:  # Avoid division by zero
                logger.warning(f"Invalid first day price for {code}: {first_day_price}")
                continue
                
            # Normalize prices for this code
            mask = normalized_df['code'] == code
            normalized_df.loc[mask, 'close'] = (
                normalized_df.loc[mask, 'close'] / first_day_price * 100
            )
            
            # Also normalize high and low if they exist
            for col in ['high', 'low', 'open']:
                if col in normalized_df.columns:
                    normalized_df.loc[mask, col] = (
                        normalized_df.loc[mask, col] / first_day_price * 100
                    )
        
        return normalized_df
    
    @staticmethod
    def prepare_display_dataframe(df: pd.DataFrame, normalized: bool = False) -> pd.DataFrame:
        """
        Prepare DataFrame for display with proper column names
        
        Args:
            df: Input DataFrame
            normalized: Whether data is normalized
            
        Returns:
            DataFrame formatted for display
        """
        if df.empty:
            return df
            
        # Select relevant columns for display
        base_columns = ['date', 'code', 'name', 'close', 'pct_change']
        
        # Add data_source column if it exists
        if 'data_source' in df.columns:
            display_columns = ['date', 'code', 'name', 'data_source', 'close', 'pct_change']
        else:
            display_columns = base_columns
            
        # Filter to existing columns
        available_columns = [col for col in display_columns if col in df.columns]
        display_df = df[available_columns].copy()
        
        # Create column mapping for renaming
        rename_mapping = {}
        for col in available_columns:
            if col == 'close':
                if normalized:
                    rename_mapping[col] = DISPLAY_COLUMNS['close_normalized']
                else:
                    rename_mapping[col] = DISPLAY_COLUMNS['close']
            elif col in DISPLAY_COLUMNS:
                rename_mapping[col] = DISPLAY_COLUMNS[col]
        
        # Rename columns
        display_df = display_df.rename(columns=rename_mapping)
        
        return display_df
    
    @staticmethod
    def calculate_returns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate returns and additional metrics
        
        Args:
            df: Stock data DataFrame
            
        Returns:
            DataFrame with additional calculated columns
        """
        if df.empty:
            return df
            
        result_df = df.copy()
        
        # Calculate daily returns for each stock
        for code in df['code'].unique():
            mask = result_df['code'] == code
            code_data = result_df[mask].copy()
            
            if len(code_data) > 1:
                # Calculate daily returns
                code_data['daily_return'] = code_data['close'].pct_change()
                
                # Calculate cumulative returns
                code_data['cumulative_return'] = (1 + code_data['daily_return']).cumprod() - 1
                
                # Calculate rolling volatility (20-day)
                if len(code_data) >= 20:
                    code_data['volatility_20d'] = code_data['daily_return'].rolling(window=20).std() * (252 ** 0.5)
                
                # Update the main dataframe
                result_df.loc[mask, 'daily_return'] = code_data['daily_return']
                result_df.loc[mask, 'cumulative_return'] = code_data['cumulative_return']
                if 'volatility_20d' in code_data.columns:
                    result_df.loc[mask, 'volatility_20d'] = code_data['volatility_20d']
        
        return result_df
    
    @staticmethod
    def generate_summary_stats(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Generate summary statistics for each stock
        
        Args:
            df: Stock data DataFrame
            
        Returns:
            Dictionary with summary statistics
        """
        if df.empty:
            return {}
            
        summary_stats = {}
        
        for code in df['code'].unique():
            code_data = df[df['code'] == code]
            if code_data.empty:
                continue
                
            # Calculate basic statistics
            stats = {
                'Code': code,
                'Name': code_data['name'].iloc[0] if 'name' in code_data.columns else code,
                'Start Date': code_data['date'].min().strftime('%Y-%m-%d'),
                'End Date': code_data['date'].max().strftime('%Y-%m-%d'),
                'Start Price': code_data['close'].iloc[0],
                'End Price': code_data['close'].iloc[-1],
                'Total Return (%)': ((code_data['close'].iloc[-1] / code_data['close'].iloc[0]) - 1) * 100,
                'Max Price': code_data['close'].max(),
                'Min Price': code_data['close'].min(),
                'Avg Volume': code_data['volume'].mean() if 'volume' in code_data.columns else 0,
            }
            
            # Calculate volatility if we have enough data
            if len(code_data) > 1:
                daily_returns = code_data['close'].pct_change().dropna()
                if len(daily_returns) > 0:
                    stats['Volatility (Annual %)'] = daily_returns.std() * (252 ** 0.5) * 100
                    stats['Sharpe Ratio'] = (daily_returns.mean() / daily_returns.std()) * (252 ** 0.5) if daily_returns.std() > 0 else 0
            
            summary_stats[code] = stats
        
        return summary_stats 