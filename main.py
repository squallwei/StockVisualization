"""
Main application file for the Stock Visualization Tool

This is the entry point for the refactored Streamlit application.
Run with: streamlit run main.py
"""

import streamlit as st
import pandas as pd

from config import APP_CONFIG, MAX_WIDTH
from components.sidebar import SidebarComponents
from components.charts import ChartComponents
from components.tables import TableComponents
from data.fetcher import StockDataFetcher
from data.processor import DataProcessor
from utils.validators import CodeValidator


class StockVisualizationApp:
    """Main application class for the Stock Visualization Tool"""
    
    def __init__(self):
        self.data_fetcher = StockDataFetcher()
        self.data_processor = DataProcessor()
        self.setup_page()
        self.setup_styling()
    
    def setup_page(self):
        """Configure Streamlit page settings"""
        st.set_page_config(**APP_CONFIG)
    
    def setup_styling(self):
        """Apply custom CSS styling"""
        st.markdown(f"""
        <style>
            .main {{
                background-color: #f5f7f9;
            }}
            .stApp {{
                max-width: {MAX_WIDTH}px;
                margin: 0 auto;
            }}
            h1, h2, h3 {{
                color: #0e1117;
            }}
            .sidebar .sidebar-content {{
                background-color: #f0f2f6;
            }}
            .reportview-container .main .block-container {{
                padding-top: 2rem;
            }}
            
            /* Custom styling for metrics */
            div[data-testid="metric-container"] {{
                background-color: white;
                border: 1px solid #ddd;
                padding: 1rem;
                border-radius: 0.5rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            }}
            
            /* Improve table styling */
            .dataframe {{
                border: none !important;
            }}
            
            /* Button styling */
            .stDownloadButton > button {{
                background-color: #ff6b6b;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0.5rem 1rem;
                font-weight: 500;
            }}
            
            .stDownloadButton > button:hover {{
                background-color: #ff5252;
                color: white;
            }}
        </style>
        """, unsafe_allow_html=True)
    
    def render_header(self):
        """Render application header"""
        st.title("📊 股票与指数可视化工具 | Stock & Index Visualization Tool")
        st.markdown(
            "使用此工具可视化和比较多个股票或指数的表现。| Use this tool to visualize and compare multiple stocks or indices performance."
        )
        st.markdown("---")
    
    def process_user_inputs(self, inputs: dict) -> tuple:
        """
        Process and validate user inputs
        
        Args:
            inputs: Dictionary of user inputs from sidebar
            
        Returns:
            Tuple of (valid_tickers, is_valid, error_message)
        """
        ticker_input = inputs['ticker_input']
        start_date = inputs['start_date']
        end_date = inputs['end_date']
        
        if not ticker_input:
            return [], False, "请输入股票或指数代码 | Please enter stock or index codes"
        
        # Validate date range
        date_valid, date_error = CodeValidator.validate_date_range(start_date, end_date)
        if not date_valid:
            return [], False, date_error
        
        # Validate and parse ticker codes
        valid_tickers, invalid_tickers = CodeValidator.validate_multiple_codes(ticker_input)
        
        if invalid_tickers:
            st.warning(f"无效的代码格式已跳过 | Invalid code formats skipped: {', '.join(invalid_tickers)}")
        
        if not valid_tickers:
            return [], False, "没有有效的股票或指数代码 | No valid stock or index codes"
        
        # Sanitize codes
        valid_tickers = CodeValidator.sanitize_codes(valid_tickers)
        
        return valid_tickers, True, ""
    
    def fetch_and_process_data(self, tickers: list, inputs: dict) -> tuple:
        """
        Fetch and process stock data
        
        Args:
            tickers: List of valid ticker codes
            inputs: Dictionary of user inputs
            
        Returns:
            Tuple of (processed_df, names_dict)
        """
        # Format dates for AKShare
        start_date_str = inputs['start_date'].strftime("%Y%m%d")
        end_date_str = inputs['end_date'].strftime("%Y%m%d")
        
        # Fetch data
        with st.spinner('获取数据中... | Fetching data...'):
            df, names = self.data_fetcher.fetch_multiple_stocks(
                tickers, start_date_str, end_date_str, inputs['adjust_value']
            )
        
        if df.empty:
            st.error("无法获取数据，请检查代码和日期范围 | Failed to fetch data, please check codes and date range")
            return pd.DataFrame(), {}
        
        # Process data (normalize if requested)
        if inputs['normalize']:
            df = self.data_processor.normalize_data(df, tickers)
        
        # Calculate additional metrics
        df = self.data_processor.calculate_returns(df)
        
        return df, names
    
    def render_example_section(self):
        """Render example section when no input is provided"""
        st.info("请在侧边栏输入股票或指数代码 | Please enter stock or index codes in the sidebar")
        
        st.markdown("### 示例图表 | Example Chart")
        st.markdown(
            "输入股票或指数代码后将显示类似下面的图表 | After entering stock or index codes, you'll see a chart similar to the one below"
        )
        
        # Create and display example chart
        example_chart = ChartComponents.create_example_chart()
        if example_chart:
            st.plotly_chart(example_chart, use_container_width=True)
        
        # Show feature highlights
        self.render_feature_highlights()
    
    def render_feature_highlights(self):
        """Render feature highlights section"""
        st.markdown("### 功能特点 | Key Features")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **📈 多数据源支持**
            - 股票数据
            - ETF基金数据  
            - 指数数据
            - 自动检测数据类型
            """)
        
        with col2:
            st.markdown("""
            **📊 丰富的可视化**
            - 交互式价格图表
            - 成交量分析
            - 收益率比较
            - 标准化对比
            """)
        
        with col3:
            st.markdown("""
            **📋 数据分析工具**
            - 统计摘要
            - 股票比较
            - 多格式下载
            - 实时数据缓存
            """)
    
    def run(self):
        """Main application run loop"""
        # Render header
        self.render_header()
        
        # Render sidebar and get inputs
        inputs = SidebarComponents.render_complete_sidebar()
        
        # Process inputs
        valid_tickers, is_valid, error_message = self.process_user_inputs(inputs)
        
        if not is_valid:
            if error_message:
                st.error(error_message)
            
            # Show example section
            self.render_example_section()
            return
        
        # Fetch and process data
        df, names = self.fetch_and_process_data(valid_tickers, inputs)
        
        if df.empty:
            return
        
        # Display success info
        st.success(f"成功获取 {len(valid_tickers)} 个股票/指数的数据 | Successfully fetched data for {len(valid_tickers)} stocks/indices")
        
        # Render charts in tabs
        st.markdown("### 📈 图表分析 | Chart Analysis")
        ChartComponents.render_chart_tabs(df, names, inputs['normalize'])
        
        # Render tables and statistics
        st.markdown("### 📋 数据分析 | Data Analysis")
        TableComponents.render_complete_tables(df, names, inputs['normalize'])


def main():
    """Main function to run the application"""
    app = StockVisualizationApp()
    app.run()


if __name__ == "__main__":
    main() 