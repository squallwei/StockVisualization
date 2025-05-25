"""
Configuration settings for the Stock Visualization Application
"""

import datetime
from typing import Dict, List, Tuple

# App Configuration
APP_CONFIG = {
    "page_title": "多股票和指数可视化工具 | Multi-Stock & Index Visualization",
    "page_icon": "📈",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Layout Configuration
MAX_WIDTH = 1200  # This will be used in CSS styling instead

# Date Configuration
DEFAULT_START_DATE = datetime.date(2023, 1, 1)
DEFAULT_END_DATE = datetime.date.today()
MIN_DATE = datetime.date(2000, 1, 1)

# Data Configuration
CACHE_TTL = 3600  # Cache time to live in seconds
MAX_WORKERS = 10  # Maximum number of concurrent requests
VALID_CODE_PATTERN = r'^[0-9]{6}$'

# Chart Configuration
CHART_HEIGHT = 600
CHART_COLORS = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
]

# Column Mappings
COLUMN_MAPPINGS = {
    "日期": "date",
    "开盘": "open",
    "收盘": "close",
    "最高": "high",
    "最低": "low",
    "成交量": "volume",
    "成交额": "amount",
    "振幅": "amplitude",
    "涨跌幅": "pct_change",
    "涨跌额": "price_change",
    "换手率": "turnover"
}

# Price Adjustment Options
ADJUST_OPTIONS = {
    "前复权 | Forward Adjusted": "qfq",
    "后复权 | Backward Adjusted": "hfq",
    "不复权 | Not Adjusted": ""
}

# Display Column Mappings
DISPLAY_COLUMNS = {
    'date': '日期 | Date',
    'code': '代码 | Code',
    'name': '名称 | Name',
    'data_source': '数据源 | Data Source',
    'close': '收盘价 | Close',
    'close_normalized': '标准化价格 | Normalized Price',
    'pct_change': '涨跌幅(%) | Change(%)'
}

# Chart Range Selector Buttons
RANGE_BUTTONS = [
    dict(count=1, label="1月 | 1M", step="month", stepmode="backward"),
    dict(count=3, label="3月 | 3M", step="month", stepmode="backward"),
    dict(count=6, label="6月 | 6M", step="month", stepmode="backward"),
    dict(count=1, label="1年 | 1Y", step="year", stepmode="backward"),
    dict(step="all", label="全部 | All")
] 