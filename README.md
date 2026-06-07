# 半导体投资分析系统

📊 端侧 AI 芯片赛道（全志科技 + 瑞芯微）的标准化数据采集与投资分析框架

## 功能

- **实时看板**: 自动采集股票数据，带图表可视化
- **自动化采集**: GitHub Actions 每日自动运行
- **投资框架**: 标准化的产业链数据收集与分析流程
- **跨设备访问**: GitHub Pages 托管，任何浏览器可看

## 目录结构

```
├── outputs/
│   ├── dashboard_v2.html      # 可视化看板（主页面）
│   ├── 半导体投资分析框架.md    # 投资分析框架
│   └── data/                  # 每日采集数据存档
├── work/
│   ├── data_collector.py      # 数据采集脚本
│   └── auto_runner.sh         # 自动化启动脚本
└── .github/workflows/         # GitHub Actions 配置
```

## 技术栈

- **数据源**: 新浪财经 API
- **可视化**: ECharts
- **自动化**: GitHub Actions
- **托管**: GitHub Pages
