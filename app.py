import streamlit as st
import pandas as pd

# 1. 設定 App 標題與風格
st.set_page_config(page_title="2.4 退休槓鈴終極儀表板", layout="centered")
st.title("🛡️ 2.4 全球精煉退休槓鈴")
st.write("配置比例：35 / 10 / 10 / 5 / (12+9+9) / 5 / 5")

# 2. 市場監測儀表板 (放在最上方，掌握風險警訊)
st.divider()
st.subheader("📡 市場情緒與債券策略監測")

# 模擬 2026/04 市場數據 (可用於判斷長短債策略)
yield_2y = 3.75  # 短端參考 (00864B 相關)
yield_10y = 4.35 # 長端參考 (00679B 相關)
spread = round(yield_10y - yield_2y, 2)

c1, c2, c3 = st.columns(3)
c1.metric("美債 10Y-2Y 利差", f"{spread}%")
c2.write("**當前階段：** 曲線正常化/陡峭化")
with c3:
    if spread > 0.4:
        st.success("✅ 長債避險回歸")
    elif 0 <= spread <= 0.4:
        st.warning("⚠️ 經濟擴張末期")
    else:
        st.error("🚨 殖利率倒掛")

# 3. 定義配置比例與動態再平衡門檻
# 00864B 門檻窄(2%)，00679B 門檻寬(10%)，其餘 5%
ALLOCATION = {
    "0050 (台股市值核心)": {"pct": 0.35, "threshold": 0.05},
    "00631L (台股正二)": {"pct": 0.10, "threshold": 0.05},
    "00670L (美股正二)": {"pct": 0.10, "threshold": 0.05},
    "VXUS (國際股票-衛星)": {"pct": 0.05, "threshold": 0.10},
    "00713 (高息低波-核心)": {"pct": 0.12, "threshold": 0.05},
    "00878 (永續高股息)": {"pct": 0.09, "threshold": 0.05},
    "0056 (元大高股息)": {"pct": 0.09, "threshold": 0.05},
    "00864B (美國短債-類現金)": {"pct": 0.05, "threshold": 0.02}, # 窄門檻
    "00679B (美國長債-避險)": {"pct": 0.05, "threshold": 0.10}  # 寬門檻
}

# 4. 資產輸入介面
st.divider()
total_assets = st.number_input("請輸入預估總資產 (萬 TWD)", min_value=0.0, value=1000.0, step=10.0)

st.subheader("📝 部位現況輸入")
current_values = {}
for asset in ALLOCATION.keys():
    # 預設值為目標比例金額，方便微調
    current_values[asset] = st.number_input(f"{asset} (萬)", min_value=0.0, value=round(total_assets * ALLOCATION[asset]['pct'], 1))

# 5. 計算再平衡建議
total_actual = sum(current_values.values())
data = []
for asset, config in ALLOCATION.items():
    target_pct = config['pct']
    threshold = config['threshold']
    target_val = total_actual * target_pct
    actual_val = current_values[asset]
    diff = target_val - actual_val
    actual_pct = (actual_val / total_actual) if total_actual > 0 else 0
    
    # 判斷是否觸發再平衡 (偏離比例佔目標比例的百分比)
    is_triggered = abs(actual_pct - target_pct) > (threshold * target_pct)
    
    data.append({
        "資產名稱": asset,
        "目前比例": f"{round(actual_pct*100, 2)}%",
        "需調整 (萬)": round(diff, 2),
        "狀態": "🚩 觸發" if is_triggered else "✅ 正常",
        "指令": "🔼 買入" if diff > 0 else "🔽 賣出"
    })

# 6. 顯示再平衡表格
st.divider()
st.subheader("📊 再平衡建議表 (動態門檻監控)")
df = pd.DataFrame(data)
st.table(df)
st.info("💡 只有顯示『🚩 觸發』的項目才需要優先調整。")

# 7. 預估收益計算 (2026 預估)
st.divider()
st.subheader("💰 預估年領股息 (現金流補給)")
yields = {
    "0050": 0.03, "VXUS": 0.028, "00713": 0.07, "00878": 0.08, 
    "0056": 0.09, "00864B": 0.045, "00679B": 0.035
}

total_div = sum(current_values[asset] * yields.get(asset[:5].strip(), 0) for asset in ALLOCATION.keys())

col1, col2 = st.columns(2)
col1.metric("預計年領總額", f"{round(total_div, 2)} 萬")
col2.metric("每月平均預算", f"{round(total_div/12, 2)} 萬")

st.caption("註：利差大於 0% 代表債券市場正常化，利差越大，長債(00679B)的避險緩衝作用越明顯。")
