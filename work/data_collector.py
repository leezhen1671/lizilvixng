#!/usr/bin/env python3
"""半导体投资数据采集器 v2.1 - 自动化监测工具"""
import json, os, subprocess, sys
from datetime import datetime, date

OUTPUT_DIR = "/Users/zhen/Documents/Codex/2026-06-07/deepseek/outputs"
DATA_DIR = os.path.join(OUTPUT_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

STOCKS = {
    "全志科技": {"sina_code": "sz300458", "role": "核心持仓"},
    "瑞芯微":   {"sina_code": "sh603893", "role": "核心持仓"},
    "恒玄科技": {"sina_code": "sz300661", "role": "竞对参考"},
    "晶晨股份": {"sina_code": "sh688099", "role": "赛道参考"},
    "圣邦股份": {"sina_code": "sz300673", "role": "赛道参考"},
    "中芯国际": {"sina_code": "sh688981", "role": "代工参考"},
    "立昂微":   {"sina_code": "sh605358", "role": "上游参考"},
}

def fetch_price():
    """通过新浪财经API - 处理GBK编码"""
    codes = ",".join([info["sina_code"] for info in STOCKS.values()])
    result = subprocess.run(
        ["curl", "-s", "--max-time", "10",
         "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
         "-H", "Referer: https://finance.sina.com.cn",
         f"https://hq.sinajs.cn/list={codes}"],
        capture_output=True, timeout=15
    )
    # Sina returns GBK encoding
    raw_text = result.stdout.decode("gbk", errors="replace")
    data = {}
    for line in raw_text.strip().split("\n"):
        if not line.startswith("var hq_str_"):
            continue
        try:
            parts = line.split('"')[1].split(",")
            name = parts[0]
            cl = float(parts[3]) if parts[3] else 0
            yc = float(parts[2]) if parts[2] else 0
            data[name] = {
                "price": cl,
                "open": float(parts[1]) if parts[1] else 0,
                "yclose": yc,
                "high": float(parts[4]) if parts[4] else 0,
                "low": float(parts[5]) if parts[5] else 0,
                "volume": int(parts[8]) if parts[8] else 0,
                "amount": round(float(parts[9]) / 100000000, 2) if parts[9] else 0,
                "change": round(cl - yc, 2),
                "change_pct": round((cl - yc) / yc * 100, 2) if yc else 0,
                "date": parts[30] if len(parts) > 30 else "",
            }
        except Exception as e:
            continue
    return data

def collect_market_snapshot():
    print("📊 采集市场数据...")
    prices = fetch_price()
    snap = {"date": datetime.now().strftime("%Y-%m-%d %H:%M"), "stocks": {}, "market_date": ""}
    for name, info in STOCKS.items():
        if name in prices:
            d = prices[name]
            snap["stocks"][name] = {"role": info["role"], "data": d}
            snap["market_date"] = d.get("date", "")
            status = f"¥{d['price']:.2f} ({d['change']:+.2f}, {d.get('change_pct',0):+.2f}%)"
        else:
            status = "⚠️ 未获取到"
            snap["stocks"][name] = {"role": info["role"], "data": {"error": "no_data"}}
        print(f"  {name} ({info['role']}): {status}")
    return snap

def save_snapshot(snap):
    today = date.today().isoformat()
    json_path = os.path.join(DATA_DIR, f"snapshot_{today}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, indent=2)
    
    lines = [f"# 市场快照 - {snap['date']}\n",
             f"行情日期: {snap.get('market_date','')}\n",
             "## 📈 表现\n"]
    lines.append("| 股票 | 角色 | 最新价 | 涨跌额 | 涨跌幅% | 最高 | 最低 | 昨收 |")
    lines.append("|------|------|--------|--------|---------|------|------|------|")
    for name, info in snap["stocks"].items():
        d = info["data"]
        if "price" in d and d["price"]:
            c = d["change"]
            mark = "🟢" if c > 0.01 else "🔴" if c < -0.01 else "⚪"
            lines.append(f"| {name} | {info['role']} | ¥{d['price']:.2f} | {mark}{c:+.2f} | {d.get('change_pct',0):+.2f}% | ¥{d['high']:.2f} | ¥{d['low']:.2f} | ¥{d['yclose']:.2f} |")
        else:
            lines.append(f"| {name} | {info['role']} | ⚠️ 无数据 | - | - | - | - |")
    
    # 框架检查清单
    lines.extend([
        "\n## ✅ 周度检查清单",
        "- [ ] 存储: LPDDR价格趋势/存储巨头动态",
        "- [ ] 封测: CoWoS/先进封装消息",
        "- [ ] AI终端: 眼镜/机器人/座舱新品",
        "- [ ] 竞对: 恒玄/晶晨等公司动态",
        "- [ ] 减持监控: 瑞芯微减持进展\n",
    ])
    
    md_path = os.path.join(DATA_DIR, f"snapshot_{today}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    
    print(f"\n✅ JSON: {os.path.basename(json_path)}")
    print(f"✅ 摘要: {os.path.basename(md_path)}")
    return md_path

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "--market":
        snap = collect_market_snapshot()
        save_snapshot(snap)
    else:
        print("半导体数据采集器 v2.1")
        print("=" * 40)
        print("  python3 data_collector.py --market  # 采集实时快照")
        print(f"\n数据目录: {DATA_DIR}")
