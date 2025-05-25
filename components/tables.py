"""
Table components for the stock visualization application
"""

import datetime
from typing import Dict, List
import pandas as pd
import streamlit as st

from data.processor import DataProcessor
from utils.formatters import DataFormatter


class TableComponents:
    """Handles table display and data export functionality"""
    
    @staticmethod
    def render_data_table(df: pd.DataFrame, normalized: bool = False):
        """
        Render data table with download functionality
        
        Args:
            df: Stock data DataFrame
            normalized: Whether data is normalized
        """
        if df.empty:
            st.warning("没有数据可显示 | No data to display")
            return
        
        with st.expander("查看数据表 & 下载 | View Data Table & Download", expanded=False):
            # Prepare display dataframe
            display_df = DataProcessor.prepare_display_dataframe(df, normalized)
            
            # Format the dataframe for better display
            formatted_df = DataFormatter.format_dataframe_for_display(display_df)
            
            # Display table
            st.dataframe(formatted_df, use_container_width=True, height=400)
            
            # Download section
            TableComponents._render_download_section(df, display_df)
    
    @staticmethod
    def render_summary_stats(df: pd.DataFrame):
        """
        Render summary statistics table
        
        Args:
            df: Stock data DataFrame
        """
        if df.empty:
            return
        
        with st.expander("统计摘要 | Summary Statistics", expanded=False):
            # Generate summary statistics
            summary_stats = DataProcessor.generate_summary_stats(df)
            
            if not summary_stats:
                st.info("无法生成统计摘要 | Cannot generate summary statistics")
                return
            
            # Convert to DataFrame for display
            stats_df = pd.DataFrame(summary_stats).T
            
            # Format the statistics
            formatted_stats = {}
            for code, stats in summary_stats.items():
                formatted_stats[code] = DataFormatter.format_summary_stats(stats)
            
            formatted_stats_df = pd.DataFrame(formatted_stats).T
            
            # Display statistics table
            st.dataframe(formatted_stats_df, use_container_width=True)
            
            # Download CSV for summary stats
            csv_stats = stats_df.to_csv(index=True).encode('utf-8')
            st.download_button(
                label="下载统计摘要CSV | Download Summary Stats CSV",
                data=csv_stats,
                file_name=f"summary_stats_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
            )
    
    @staticmethod
    def render_comparison_table(df: pd.DataFrame, names: Dict[str, str]):
        """
        Render comparison table for multiple stocks
        
        Args:
            df: Stock data DataFrame
            names: Dictionary mapping codes to names
        """
        if df.empty or len(df['code'].unique()) <= 1:
            return
        
        with st.expander("股票比较 | Stock Comparison", expanded=False):
            comparison_data = []
            
            for code in df['code'].unique():
                code_data = df[df['code'] == code].copy()
                if code_data.empty:
                    continue
                
                # Calculate metrics for comparison
                start_price = code_data['close'].iloc[0]
                end_price = code_data['close'].iloc[-1]
                total_return = ((end_price / start_price) - 1) * 100
                max_price = code_data['close'].max()
                min_price = code_data['close'].min()
                
                # Calculate volatility if we have enough data
                volatility = 0
                if len(code_data) > 1:
                    daily_returns = code_data['close'].pct_change().dropna()
                    if len(daily_returns) > 0:
                        volatility = daily_returns.std() * (252 ** 0.5) * 100
                
                comparison_data.append({
                    '代码 | Code': code,
                    '名称 | Name': names.get(code, code),
                    '起始价格 | Start Price': start_price,
                    '结束价格 | End Price': end_price,
                    '总收益率 (%) | Total Return (%)': total_return,
                    '最高价 | Max Price': max_price,
                    '最低价 | Min Price': min_price,
                    '年化波动率 (%) | Annual Volatility (%)': volatility,
                    '数据点数 | Data Points': len(code_data)
                })
            
            if comparison_data:
                comparison_df = pd.DataFrame(comparison_data)
                
                # Format the comparison table
                formatted_comparison = comparison_df.copy()
                for col in ['起始价格 | Start Price', '结束价格 | End Price', '最高价 | Max Price', '最低价 | Min Price']:
                    formatted_comparison[col] = formatted_comparison[col].apply(lambda x: f"¥{x:.2f}")
                
                for col in ['总收益率 (%) | Total Return (%)', '年化波动率 (%) | Annual Volatility (%)']:
                    formatted_comparison[col] = formatted_comparison[col].apply(lambda x: f"{x:.2f}%")
                
                st.dataframe(formatted_comparison, use_container_width=True)
                
                # Download comparison data
                csv_comparison = comparison_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="下载比较数据CSV | Download Comparison CSV",
                    data=csv_comparison,
                    file_name=f"stock_comparison_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                )
    
    @staticmethod
    def _render_download_section(df: pd.DataFrame, display_df: pd.DataFrame):
        """
        Render download section with multiple format options
        
        Args:
            df: Original DataFrame
            display_df: Formatted display DataFrame
        """
        st.subheader("下载数据 | Download Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # CSV download for raw data
            csv_raw = df.to_csv(index=False).encode('utf-8')
            filename_raw = DataFormatter.create_download_filename(
                "stock_data_raw", 
                df['code'].unique().tolist() if 'code' in df.columns else ['data']
            )
            st.download_button(
                label="下载原始数据CSV | Download Raw CSV",
                data=csv_raw,
                file_name=filename_raw,
                mime="text/csv",
            )
        
        with col2:
            # CSV download for display data
            csv_display = display_df.to_csv(index=False).encode('utf-8')
            filename_display = DataFormatter.create_download_filename(
                "stock_data_formatted",
                df['code'].unique().tolist() if 'code' in df.columns else ['data']
            )
            st.download_button(
                label="下载格式化CSV | Download Formatted CSV",
                data=csv_display,
                file_name=filename_display,
                mime="text/csv",
            )
        
        with col3:
            # JSON download
            json_data = df.to_json(orient='records', date_format='iso').encode('utf-8')
            filename_json = DataFormatter.create_download_filename(
                "stock_data",
                df['code'].unique().tolist() if 'code' in df.columns else ['data'],
                "json"
            )
            st.download_button(
                label="下载JSON | Download JSON",
                data=json_data,
                file_name=filename_json,
                mime="application/json",
            )
    
    @staticmethod
    def render_data_info(df: pd.DataFrame):
        """
        Render data information summary
        
        Args:
            df: Stock data DataFrame
        """
        if df.empty:
            return
        
        # Create info metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="股票数量 | Number of Stocks",
                value=len(df['code'].unique()) if 'code' in df.columns else 0
            )
        
        with col2:
            st.metric(
                label="数据点总数 | Total Data Points",
                value=len(df)
            )
        
        with col3:
            if 'date' in df.columns:
                date_range = (df['date'].max() - df['date'].min()).days
                st.metric(
                    label="时间跨度 (天) | Time Span (Days)",
                    value=date_range
                )
        
        with col4:
            if 'data_source' in df.columns:
                sources = df['data_source'].unique()
                st.metric(
                    label="数据源数量 | Data Sources",
                    value=len(sources)
                )
    
    @staticmethod
    def render_complete_tables(df: pd.DataFrame, names: Dict[str, str], normalized: bool = False):
        """
        Render all table components
        
        Args:
            df: Stock data DataFrame
            names: Dictionary mapping codes to names
            normalized: Whether data is normalized
        """
        if df.empty:
            st.warning("没有数据可显示表格 | No data available for tables")
            return
        
        # Data information summary
        TableComponents.render_data_info(df)
        
        # Main data table
        TableComponents.render_data_table(df, normalized)
        
        # Summary statistics
        TableComponents.render_summary_stats(df)
        
        # Comparison table (only if multiple stocks)
        if len(df['code'].unique()) > 1:
            TableComponents.render_comparison_table(df, names) 