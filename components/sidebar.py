"""
Sidebar components for the stock visualization application
"""

import datetime
from typing import Tuple, Dict
import streamlit as st

from config import DEFAULT_START_DATE, DEFAULT_END_DATE, MIN_DATE, ADJUST_OPTIONS


class SidebarComponents:
    """Handles all sidebar UI components and interactions"""
    
    @staticmethod
    def render_header():
        """Render sidebar header"""
        st.sidebar.header("输入参数 | Input Parameters")
    
    @staticmethod
    def render_ticker_input() -> str:
        """
        Render ticker input section
        
        Returns:
            Input string with stock codes
        """
        st.sidebar.subheader("股票/指数代码 | Stock/Index Codes")
        ticker_input = st.sidebar.text_area(
            "输入股票或指数代码，用逗号分隔 | Enter stock or index codes, separated by commas",
            help="例如: 600000,601288,000001,399001 | Example: 600000,601288,000001,399001",
            placeholder="600000,601288,000001"
        )
        return ticker_input
    
    @staticmethod
    def render_date_inputs() -> Tuple[datetime.date, datetime.date]:
        """
        Render date input section
        
        Returns:
            Tuple of (start_date, end_date)
        """
        st.sidebar.subheader("日期范围 | Date Range")
        
        start_date = st.sidebar.date_input(
            "开始日期 | Start Date",
            value=DEFAULT_START_DATE,
            min_value=MIN_DATE,
            max_value=DEFAULT_END_DATE
        )
        
        end_date = st.sidebar.date_input(
            "结束日期 | End Date",
            value=DEFAULT_END_DATE,
            min_value=start_date,
            max_value=DEFAULT_END_DATE
        )
        
        return start_date, end_date
    
    @staticmethod
    def render_normalization_toggle() -> bool:
        """
        Render normalization toggle
        
        Returns:
            Whether normalization is enabled
        """
        return st.sidebar.checkbox(
            "标准化价格 (首日=100) | Normalize Prices (First Day=100)",
            value=False,
            help="将所有股票/指数的价格标准化，使首日价格为100，方便比较相对表现 | Normalize all stocks/indices to 100 on the first day to compare relative performance"
        )
    
    @staticmethod
    def render_adjustment_selector() -> str:
        """
        Render price adjustment selector
        
        Returns:
            Selected adjustment value
        """
        adjust = st.sidebar.selectbox(
            "价格调整方式 | Price Adjustment",
            options=list(ADJUST_OPTIONS.keys()),
            index=0,
            help="选择价格调整方式，前复权适合大多数分析 | Choose price adjustment method, forward adjusted is suitable for most analyses"
        )
        return ADJUST_OPTIONS[adjust]
    
    @staticmethod
    def render_info_section():
        """Render information section"""
        st.sidebar.markdown("---")
        st.sidebar.markdown("""
        **信息 | Info:**
        * 股票代码: 6位数字，例如 600000 (股票)
        * 基金代码: 6位数字，例如 510300 (ETF基金)
        * 指数代码: 6位数字，例如 000001 (上证指数)
        
        系统会自动检测代码类型并从适当的数据源获取数据。
        System will automatically detect code type and fetch data from appropriate source.
        """)
    
    @staticmethod
    def render_example_codes():
        """Render example codes section"""
        with st.sidebar.expander("示例代码 | Example Codes"):
            st.markdown("""
            **热门股票 | Popular Stocks:**
            - 600000 (浦发银行)
            - 000001 (平安银行)
            - 601318 (中国平安)
            - 000002 (万科A)
            
            **主要指数 | Major Indices:**
            - 000001 (上证指数)
            - 399001 (深证成指)
            - 399006 (创业板指)
            
            **热门ETF | Popular ETFs:**
            - 510300 (沪深300ETF)
            - 510500 (中证500ETF)
            - 159919 (沪深300ETF)
            """)
    
    @staticmethod
    def render_complete_sidebar() -> Dict[str, any]:
        """
        Render complete sidebar and return all input values
        
        Returns:
            Dictionary with all sidebar input values
        """
        SidebarComponents.render_header()
        
        ticker_input = SidebarComponents.render_ticker_input()
        start_date, end_date = SidebarComponents.render_date_inputs()
        normalize = SidebarComponents.render_normalization_toggle()
        adjust_value = SidebarComponents.render_adjustment_selector()
        
        SidebarComponents.render_info_section()
        SidebarComponents.render_example_codes()
        
        return {
            'ticker_input': ticker_input,
            'start_date': start_date,
            'end_date': end_date,
            'normalize': normalize,
            'adjust_value': adjust_value
        } 