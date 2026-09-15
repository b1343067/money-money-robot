import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Dynamic Risk Profile", layout="centered")

# ==========================================
# NLP 分析引擎 (極簡版)
# ==========================================
def analyze_nlp(t1, t2, t3):
    text = (t1 + t2 + t3).lower()
    
    if not text.strip():
        return "無數據", "請輸入對話以啟動分析", "無"

    if any(w in text for w in ["怕", "賣", "擔心", "焦慮", "虧", "恐慌", "睡不著"]):
        return "高度焦慮 / 損失規避", "留意恐慌性拋售風險，建議提高防禦資產。", "焦慮"
    elif any(w in text for w in ["加碼", "買", "抄底", "機會", "歐印", "滿倉"]):
        return "過度自信", "留意過度集中與槓桿風險，嚴守停損紀律。", "自信"
    elif any(w in text for w in ["朋友", "別人", "跟", "羨慕", "不是滋味", "換"]):
        return "從眾傾向 / FOMO", "易受外界雜訊影響，留意追高殺低風險。", "從眾"
    else:
        return "情緒平穩", "無極端偏誤，維持長期投資紀律。", "平穩"

# ==========================================
# 介面設計：輸入區 (拿掉數字標題)
# ==========================================
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False

if not st.session_state.analyzed:
    
    st.markdown("### Financial Capacity 財務條件")
    inc = st.selectbox("💰 收入與現金流 (Income / Cash Flow)", ["穩定正向", "收支打平", "入不敷出"])
    ast = st.selectbox("💼 可投資資產 (Investable Assets)", ["50萬以下", "50-300萬", "300萬以上"])
    liq = st.selectbox("🏠 流動性需求 (Liquidity Need)", ["高 (隨時需要變現)", "中 (偶有資金需求)", "低 (閒置資金)"])
    hor = st.selectbox("📅 投資期限 (Time Horizon)", ["1年內", "1-3年", "3-10年", "10年以上"])
    lia = st.selectbox("🧾 負債狀況 (Liabilities)", ["無負債", "可控負債 (如房貸)", "高負債壓力"])
    
    st.markdown("---")
    
    st.markdown("### Behavioral & Emotional Assessment 行為/情緒評估")
    q1 = st.text_area("如果您的投資組合一個月下跌 20%，您會怎麼做？為什麼？")
    q2 = st.text_area("最近市場波動很大，您目前對自己的投資有什麼感受？")
    q3 = st.text_area("如果您的朋友靠 AI 股票賺了 30%，而您的投資只有 5%，您會怎麼做？")

    st.write("")
    if st.button("Generate Dynamic Profile", type="primary", use_container_width=True):
        st.session_state.data = {"inc":inc, "ast":ast, "liq":liq, "hor":hor, "lia":lia, "q1":q1, "q2":q2, "q3":q3}
        st.session_state.analyzed = True
        st.rerun()

# ==========================================
# 介面設計：輸出區 (完美還原 圖 13)
# ==========================================
else:
    d = st.session_state.data
    
    # 計算 Baseline
    score = 0
    if d["inc"] == "穩定正向": score += 1
    if d["ast"] in ["50-300萬", "300萬以上"]: score += 1
    if d["liq"] == "低 (閒置資金)": score += 1
    if d["hor"] in ["3-10年", "10年以上"]: score += 1
    if d["lia"] == "無負債": score += 1
    
    if score <= 2: baseline = "保守型 (Conservative)"
    elif score <= 4: baseline = "穩健型 (Moderate)"
    else: baseline = "積極型 (Aggressive)"

    state, alert, logic_flag = analyze_nlp(d["q1"], d["q2"], d["q3"])

    # --- 完美還原圖 13 上半部 ---
    st.markdown("<h2 style='text-align: center;'>Dynamic Investor<br>Risk Profile<br><span style='font-size: 24px;'>動態投資人風險畫像</span></h2>", unsafe_allow_html=True)
    
    # 畫出圖 13 的「半圓形科技感儀表板」
    fig_arch = go.Figure(data=[go.Pie(
        values=[1, 1, 1, 3], # 讓下面那一半隱藏，形成完美半圓
        marker=dict(colors=['#00d2ff', '#3a7bd5', '#8e2de2', 'rgba(0,0,0,0)']),
        hole=0.75,
        rotation=90,
        direction='clockwise',
        textinfo='none', hoverinfo='none'
    )])
    fig_arch.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        height=220, showlegend=False,
        annotations=[dict(text="👤", x=0.5, y=0.35, font_size=60, showarrow=False)]
    )
    st.plotly_chart(fig_arch, use_container_width=True)

    # 圖 13 的三大文字區塊 (乾淨俐落)
    st.markdown(f"#### 📊 Baseline Risk (長期風險承受度)\n**{baseline}**")
    st.write("")
    st.markdown(f"#### ❤️ Current Emotional State (當下情緒狀態)\n**{state}**")
    st.write("")
    st.markdown(f"#### ⚙️ Behavioral Alert (行為提醒)\n**{alert}**")
    
    st.markdown("---")

    # 圖 13 下半部：即時投資建議與圓餅圖
    st.markdown("#### 💡 更個人化、更即時的投資建議")
    
    labels = ["防禦資產 (現金/定存)", "核心部位 (大盤指數)", "衛星部位 (成長型/科技)"]
    if logic_flag == "焦慮":
        vals, cols = [60, 40, 0], ["#E0E0E0", "#00BFFF", "#FF69B4"]
    elif logic_flag in ["自信", "從眾"]:
        vals, cols = [20, 40, 40], ["#E0E0E0", "#00BFFF", "#FF69B4"]
    else:
        if baseline == "保守型 (Conservative)": vals = [60, 40, 0]
        elif baseline == "穩健型 (Moderate)": vals = [30, 50, 20]
        else: vals = [10, 60, 30]
        cols = ["#E0E0E0", "#00BFFF", "#FF69B4"]

    fig_pie = go.Figure(data=[go.Pie(labels=labels, values=vals, marker=dict(colors=cols), hole=.4)])
    fig_pie.update_layout(margin=dict(l=0, r=0, t=20, b=0), height=300)
    st.plotly_chart(fig_pie, use_container_width=True)

    if st.button("🔄 重新測驗", use_container_width=True):
        st.session_state.analyzed = False
        st.rerun()
