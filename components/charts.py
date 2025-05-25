"""
Chart components for the stock visualization application
"""

from typing import Dict, List, Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import streamlit as st

from config import CHART_HEIGHT, CHART_COLORS, RANGE_BUTTONS


class ChartComponents:
    """Handles chart creation and visualization"""
    
    @staticmethod
    def create_stock_chart(df: pd.DataFrame, names: Dict[str, str], normalized: bool = False) -> Optional[go.Figure]:
        """
        Create an interactive stock chart with Plotly
        
        Args:
            df: Stock data DataFrame
            names: Dictionary mapping codes to names
            normalized: Whether the data is normalized
            
        Returns:
            Plotly figure or None if data is empty
        """
        if df.empty:
            return None
        
        fig = go.Figure()
        codes = df['code'].unique()
        
        # Use colors from config
        colors = CHART_COLORS
        
        # Add a line for each stock
        for i, code in enumerate(codes):
            color = colors[i % len(colors)]
            code_data = df[df['code'] == code]
            
            if not code_data.empty:
                name = f"{code} · {names.get(code, '')}"
                fig.add_trace(
                    go.Scatter(
                        x=code_data['date'],
                        y=code_data['close'],
                        mode='lines',
                        name=name,
                        line=dict(color=color, width=2),
                        hovertemplate=(
                            "%{x}<br>"
                            + f"{name}<br>"
                            + "%{y:.2f}" + (" (指数)" if normalized else "")
                            + "<extra></extra>"
                        )
                    )
                )
        
        # Configure chart layout
        ChartComponents._configure_chart_layout(fig, normalized)
        
        return fig
    
    @staticmethod
    def create_volume_chart(df: pd.DataFrame, names: Dict[str, str]) -> Optional[go.Figure]:
        """
        Create volume chart
        
        Args:
            df: Stock data DataFrame
            names: Dictionary mapping codes to names
            
        Returns:
            Plotly figure or None if data is empty
        """
        if df.empty or 'volume' not in df.columns:
            return None
        
        fig = go.Figure()
        codes = df['code'].unique()
        colors = CHART_COLORS
        
        for i, code in enumerate(codes):
            color = colors[i % len(colors)]
            code_data = df[df['code'] == code]
            
            if not code_data.empty and 'volume' in code_data.columns:
                name = f"{code} · {names.get(code, '')}"
                fig.add_trace(
                    go.Bar(
                        x=code_data['date'],
                        y=code_data['volume'],
                        name=name,
                        marker_color=color,
                        opacity=0.7,
                        hovertemplate=(
                            "%{x}<br>"
                            + f"{name}<br>"
                            + "成交量: %{y:,.0f}"
                            + "<extra></extra>"
                        )
                    )
                )
        
        fig.update_layout(
            title="成交量 | Trading Volume",
            xaxis_title="日期 | Date",
            yaxis_title="成交量 | Volume",
            height=400,
            template="plotly_white",
            hovermode="x unified"
        )
        
        return fig
    
    @staticmethod
    def create_returns_chart(df: pd.DataFrame, names: Dict[str, str]) -> Optional[go.Figure]:
        """
        Create returns chart
        
        Args:
            df: Stock data DataFrame with returns calculated
            names: Dictionary mapping codes to names
            
        Returns:
            Plotly figure or None if data is empty
        """
        if df.empty or 'cumulative_return' not in df.columns:
            return None
        
        fig = go.Figure()
        codes = df['code'].unique()
        colors = CHART_COLORS
        
        for i, code in enumerate(codes):
            color = colors[i % len(colors)]
            code_data = df[df['code'] == code]
            
            if not code_data.empty and 'cumulative_return' in code_data.columns:
                name = f"{code} · {names.get(code, '')}"
                fig.add_trace(
                    go.Scatter(
                        x=code_data['date'],
                        y=code_data['cumulative_return'] * 100,  # Convert to percentage
                        mode='lines',
                        name=name,
                        line=dict(color=color, width=2),
                        hovertemplate=(
                            "%{x}<br>"
                            + f"{name}<br>"
                            + "累计收益率: %{y:.2f}%"
                            + "<extra></extra>"
                        )
                    )
                )
        
        fig.update_layout(
            title="累计收益率 | Cumulative Returns",
            xaxis_title="日期 | Date",
            yaxis_title="累计收益率 (%) | Cumulative Returns (%)",
            height=CHART_HEIGHT,
            template="plotly_white",
            hovermode="x unified"
        )
        
        # Add zero line
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        
        return fig
    
    @staticmethod
    def create_example_chart() -> go.Figure:
        """
        Create example chart for demonstration
        
        Returns:
            Example Plotly figure
        """
        # Create example data
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='B')
        np.random.seed(42)
        
        example_df = pd.DataFrame()
        example_names = {'600000': '浦发银行', '601288': '农业银行', '000001': '上证指数'}
        
        for i, (code, name) in enumerate(example_names.items()):
            base = 100 + i * 20
            volatility = 0.01 + i * 0.005
            
            prices = [base]
            for _ in range(1, len(dates)):
                change = np.random.normal(0.0003, volatility)
                prices.append(prices[-1] * (1 + change))
            
            df = pd.DataFrame({
                'date': dates,
                'code': code,
                'name': name,
                'close': prices
            })
            example_df = pd.concat([example_df, df])
        
        # Normalize data
        for code in example_names.keys():
            code_data = example_df[example_df['code'] == code]
            first_price = code_data['close'].iloc[0]
            example_df.loc[example_df['code'] == code, 'close'] = (
                example_df.loc[example_df['code'] == code, 'close'] / first_price * 100
            )
        
        # Create chart
        fig = ChartComponents.create_stock_chart(example_df, example_names, normalized=True)
        return fig
    
    @staticmethod
    def _configure_chart_layout(fig: go.Figure, normalized: bool = False):
        """
        Configure chart layout with standard settings
        
        Args:
            fig: Plotly figure to configure
            normalized: Whether data is normalized
        """
        title = "股票/指数价格走势 | Stock/Index Price Trends"
        if normalized:
            title += " (标准化: 首日=100 | Normalized: First Day=100)"
        
        fig.update_layout(
            title=title,
            xaxis_title="日期 | Date",
            yaxis_title="价格 | Price" if not normalized else "标准化价格指数 | Normalized Price Index",
            legend_title="代码·名称 | Code·Name",
            hovermode="x unified",
            height=CHART_HEIGHT,
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        # Add range selector and slider
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(buttons=RANGE_BUTTONS),
                rangeslider=dict(visible=True),
                type="date"
            )
        )
    
    @staticmethod
    def render_chart_tabs(df: pd.DataFrame, names: Dict[str, str], normalized: bool = False):
        """
        Render charts in tabs for better organization
        
        Args:
            df: Stock data DataFrame
            names: Dictionary mapping codes to names
            normalized: Whether data is normalized
        """
        if df.empty:
            st.error("无法显示图表：数据为空 | Cannot display charts: No data available")
            return
        
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["价格走势 | Price Trends", "成交量 | Volume", "收益率 | Returns"])
        
        with tab1:
            price_chart = ChartComponents.create_stock_chart(df, names, normalized)
            if price_chart:
                st.plotly_chart(price_chart, use_container_width=True)
        
        with tab2:
            volume_chart = ChartComponents.create_volume_chart(df, names)
            if volume_chart:
                st.plotly_chart(volume_chart, use_container_width=True)
            else:
                st.info("成交量数据不可用 | Volume data not available")
        
        with tab3:
            # Calculate returns if not already present
            if 'cumulative_return' not in df.columns:
                from data.processor import DataProcessor
                df = DataProcessor.calculate_returns(df)
            
            returns_chart = ChartComponents.create_returns_chart(df, names)
            if returns_chart:
                st.plotly_chart(returns_chart, use_container_width=True)
            else:
                st.info("收益率数据不可用 | Returns data not available") 