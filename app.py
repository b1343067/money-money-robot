import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Dynamic Risk Profile", layout="centered")

# ==========================================
# NLP 模擬引擎 (極簡版，無多餘廢話)
# ==========================================
def analyze_nlp(t1, t2, t3):
    text = (t1 + t2 + t3).lower()
    
    if not text.strip():
        return 0, 0, 0, 0, "無數據", "無"

    # 關鍵字判定
    if any(w in text for w in ["怕", "賣", "擔心", "焦慮", "虧", "恐慌", "睡不著"]):
        return 85, 90, 20, 40, "高度焦慮 / 損失規避", "留意恐慌性拋售風險，建議提高防禦資產。"
    elif any(w in text for w in ["加碼", "買", "抄底", "機會", "歐印", "滿倉"]):
        return 15, 20, 90, 50, "過度自信", "留意過度集中與槓桿風險，嚴守停損紀律。"
    elif any(w in text for w in ["朋友", "別人", "跟", "羨慕", "不是滋味", "換"]):
        return 65, 40, 50, 85, "從眾傾向 / FOMO", "易受外界雜訊影響，留意追高殺低風險。"
    else:
        return 20, 30, 50, 20, "情緒平穩", "無極端偏誤，維持長期投資紀律。"

# ==========================================
# 介面設計：輸入區 (對齊 Image 8 & 9)
# ==========================================
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False

if not st.session_state.analyzed:
    
    st.markdown("### 3️⃣ Financial Capacity 財務條件")
    inc = st.selectbox("💰 收入與現金流 (Income / Cash Flow)", ["穩定正向", "收支打平", "入不敷出"])
    ast = st.selectbox("💼 可投資資產 (Investable Assets)", ["50萬以下", "50-300萬", "300萬以上"])
    liq = st.selectbox("🏠 流動性需求 (Liquidity Need)", ["高 (隨時需要變現)", "中 (偶有資金需求)", "低 (閒置資金)"])
    hor = st.selectbox("📅 投資期限 (Time Horizon)", ["1年內", "1-3年", "3-10年", "10年以上"])
    lia = st.selectbox("🧾 負債狀況 (Liabilities)", ["無負債", "可控負債 (如房貸)", "高負債壓力"])
    
    st.markdown("---")
    
    st.markdown("### 2️⃣ Behavioral & Emotional Assessment 行為/情緒評估")
    q1 = st.text_area("如果您的投資組合一個月下跌 20%，您會怎麼做？為什麼？")
    q2 = st.text_area("最近市場波動很大，您目前對自己的投資有什麼感受？")
    q3 = st.text_area("如果您的朋友靠 AI 股票賺了 30%，而您的投資只有 5%，您會怎麼做？")

    st.write("")
    if st.button("Generate Dynamic Profile", type="primary", use_container_width=True):
        st.session_state.data = {"inc":inc, "ast":ast, "liq":liq, "hor":hor, "lia":lia, "q1":q1, "q2":q2, "q3":q3}
        st.session_state.analyzed = True
        st.rerun()

# ==========================================
# 介面設計：輸出區 (完全對齊 Image 10)
# ==========================================
else:
    d = st.session_state.data
    
    # 1. 計算 Baseline
    score = 0
    if d["inc"] == "穩定正向": score += 1
    if d["ast"] in ["50-300萬", "300萬以上"]: score += 1
    if d["liq"] == "低 (閒置資金)": score += 1
    if d["hor"] in ["3-10年", "10年以上"]: score += 1
    if d["lia"] == "無負債": score += 1
    
    if score <= 2: baseline = "保守型 (Conservative)"
    elif score <= 4: baseline = "穩健型 (Moderate)"
    else: baseline = "積極型 (Aggressive)"

    # 2. 獲取 NLP 結果
    anx, loss, conf, herd, state, alert = analyze_nlp(d["q1"], d["q2"], d["q3"])

    # --- 畫面渲染 (無多餘廢話) ---
    st.markdown("## Dynamic Investor Risk Profile")
    st.markdown("### 動態投資人風險畫像")
    st.markdown("---")

    # Image 10: 三大指標
    st.markdown(f"#### 📊 Baseline Risk (長期風險承受度)\n**{baseline}**")
    st.write("")
    st.markdown(f"#### ❤️ Current Emotional State (當下情緒狀態)\n**{state}**")
    st.write("")
    st.markdown(f"#### ⚙️ Behavioral Alert (行為提醒)\n**{alert}**")
    
    st.markdown("---")

    # Image 8 底部: 四個情緒指標
    st.markdown("**行為 / 情緒指標**")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.write("😨 焦慮")
        st.progress(anx / 100)
    with c2:
        st.write("📉 損失規避")
        st.progress(loss / 100)
    with c3:
        st.write("😎 自信程度")
        st.progress(conf / 100)
    with c4:
        st.write("🐑 從眾傾向")
        st.progress(herd / 100)
        
    st.markdown("---")

    # Image 10 底部: 投資建議圖表
    st.markdown("#### 💡 更個人化、更即時的投資建議")
    
    # 根據情緒動態分配 (無廢話，直接給圖)
    labels = ["防禦資產 (現金/定存)", "核心部位 (大盤指數)", "衛星部位 (成長型/科技)"]
    if "焦慮" in state:
        vals, cols = [60, 40, 0], ["#E0E0E0", "#00BFFF", "#FF69B4"]
    elif "自信" in state or "從眾" in state:
        vals, cols = [20, 40, 40], ["#E0E0E0", "#00BFFF", "#FF69B4"]
    else:
        if baseline == "保守型 (Conservative)": vals = [60, 40, 0]
        elif baseline == "穩健型 (Moderate)": vals = [30, 50, 20]
        else: vals = [10, 60, 30]
        cols = ["#E0E0E0", "#00BFFF", "#FF69B4"]

    fig = go.Figure(data=[go.Pie(labels=labels, values=vals, marker=dict(colors=cols), hole=.4)])
    fig.update_layout(margin=dict(l=0, r=0, t=20, b=0), height=300)
    st.plotly_chart(fig, use_container_width=True)

    if st.button("🔄 重新測驗", use_container_width=True):
        st.session_state.analyzed = False
        st.rerun()
