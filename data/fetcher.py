"""
Data fetcher module for retrieving stock, fund, and index data
"""

import re
from concurrent.futures import ThreadPoolExecutor
from typing import Tuple, Dict, List, Optional
import logging

import akshare as ak
import pandas as pd
import streamlit as st

from config import VALID_CODE_PATTERN, MAX_WORKERS, CACHE_TTL, COLUMN_MAPPINGS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StockDataFetcher:
    """Handles fetching stock, fund, and index data from multiple sources"""
    
    def __init__(self):
        self.error_log: List[str] = []
    
    @st.cache_data(ttl=CACHE_TTL, show_spinner=False)
    def fetch_single_stock_data(_self, code: str, start_date: str, end_date: str, adjust: str = "qfq") -> Tuple[pd.DataFrame, str]:
        """
        Fetch data for a single stock/fund/index from multiple sources
        
        Args:
            code: Stock/fund/index code
            start_date: Start date in YYYYMMDD format
            end_date: End date in YYYYMMDD format
            adjust: Price adjustment type
            
        Returns:
            Tuple of (DataFrame, stock_name)
        """
        if not _self._validate_code(code):
            logger.warning(f"Invalid code format: {code}")
            return pd.DataFrame(), ""
        
        _self.error_log.clear()
        
        # Try different data sources in order
        data_sources = [
            ("stock", _self._fetch_stock_data),
            ("fund", _self._fetch_fund_data),
            ("index", _self._fetch_index_data)
        ]
        
        for source_type, fetch_func in data_sources:
            try:
                df, name = fetch_func(code, start_date, end_date, adjust)
                if not df.empty:
                    df = _self._standardize_dataframe(df, code, name, source_type)
                    return df, name
            except Exception as e:
                error_msg = f"{source_type.title()} data source error: {str(e)}"
                _self.error_log.append(error_msg)
                logger.error(error_msg)
        
        # Log all errors if no data found
        if _self.error_log:
            logger.error(f"All data sources failed for {code}: {'; '.join(_self.error_log)}")
        
        return pd.DataFrame(), ""
    
    def fetch_multiple_stocks(self, codes: List[str], start_date: str, end_date: str, adjust: str = "qfq") -> Tuple[pd.DataFrame, Dict[str, str]]:
        """
        Fetch data for multiple stocks concurrently
        
        Args:
            codes: List of stock codes
            start_date: Start date
            end_date: End date
            adjust: Price adjustment type
            
        Returns:
            Tuple of (combined DataFrame, names dictionary)
        """
        results = []
        names = {}
        data_sources = {}
        
        # Progress tracking
        progress_bar = st.progress(0)
        progress_text = st.empty()
        progress_text.text("Fetching data...")
        
        # Use ThreadPoolExecutor for concurrent requests
        with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, len(codes))) as executor:
            future_to_code = {
                executor.submit(self.fetch_single_stock_data, code, start_date, end_date, adjust): code
                for code in codes
            }
            
            completed = 0
            for future in future_to_code:
                code = future_to_code[future]
                try:
                    df, name = future.result()
                    if not df.empty:
                        results.append(df)
                        names[code] = name
                        if 'data_source' in df.columns:
                            data_sources[code] = df['data_source'].iloc[0]
                    else:
                        st.warning(f"No data found for {code}")
                except Exception as e:
                    logger.error(f"Error processing {code}: {str(e)}")
                    st.error(f"Error processing {code}: {str(e)}")
                
                # Update progress
                completed += 1
                progress = completed / len(codes)
                progress_bar.progress(progress)
                progress_text.text(f"Fetching data: {completed}/{len(codes)} completed")
        
        # Clear progress indicators
        progress_bar.empty()
        progress_text.empty()
        
        # Display data source information
        if data_sources:
            source_info = ", ".join([f"{code}: {source}" for code, source in data_sources.items()])
            st.info(f"Data sources used: {source_info}")
        
        if not results:
            return pd.DataFrame(), {}
        
        combined_df = pd.concat(results, ignore_index=True)
        return combined_df, names
    
    def _validate_code(self, code: str) -> bool:
        """Validate stock code format"""
        return bool(re.match(VALID_CODE_PATTERN, code.strip()))
    
    def _fetch_stock_data(self, code: str, start_date: str, end_date: str, adjust: str) -> Tuple[pd.DataFrame, str]:
        """Fetch stock data from akshare stock API"""
        df = ak.stock_zh_a_hist(
            symbol=code, period="daily", start_date=start_date, end_date=end_date, adjust=adjust
        )
        name = self._get_stock_name(code) if not df.empty else code
        return df, name
    
    def _fetch_fund_data(self, code: str, start_date: str, end_date: str, adjust: str) -> Tuple[pd.DataFrame, str]:
        """Fetch fund data from akshare fund API"""
        df = ak.fund_etf_hist_em(
            symbol=code, period="daily", start_date=start_date, end_date=end_date
        )
        name = self._get_fund_name(code) if not df.empty else code
        return df, name
    
    def _fetch_index_data(self, code: str, start_date: str, end_date: str, adjust: str) -> Tuple[pd.DataFrame, str]:
        """Fetch index data from akshare index API"""
        df = ak.index_zh_a_hist(
            symbol=code, period="daily", start_date=start_date, end_date=end_date
        )
        name = self._get_index_name(code) if not df.empty else code
        return df, name
    
    def _standardize_dataframe(self, df: pd.DataFrame, code: str, name: str, source_type: str) -> pd.DataFrame:
        """Standardize dataframe structure and add metadata"""
        # Standardize column names
        df = df.rename(columns=COLUMN_MAPPINGS)
        
        # Convert date to datetime and sort
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Add metadata
        df['code'] = code
        df['name'] = name
        df['data_source'] = source_type
        
        return df
    
    def _get_stock_name(self, code: str) -> str:
        """Get stock name from code"""
        try:
            stock_info = ak.stock_individual_info_em(symbol=code)
            return stock_info.iloc[0, 1] if not stock_info.empty else code
        except Exception as e:
            logger.warning(f"Failed to get stock name for {code}: {e}")
            return code
    
    def _get_fund_name(self, code: str) -> str:
        """Get fund name from code"""
        try:
            fund_info = ak.fund_individual_basic_info_xq(symbol=code)
            name_series = fund_info[fund_info['代码'] == code]['名称']
            return name_series.values[0] if not name_series.empty else code
        except Exception as e:
            logger.warning(f"Failed to get fund name for {code}: {e}")
            return code
    
    def _get_index_name(self, code: str) -> str:
        """Get index name from code"""
        try:
            index_info = ak.index_stock_info()
            name_series = index_info[index_info['代码'] == code]['名称']
            return name_series.values[0] if not name_series.empty else code
        except Exception as e:
            logger.warning(f"Failed to get index name for {code}: {e}")
            return code 