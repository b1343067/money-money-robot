import streamlit as st
import plotly.graph_objects as go
import json
from datetime import datetime

# ==========================================
# 1. 頁面基本設定
# ==========================================
st.set_page_config(page_title="AI 理財機器人", layout="wide")
st.title("🤖 AI-Assisted Digital Investor Profiling System")
st.markdown("---")

# ==========================================
# 2. 問卷區 (包含偏好設定)
# ==========================================
st.header("Step 1: 投資人屬性與偏好評估")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("💰 財務能力 (Capacity)")
    q1 = st.radio("1. 若下個月突然面臨相當於「兩個月薪水」的意外開銷，您會如何應對？", 
                  ["必須變賣投資或借貸", "動用存款，但會感到吃力", "輕鬆用閒置資金支付"])
    q2 = st.radio("2. 在您的總支出中，「無法妥協的固定開銷」大約佔比？", 
                  ["超過 70% (現金流緊繃)", "40% 到 70% (適中)", "不到 40% (極寬裕)"])

with col2:
    st.subheader("⚖️ 風險屬性 (Risk)")
    q3 = st.radio("3. 這筆投資資金，您預期的真正「出場時機」是？", 
                  ["3年內 (如需買房頭期)", "3到10年 (中期計畫)", "10年以上 (長期/退休)"])
    q4 = st.radio("4. 假設投資 100 萬，某天打開帳戶發現虧損 25%，您的直覺反應是？", 
                  ["自我懷疑，立刻停損出場", "放著不管，等待漲回來", "檢查基本面，沒變就加碼"])

with col3:
    st.subheader("🧠 行為紀律 (Behavior)")
    q5 = st.radio("5. 當朋友炫耀買飆股賺了 50%，而您的大盤持股幾乎沒動，您會？", 
                  ["受不了，賣大盤換飆股", "有點心動，拿點錢跟風", "不為所動，堅持原本紀律"])
    q6 = st.radio("6. 您認為自己預測「未來半年股市大盤漲跌」的準確率有多高？", 
                  ["極高，我常精準抓到波段", "普通，偶爾會看對", "無法預測，我只相信長期"])

st.markdown("---")
# ===== 新增：資產偏好設定區 =====
st.subheader("⚙️ 投資偏好設定 (Preferences)")
st.caption("請根據您的個人喜好，勾選是否允許系統將以下資產納入您的投資組合：")
pref_col1, pref_col2 = st.columns(2)
with pref_col1:
    include_bonds = st.checkbox("✅ 包含【債券】 (降低整體波動，提供絕對防禦力)", value=True)
with pref_col2:
    include_dividend = st.checkbox("✅ 包含【高股息股票】 (提供穩定現金流，具備相對防禦力)", value=False)

st.markdown("---")

# ==========================================
# 3. 計分與分析邏輯
# ==========================================
score_map = {
    "必須變賣投資或借貸": 1, "動用存款，但會感到吃力": 2, "輕鬆用閒置資金支付": 3,
    "超過 70% (現金流緊繃)": 1, "40% 到 70% (適中)": 2, "不到 40% (極寬裕)": 3,
    "3年內 (如需買房頭期)": 1, "3到10年 (中期計畫)": 2, "10年以上 (長期/退休)": 3,
    "自我懷疑，立刻停損出場": 1, "放著不管，等待漲回來": 2, "檢查基本面，沒變就加碼": 3,
    "受不了，賣大盤換飆股": 1, "有點心動，拿點錢跟風": 2, "不為所動，堅持原本紀律": 3,
    "極高，我常精準抓到波段": 1, "普通，偶爾會看對": 2, "無法預測，我只相信長期": 3 
}

if st.button("🚀 Analyze My Profile", type="primary", use_container_width=True):
    
    st.markdown("---")
    st.header("Step 2: AI 分析結果與配置建議")
    
    cap_score = score_map[q1] + score_map[q2]
    risk_score = score_map[q3] + score_map[q4]
    beh_score = score_map[q5] + score_map[q6]
    total_score = cap_score + risk_score + beh_score
    
    res_col1, res_col2 = st.columns([1, 1.2])
    
    with res_col1:
        st.subheader("📊 投資人多維度屬性")
        # 雷達圖
        fig_radar = go.Figure(data=go.Scatterpolar(
          r=[cap_score, risk_score, beh_score],
          theta=['財務能力 (Capacity)', '風險屬性 (Risk)', '行為紀律 (Behavior)'],
          fill='toself', marker=dict(color='#00ff88'), fillcolor='rgba(0, 255, 136, 0.3)'
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 6])), showlegend=False, margin=dict(l=40, r=40, t=20, b=20))
        st.plotly_chart(fig_radar, use_container_width=True)

    with res_col2:
        st.subheader("🎯 專屬資產配置建議")
        
        # 動態決定「防禦部位」的類別與比例
        defense_label = "現金與活儲"
        defense_color = "#E0E0E0"
        if include_bonds:
            defense_label = "固定收益 (避險債券)"
            defense_color = "#82CAFF"
        elif include_dividend:
            defense_label = "防禦型股票 (高股息)"
            defense_color = "#FFD700"

        # 根據總分決定比例
        if total_score >= 14:
            st.success("⭐ 系統判定：【積極成長型】")
            allocations = [defense_label, "市值型大盤股票", "科技成長股票"]
            values = [20, 50, 30]
            colors = [defense_color, "#00BFFF", "#FF69B4"]
        elif total_score >= 9:
            st.info("⭐ 系統判定：【穩健平衡型】")
            allocations = [defense_label, "市值型大盤股票", "科技成長股票"]
            values = [40, 50, 10]
            colors = [defense_color, "#00BFFF", "#FF69B4"]
        else:
            st.warning("⭐ 系統判定：【保守防禦型】")
            allocations = [defense_label, "市值型大盤股票"]
            values = [70, 30]
            colors = [defense_color, "#00BFFF"]

        # 畫出超美的資產配置圓餅圖
        fig_pie = go.Figure(data=[go.Pie(labels=allocations, values=values, marker=dict(colors=colors), hole=.4)])
        fig_pie.update_layout(margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # 使用 Expander 隱藏具體標的，想看的人再點開
        with st.expander("🔍 點擊查看推薦的「具體標的範例」"):
            st.markdown("""
            此為系統根據上述資產類別，為您挑選的標的範例 (僅供參考)：
            *   **市值型大盤股票**：VOO (標普500 ETF)、BRK/B (波克夏)
            *   **科技成長股票**：NVDA (輝達)、GOOGL (Alphabet)、AAOI
            """)
            if include_bonds:
                st.markdown("*   **固定收益 (避險債券)**：BND (美國綜合債券 ETF)、TLT (美國長天期公債)")
            elif include_dividend:
                st.markdown("*   **防禦型股票 (高股息)**：SCHD (美股高股息 ETF)、00878 (台股高股息 ETF)")
            else:
                st.markdown("*   **防禦部位 (現金)**：數位帳戶高利活存、美元定存")
