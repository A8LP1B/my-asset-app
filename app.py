import streamlit as st
import pandas as pd

# 設定 App 標題與風格
st.set_page_config(page_title="2.0 全球雙引擎管理員", layout="centered")
st.title("🛡️ 2.0 全球雙引擎退休槓鈴")
st.write("目標配置：30 / 17.5 / 17.5 / (10+7.5+7.5) / 5 / 5")

# 1. 定義配置比例 (將 25% 高股息拆分為 10%, 7.5%, 7.5%)
ALLOCATION = {
    "0050 (台股市值核心)": 0.30,
    "00631L (台股正二)": 0.175,
    "00670L (美股正二)": 0.175,
    "00713 (高息低波-核心)": 0.10,
    "00878 (永續高股息)": 0.075,
    "0056 (元大高股息)": 0.075,
    "00864B (美國短債/類現金)": 0.05,
    "00679B (美國長債/保險)": 0.05
}

# 2. 輸入介面
st.divider()
total_assets = st.number_input("請輸入當前總資產預計值 (萬)", min_value=0.0, value=1000.0, step=10.0)

st.subheader("📝 各項部位現況")
current_values = {}
for asset in ALLOCATION.keys():
    # 預設值給目標比例的金額，方便使用者微調
    current_values[asset] = st.number_input(f"{asset} 現有價值 (萬)", min_value=0.0, value=round(total_assets * ALLOCATION[asset], 1))

# 3. 計算再平衡
total_actual = sum(current_values.values())
data = []
for asset, target_pct in ALLOCATION.items():
    target_val = total_actual * target_pct
    actual_val = current_values[asset]
    diff = target_val - actual_val
    actual_pct = (actual_val / total_actual * 100) if total_actual > 0 else 0
    
    data.append({
        "資產名稱": asset,
        "目標比例": f"{target_pct*100}%",
        "目前比例": f"{round(actual_pct, 1)}%",
        "目標金額": round(target_val, 1),
        "目前金額": round(actual_val, 1),
        "需調整": round(diff, 2),
        "指令": "🔼 買入" if diff > 0.5 else "🔽 賣出" if diff < -0.5 else "✅ 持有"
    })

# 4. 顯示結果
st.divider()
st.subheader("📊 再平衡建議表")
df = pd.DataFrame(data)
st.table(df)

# 5. 股息估計 (2026年預估殖利率)
st.divider()
st.subheader("💰 預估年領股息")
# 假設殖利率: 0050:3%, 00713:7%, 00878:8%, 0056:10%, 短債:4.5%, 長債:3.5%
yields = {
    "0050 (台股市值核心)": 0.03,
    "00631L (台股正二)": 0.0,
    "00670L (美股正二)": 0.0,
    "00713 (高息低波-核心)": 0.07,
    "00878 (永續高股息)": 0.08,
    "0056 (元大高股息)": 0.10,
    "00864B (美國短債/類現金)": 0.045,
    "00679B (美國長債/保險)": 0.035
}

total_div = sum(current_values[asset] * yields[asset] for asset in ALLOCATION.keys())

c1, c2 = st.columns(2)
c1.metric("預計年領總額", f"{round(total_div, 2)} 萬")
c2.metric("每月平均收入", f"{round(total_div/12, 4)} 萬")

st.info("💡 提醒：正二部位不直接配息，其收益已反映在淨值中。")
