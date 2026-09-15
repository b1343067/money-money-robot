import streamlit as st
import plotly.graph_objects as go

# 設定為 centered 更適合手機版單手滑動閱覽
st.set_page_config(page_title="AI 投資風險評估", layout="centered")

# ==========================================
# 模擬 AI NLP 情緒與行為分析引擎
# ==========================================
def analyze_behavior(t1, t2):
    """根據輸入的文字，計算四個情緒指標，並判定狀態與提醒"""
    text = (t1 + " " + t2).lower()
    
    # 預設基礎分數 (0-100)
    anx, loss_av, conf, herd = 20, 30, 50, 30
    state = "情緒平穩 (Neutral)"
    alert = "✅ 目前情緒狀態穩定，展現長期投資紀律，未偵測到極端行為偏誤。"

    # 關鍵字判定邏輯
    if any(w in text for w in ["怕", "賣", "擔心", "焦慮", "虧", "恐慌", "睡不著", "壓力"]):
        anx, loss_av, conf, herd = 85, 90, 20, 40
        state = "高度焦慮與損失規避 (High Anxiety & Loss Aversion)"
        alert = "⚠️ 【AI 行為提醒】偵測到強烈的損失規避心理。在市場波動時，您極易發生「恐慌性拋售 (Panic Selling)」，建議提高防禦資產部位。"
    elif any(w in text for w in ["加碼", "買", "抄底", "all in", "歐印", "滿倉", "機會", "不甘心"]):
        anx, loss_av, conf, herd = 15, 20, 95, 50
        state = "過度自信 (Overconfidence)"
        alert = "⚠️ 【AI 行為提醒】偵測到過度自信特徵。您可能會低估下行風險並進行過度集中或槓桿交易，建議設定嚴格的停損紀律。"
    elif any(w in text for w in ["朋友", "別人", "大家", "跟", "聽說", "不是滋味", "羨慕"]):
        anx, loss_av, conf, herd = 60, 40, 40, 85
        state = "從眾傾向與錯失恐懼 (Herding & FOMO)"
        alert = "⚠️ 【AI 行為提醒】易受外界雜訊與他人獲利影響 (FOMO)。缺乏獨立判斷容易導致「追高殺低」，建議回歸原本設定的投資目標。"
    elif text.strip() == "":
        state = "數據不足 (Insufficient Data)"
        alert = "請輸入對話以啟動 AI 情緒行為偵測。"
        anx, loss_av, conf, herd = 0, 0, 0, 0

    return anx, loss_av, conf, herd, state, alert

# ==========================================
# 介面設計：無縫式問卷 (拿掉 1, 2, 3 的標籤)
# ==========================================
st.markdown("## 📊 Investor Risk Assessment")
st.caption("從數據與對話，理解每一位投資人")
st.markdown("---")

if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False

if not st.session_state.analyzed:
    
    # --- 基本與財務條件 (混合在一起，不分區塊) ---
    st.markdown("#### 客觀條件評估")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("年齡 (Age)", min_value=18, max_value=100, value=30)
        goal = st.selectbox("投資目標 (Financial Goal)", ["資產保值", "穩定收息", "長期資本成長", "追求絕對高報酬"])
        horizon = st.selectbox("投資期限 (Investment Horizon)", ["1年內", "1-3年", "3-10年", "10年以上"])
    with col2:
        income = st.selectbox("收入與現金流 (Income/Cash Flow)", ["吃緊 (入不敷出)", "穩定 (每月有結餘)", "寬裕 (高儲蓄率)"])
        assets = st.selectbox("可投資資產 (Investable Assets)", ["50萬以下", "50-300萬", "300萬以上"])
        loss_cap = st.selectbox("損失承受能力 (Loss Capacity)", ["無法承受本金虧損", "最多承受 -10%", "可承受 -20% 到 -30%", "可承受 -50% 甚至歸零"])

    st.write("") # 換行
    
    # --- 開放式對話區 ---
    st.markdown("#### AI 對話與行為分析")
    st.info("💡 請用文字描述您的真實感受，AI 將藉此分析您的潛在行為偏誤：")
    nlp1 = st.text_area("Q1: 如果您的投資組合在一個月內無預警下跌 20%，您當下會怎麼做？為什麼？", placeholder="請輸入您的真實想法...")
    nlp2 = st.text_area("Q2: 假設您的朋友靠著飆股一個月賺了 30%，而您的績效只有 5%，您有什麼感受？", placeholder="請輸入您的真實想法...")

    st.write("")
    if st.button("🧠 產生動態投資人風險畫像", type="primary", use_container_width=True):
        st.session_state.data = {
            "age": age, "goal": goal, "horizon": horizon, "loss_cap": loss_cap,
            "income": income, "assets": assets,
            "nlp1": nlp1, "nlp2": nlp2
        }
        st.session_state.analyzed = True
        st.rerun()

