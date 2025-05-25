# 股票与指数可视化工具 | Stock & Index Visualization Tool (Refactored)

一个功能强大的多股票和指数可视化工具，支持实时数据获取、交互式图表和深入的数据分析。

A powerful multi-stock and index visualization tool with real-time data fetching, interactive charts, and comprehensive data analysis.

## 🌟 主要特性 | Key Features

### 📈 多数据源支持 | Multi-Data Source Support
- **股票数据**: 支持A股股票实时数据
- **ETF基金**: 支持ETF基金数据
- **指数数据**: 支持主要股指数据
- **自动检测**: 自动识别代码类型并选择合适的数据源

### 📊 丰富的可视化 | Rich Visualization
- **交互式图表**: 基于Plotly的高质量交互式图表
- **价格走势**: 支持标准化和非标准化价格对比
- **成交量分析**: 详细的成交量可视化
- **收益率分析**: 累计收益率和波动率分析
- **多时间范围**: 灵活的时间范围选择器

### 📋 数据分析工具 | Data Analysis Tools
- **统计摘要**: 详细的统计指标计算
- **股票比较**: 多股票横向对比分析
- **数据导出**: 支持CSV、JSON等多种格式导出
- **实时缓存**: 智能数据缓存提升性能

## 🏗️ 架构设计 | Architecture

### 项目结构 | Project Structure
```
stock_visualization/
├── main.py                 # 主应用入口 | Main application entry
├── config.py              # 配置文件 | Configuration
├── requirements.txt       # 依赖包 | Dependencies
├── data/                  # 数据模块 | Data module
│   ├── __init__.py
│   ├── fetcher.py         # 数据获取 | Data fetching
│   └── processor.py       # 数据处理 | Data processing
├── components/            # UI组件 | UI components
│   ├── __init__.py
│   ├── sidebar.py         # 侧边栏组件 | Sidebar components
│   ├── charts.py          # 图表组件 | Chart components
│   └── tables.py          # 表格组件 | Table components
└── utils/                 # 工具模块 | Utilities
    ├── __init__.py
    ├── validators.py      # 验证工具 | Validators
    └── formatters.py      # 格式化工具 | Formatters
```

### 核心模块 | Core Modules

#### 1. 数据层 | Data Layer (`data/`)
- **StockDataFetcher**: 负责从多个数据源获取股票、基金、指数数据
- **DataProcessor**: 处理数据标准化、收益率计算等数据转换

#### 2. 组件层 | Component Layer (`components/`)
- **SidebarComponents**: 管理所有侧边栏UI组件
- **ChartComponents**: 处理所有图表创建和可视化
- **TableComponents**: 管理数据表格显示和下载功能

#### 3. 工具层 | Utility Layer (`utils/`)
- **CodeValidator**: 处理股票代码验证和输入验证
- **DataFormatter**: 格式化数据显示和导出

## 🚀 快速开始 | Quick Start

### 安装依赖 | Install Dependencies
```bash
pip install -r requirements.txt
```

### 运行应用 | Run Application
```bash
streamlit run main.py
```

### 使用方法 | Usage

1. **输入股票代码**: 在侧边栏输入6位数字股票/基金/指数代码
2. **选择日期范围**: 设置数据的开始和结束日期
3. **配置选项**: 选择是否标准化价格、复权方式等
4. **查看分析**: 在多个标签页中查看价格走势、成交量、收益率
5. **导出数据**: 下载原始数据或格式化数据

### 示例代码 | Example Codes
```
股票: 600000,601288,000001
基金: 510300,510500,159919
指数: 000001,399001,399006
```

## 🔧 配置说明 | Configuration

### 应用配置 | Application Config (`config.py`)
```python
# 修改默认设置
DEFAULT_START_DATE = datetime.date(2023, 1, 1)
CACHE_TTL = 3600  # 缓存时间(秒)
MAX_WORKERS = 10  # 并发请求数
```

### 自定义样式 | Custom Styling
应用支持通过CSS自定义样式，主要样式在`main.py`的`setup_styling`方法中定义。

## 📊 功能详解 | Feature Details

### 数据获取 | Data Fetching
- **并发请求**: 使用ThreadPoolExecutor并发获取多个股票数据
- **多源容错**: 自动尝试股票、基金、指数三个数据源
- **智能缓存**: 基于Streamlit的缓存机制，避免重复请求
- **进度显示**: 实时显示数据获取进度

### 图表分析 | Chart Analysis
- **标准化对比**: 将不同股票标准化到相同起点便于比较
- **交互功能**: 支持缩放、平移、时间范围选择
- **多图表类型**: 价格走势、成交量、收益率分析
- **专业配色**: 使用色彩友好的专业配色方案

### 数据分析 | Data Analysis
- **统计指标**: 收益率、波动率、夏普比率等
- **比较分析**: 多股票横向对比表格
- **数据导出**: 原始数据、格式化数据、JSON格式
- **汇总信息**: 数据点数量、时间跨度等元信息

## 🔒 错误处理 | Error Handling

### 数据源容错 | Data Source Failover
```python
# 按优先级尝试数据源
data_sources = [
    ("stock", self._fetch_stock_data),
    ("fund", self._fetch_fund_data), 
    ("index", self._fetch_index_data)
]
```

### 输入验证 | Input Validation
- 股票代码格式验证（6位数字）
- 日期范围合理性检查
- 数据完整性验证

### 用户友好的错误信息 | User-Friendly Error Messages
- 中英文双语错误提示
- 具体的错误原因说明
- 建议的解决方案

## 🎨 界面设计 | UI Design

### 响应式布局 | Responsive Layout
- 自适应不同屏幕尺寸
- 合理的组件间距和布局
- 专业的色彩搭配

### 用户体验 | User Experience
- 直观的操作流程
- 实时的反馈信息
- 便捷的数据导出

## 🚀 性能优化 | Performance Optimization

### 缓存策略 | Caching Strategy
- **数据缓存**: 1小时TTL避免重复API调用
- **函数级缓存**: 对数据处理函数进行缓存
- **用户会话缓存**: 基于Streamlit的会话状态

### 并发处理 | Concurrent Processing
- **多线程获取**: 并发获取多个股票数据
- **限制并发数**: 防止API限流
- **优雅降级**: 单个请求失败不影响整体

## 📝 开发说明 | Development Notes

### 代码规范 | Code Standards
- **类型提示**: 使用Python类型提示提高代码可读性
- **文档字符串**: 详细的函数和类文档
- **模块化设计**: 清晰的模块分离和依赖关系

### 扩展开发 | Extension Development
- **新数据源**: 在`StockDataFetcher`中添加新的数据获取方法
- **新图表类型**: 在`ChartComponents`中添加新的可视化
- **新分析功能**: 在`DataProcessor`中添加新的计算方法

## 📄 许可证 | License

本项目采用MIT许可证，详见LICENSE文件。

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 贡献 | Contributing

欢迎提交Issue和Pull Request来改进这个项目！

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 支持 | Support

如有问题或建议，请通过以下方式联系：
- 提交GitHub Issue
- 发送邮件至项目维护者

For questions or suggestions, please:
- Submit a GitHub Issue
- Email the project maintainers 