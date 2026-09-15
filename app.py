import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="動態投資風險評估系統", layout="wide")

# ==========================================
# 模擬 NLP 情緒分析引擎 (Mock LLM Engine)
# ==========================================
def analyze_sentiment(text):
    """根據使用者的文字輸入，模擬 LLM 抓取情緒關鍵字"""
    text = text.lower()
    if any(word in text for word in ["怕", "賣", "擔心", "焦慮", "虧", "睡不著", "恐慌"]):
        return {"state": "高度焦慮 (High Anxiety)", "alert": "⚠️ 損失規避強烈，可能有恐慌拋售風險", "color": "red"}
    elif any(word in text for word in ["加碼", "買", "機會", "抄底", "借錢", "all in", "歐印"]):
        return {"state": "過度自信 (Overconfidence)", "alert": "⚠️ 具備過度自信或過度交易風險", "color": "orange"}
    elif any(word in text for word in ["朋友", "別人", "大家", "跟", "聽說"]):
        return {"state": "從眾傾向 (Herding)", "alert": "⚠️ 易受他人影響，缺乏獨立判斷(FOMO)", "color": "orange"}
    elif text == "":
        return {"state": "未提供數據", "alert": "缺乏足夠對話數據", "color": "gray"}
    else:
        return {"state": "情緒平穩 (Neutral)", "alert": "✅ 展現長期紀律與理性", "color": "green"}

# ==========================================
# 介面設計：還原老師的投影片架構
# ==========================================
st.markdown("## 📊 Investor Risk Assessment")
st.caption("從數據與對話，理解每一位投資人 (From Data to a Better Financial Life)")
st.markdown("---")

if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False

if not st.session_state.analyzed:
    # 建立三個區塊 (對應投影片的 1, 2, 3)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### ❶ 傳統風險評估")
        st.caption("結構化問卷取得相對穩定資訊")
        age = st.slider("年齡 (Age)", 18, 80, 30)
        goal = st.selectbox("投資目標 (Financial Goal)", ["資產保值", "穩定收息", "長期資本利得", "短期高報酬"])
        risk_tol = st.select_slider("風險偏好 (Risk Tolerance)", options=["極保守", "保守", "穩健", "積極", "極積極"], value="穩健")

    with col3: # 先排版第3區，因為都是選擇題
        st.markdown("### ❸ 財務條件")
        st.caption("評估實際的財務能力與限制條件")
        income = st.selectbox("年收入水平 (Income)", ["50萬以下", "50-100萬", "100-200萬", "200萬以上"])
        liquidity = st.selectbox("緊急預備金 (Liquidity)", ["不足3個月", "3-6個月", "6個月以上"])
        horizon = st.selectbox("投資期限 (Time Horizon)", ["1年內", "1-3年", "3-10年", "10年以上"])

    with col2:
        st.markdown("### ❷ 行為/情緒評估")
        st.caption("透過開放式問題與 LLM 進行對話分析")
        st.info("💡 請用文字描述您的真實想法：")
        nlp_input_1 = st.text_area("Q1: 如果您的投資組合一個月下跌 20%，您會怎麼做？為什麼？", placeholder="例如：我會很害怕，想趕快賣掉...")
        nlp_input_2 = st.text_area("Q2: 如果您的朋友靠 AI 股票賺了 30%，而您的績效只有 5%，您有什麼感受？", placeholder="例如：我會覺得很不是滋味，想跟著買...")

    st.markdown("---")
    if st.button("🧠 啟動 AI 動態畫像分析 (Generate Dynamic Profile)", type="primary", use_container_width=True):
        # 儲存輸入狀態
        st.session_state.data = {
            "risk_tol": risk_tol, "liquidity": liquidity,
            "nlp1": nlp_input_1, "nlp2": nlp_input_2
        }
        st.session_state.analyzed = True
        st.rerun()

else:
    # ==========================================
    # 輸出：Dynamic Investor Risk Profile
    # ==========================================
    data = st.session_state.data
    
    # 1. 計算 Baseline Risk (基於傳統+財務)
    baseline_score = {"極保守": 1, "保守": 2, "穩健": 3, "積極": 4, "極積極": 5}[data["risk_tol"]]
    if data["liquidity"] == "不足3個月": 
        baseline_score = max(1, baseline_score - 1) # 財務條件差，強降評
        
    baseline_type = ["保守型 (Conservative)", "保守型 (Conservative)", "穩健型 (Moderate)", "積極型 (Aggressive)", "極限積極型 (Highly Aggressive)"][baseline_score-1]

    # 2. 執行 NLP 情緒分析 (分析使用者的打字)
    sentiment_1 = analyze_sentiment(data["nlp1"])
    sentiment_2 = analyze_sentiment(data["nlp2"])

    st.markdown("## 🔮 動態投資人風險畫像 (Dynamic Investor Risk Profile)")
    st.markdown("---")
    
    res_col1, res_col2 = st.columns([1, 1.5])
    
    with res_col1:
        st.subheader("📊 模型基礎承受度 (Baseline Risk)")
        st.metric(label="靜態風險屬性", value=baseline_type)
        
        st.subheader("❤️ 當下情緒狀態 (Current Emotional State)")
        st.markdown(f"**面對市場暴跌：** <span style='color:{sentiment_1['color']}'>{sentiment_1['state']}</span>", unsafe_allow_html=True)
        st.markdown(f"**面對他人獲利：** <span style='color:{sentiment_2['color']}'>{sentiment_2['state']}</span>", unsafe_allow_html=True)
        
        st.subheader("⚙️ 行為提醒 (Behavioral Alert)")
        st.warning(sentiment_1['alert'])
        st.warning(sentiment_2['alert'])

    with res_col2:
        st.subheader("💡 更個人化、更即時的投資建議")
        
        # 結合你喜歡的 VOO/NVDA 策略，並根據情緒動態調整
        st.write("根據您的 **基線財務能力** 與 **當下 NLP 偵測之情緒特徵**，系統即時調整配置：")
        
        if "焦慮" in sentiment_1["state"]:
            st.error("🚨 【AI 動態介入】偵測到您目前對市場下行極度焦慮，系統強制調降高波動科技股比例，拉高現金水位以穩定心理壓力。")
            allocations = ["現金與定存 (防禦)", "VOO 大盤指數 (核心)"]
            values = [60, 40]
            colors = ["#E0E0E0", "#00BFFF"]
        elif "自信" in sentiment_1["state"] or "自信" in sentiment_2["state"]:
            st.warning("⚠️ 【AI 動態介入】偵測到過度自信或FOMO情緒，為防止過度槓桿，系統建議保留紀律性現金。")
            allocations = ["現金與定存 (防禦)", "VOO 大盤指數 (核心)", "NVDA/AI 科技股 (衛星)"]
            values = [30, 50, 20]
            colors = ["#E0E0E0", "#00BFFF", "#FF69B4"]
        else:
            st.success("✅ 【AI 動態介入】情緒平穩，可承受較高波動，建議執行您原定的成長型核心衛星策略。")
            allocations = ["現金與定存 (防禦)", "VOO 大盤指數 (核心)", "NVDA/AI 科技股 (衛星)"]
            values = [10, 60, 30]
            colors = ["#E0E0E0", "#00BFFF", "#FF69B4"]

        fig_pie = go.Figure(data=[go.Pie(labels=allocations, values=values, marker=dict(colors=colors), hole=.4)])
        fig_pie.update_layout(margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_pie, use_container_width=True)

    if st.button("🔄 重新進行對話評估"):
        st.session_state.analyzed = False
        st.rerun()