else:
    # ==========================================
    # 輸出：完全對齊投影片右側的 Dynamic Profile
    # ==========================================
    d = st.session_state.data
    
    # 1. 運算 Baseline Risk (基線風險) - 根據客觀條件算出來，而不是自己選！
    base_score = 0
    if d["age"] < 40: base_score += 2
    if d["horizon"] in ["3-10年", "10年以上"]: base_score += 2
    if d["loss_cap"] in ["可承受 -20% 到 -30%", "可承受 -50% 甚至歸零"]: base_score += 3
    if d["loss_cap"] == "無法承受本金虧損": base_score -= 5 # 絕對防禦機制
    
    if base_score <= 1: baseline_type = "保守型 (Conservative)"
    elif base_score <= 4: baseline_type = "穩健型 (Moderate)"
    else: baseline_type = "積極型 (Aggressive)"

    # 2. 運算情緒指標
    anx, loss_av, conf, herd, state, alert = analyze_behavior(d["nlp1"], d["nlp2"])

    # --- 畫面開始 ---
    st.markdown("## 🔮 Dynamic Investor Risk Profile")
    st.caption("動態投資人風險畫像報告")
    st.markdown("---")
    
    # 區塊 1：靜態基線
    st.markdown("#### 📊 Baseline Risk (模型基礎承受度)")
    st.info(f"系統根據您的年齡、財務能力與投資期限，客觀判定您的基礎屬性為：**{baseline_type}**")
    
    # 區塊 2：情緒狀態與指標
    st.markdown("#### ❤️ Current Emotional State (當下情緒狀態)")
    st.error(f"**{state}**")
    
    st.markdown("##### 行為/情緒指標 (Behavioral Indicators)")
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        st.write("😨 焦慮程度 (Anxiety)")
        st.progress(anx / 100)
        st.write("📉 損失規避 (Loss Aversion)")
        st.progress(loss_av / 100)
    with col_i2:
        st.write("😎 自信程度 (Confidence)")
        st.progress(conf / 100)
        st.write("🐑 從眾傾向 (Herding)")
        st.progress(herd / 100)

    # 區塊 3：行為提醒
    st.markdown("#### ⚙️ Behavioral Alert (行為提醒)")
    st.warning(alert)
    
    st.markdown("---")

    # 區塊 4：即時建議與動態配置 (不出現特定股票)
    st.markdown("#### 💡 更個人化、更即時的投資建議")
    st.write("AI 已整合您的「基礎財務條件」與「當下行為情緒」，即時動態調整您的資產配置：")
    
    # 動態介入邏輯
    if "焦慮" in state:
        allocations = ["防禦型資產 (現金/定存)", "核心部位 (大盤指數)"]
        values = [60, 40]
        colors = ["#E0E0E0", "#00BFFF"]
    elif "過度自信" in state or "從眾" in state:
        allocations = ["防禦型資產 (現金/定存)", "核心部位 (大盤指數)", "衛星部位 (成長型/科技型)"]
        values = [30, 50, 20]
        colors = ["#E0E0E0", "#00BFFF", "#FF69B4"]
    else:
        allocations = ["防禦型資產 (現金/定存)", "核心部位 (大盤指數)", "衛星部位 (成長型/科技型)"]
        if baseline_type == "保守型 (Conservative)":
            values = [50, 50, 0]
        elif baseline_type == "穩健型 (Moderate)":
            values = [20, 60, 20]
        else:
            values = [10, 50, 40]
        colors = ["#E0E0E0", "#00BFFF", "#FF69B4"]

    fig_pie = go.Figure(data=[go.Pie(labels=allocations, values=values, marker=dict(colors=colors), hole=.4)])
    fig_pie.update_layout(margin=dict(l=20, r=20, t=10, b=10), height=300)
    st.plotly_chart(fig_pie, use_container_width=True)

    st.write("")
    if st.button("🔄 重新進行對話評估", use_container_width=True):
        st.session_state.analyzed = False
        st.rerun()
