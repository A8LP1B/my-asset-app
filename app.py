
import streamlit as st
import pandas as pd

# 設定 App 標題與風格
st.set_page_config(page_title="2.0 全球雙引擎管理員", layout="centered")
st.title("🛡️ 2.0 全球雙引擎退休槓鈴")
st.write("目標配置：30/17.5/17.5/25/5/5")

# 1. 定義配置比例
ALLOCATION = {
    "0050 (台股市值核心)": 0.30,
    "00631L (台股正二)": 0.175,
    "00670L (美股正二)": 0.175,
    "433 高股息 (713/878/056)": 0.25,
    "00864B (美國短債/類現金)": 0.05,
    "00679B (美國長債/保險)": 0.05
}

# 2. 輸入介面
st.divider()
total_assets = st.number_input("請輸入當前總資產預計值 (萬)", min_value=0.0, value=1000.0, step=10.0)

st.subheader("📝 各項部位現況")
current_values = {}
for asset in ALLOCATION.keys():
    current_values[asset] = st.number_input(f"{asset} 現有價值 (萬)", min_value=0.0, value=total_assets * ALLOCATION[asset])

# 3. 計算再平衡
total_actual = sum(current_values.values())
data = []
for asset, target_pct in ALLOCATION.items():
    target_val = total_actual * target_pct
    actual_val = current_values[asset]
    diff = target_val - actual_val
    data.append({
        "資產名稱": asset,
        "目標金額": round(target_val, 1),
        "目前金額": round(actual_val, 1),
        "需調整": round(diff, 2),
        "指令": "🔼 買入" if diff > 0.5 else "🔽 賣出" if diff < -0.5 else "✅ 持有"
    })

# 4. 顯示結果
st.divider()
st.subheader("📊 再平衡建議")
df = pd.DataFrame(data)
st.table(df)

# 5. 股息估計
st.divider()
st.subheader("💰 預估年領股息")
# 假設殖利率
yields = {"0050": 0.03, "HighDiv": 0.08, "ShortBond": 0.045, "LongBond": 0.035}
total_div = (current_values["0050 (台股市值核心)"] * yields["0050"] + 
             current_values["433 高股息 (713/878/056)"] * yields["HighDiv"] +
             current_values["00864B (美國短債/類現金)"] * yields["ShortBond"] +
             current_values["00679B (美國長債/保險)"] * yields["LongBond"])

st.metric("預計年領總額", f"{round(total_div, 2)} 萬", f"每月約 {round(total_div/12, 2)} 萬")
