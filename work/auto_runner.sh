#!/bin/bash
# 半导体投资数据自动化采集 - 入口脚本
# 用法: ./auto_runner.sh [daily|weekly|monthly]

BASE="/Users/zhen/Documents/Codex/2026-06-07/deepseek"
DATA_DIR="$BASE/outputs/data"
COLLECTOR="$BASE/work/data_collector.py"
mkdir -p "$DATA_DIR"

# 获取当前日期
DATE=$(date +%Y-%m-%d)
WEEKDAY=$(date +%u)  # 1=周一, 7=周日
DAY=$(date +%d)

run_collector() {
    echo "=== 市场数据采集: $DATE ==="
    cd "$BASE" && python3 "$COLLECTOR" --market
    echo "完成"
}

case "${1:-daily}" in
    daily)
        # 每日更新：只采集数据，不生成简报
        run_collector
        ;;
    weekly)
        # 周度更新（周一）：采集+框架检查清单
        run_collector
        echo ""
        echo "=== 周度检查清单 ==="
        echo "[ ] 存储: LPDDR价格趋势/美光三星动态"
        echo "[ ] 封测: CoWoS/先进封装消息"
        echo "[ ] AI终端: AI眼镜/机器人新品发布"
        echo "[ ] 竞对: 恒玄/晶晨等财报比较"
        echo "[ ] 减持监控: 瑞芯微减持进展"
        echo "[ ] 持仓逻辑复盘: 全志/瑞芯微核心逻辑是否变化"
        ;;
    monthly)
        # 月度深度复盘
        run_collector
        echo ""
        echo "=== 月度复盘检查清单 ==="
        echo "1️⃣ 上游环境变化"
        echo "   [ ] 存储价格趋势: 上涨/下跌/持平"
        echo "   [ ] 封测产能: 紧张/宽松"
        echo "   [ ] 代工利用率: 满产/有空余"
        echo ""
        echo "2️⃣ 持仓基本面"
        echo "   [ ] 全志科技毛利率趋势"
        echo "   [ ] 瑞芯微减持进展"
        echo "   [ ] 新产品出货情况"
        echo ""
        echo "3️⃣ 竞对追踪"
        echo "   [ ] 恒玄科技业绩及库存变化"
        echo "   [ ] 晶晨股份季度数据"
        echo ""
        echo "4️⃣ 综合评估"
        echo "   [ ] 当前持仓逻辑是否依然成立？"
        echo "   [ ] 是否有需要调整持仓的信号？"
        ;;
    *)
        echo "用法: $0 [daily|weekly|monthly]"
        echo "  daily   每日数据采集"
        echo "  weekly  周度数据+框架检查（建议周一）"
        echo "  monthly 月度深度复盘（建议1号）"
        ;;
esac
