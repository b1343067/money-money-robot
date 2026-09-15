import streamlit as st
import plotly.graph_objects as go

# 縮小整體網頁的邊距，適合手機版顯示
st.set_page_config(page_title="AI 理財分析", layout="centered")

# ==========================================
# 初始化狀態 (決定現在要顯示問卷，還是顯示結果)
# ==========================================
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# ==========================================
# 畫面 1：只顯示問卷 (還沒按下的時候)
# ==========================================
if not st.session_state.submitted:
    
    st.markdown("### AI 理財分析系統")
    st.caption("請根據真實狀況填寫，系統將為您量身打造資產配置。")
    st.write("") # 空行換行
    
    # 把標題縮小，拿掉 Step 1
    st.markdown("#### 💰 財務能力 (Capacity)")
    q1 = st.radio("1. 若下個月突然面臨相當於「兩個月薪水」的意外開銷，您會如何應對？", 
                  ["必須變賣投資或借貸", "動用存款，但會感到吃力", "輕鬆用閒置資金支付"])
    q2 = st.radio("2. 在總支出中，「無法妥協的固定開銷」大約佔比？", 
                  ["超過 70% (現金流緊繃)", "40% 到 70% (適中)", "不到 40% (極寬裕)"])

    st.markdown("#### ⚖️ 風險屬性 (Risk)")
    q3 = st.radio("3. 這筆投資資金，您預期的真正「出場時機」是？", 
                  ["3年內 (如需買房頭期)", "3到10年 (中期計畫)", "10年以上 (長期/退休)"])
    q4 = st.radio("4. 假設投資 100 萬，發現虧損 25%，您的直覺反應是？", 
                  ["自我懷疑，立刻停損出場", "放著不管，等待漲回來", "檢查基本面，沒變就加碼"])

    st.markdown("#### 🧠 行為紀律 (Behavior)")
    q5 = st.radio("5. 當朋友炫耀買飆股賺了 50%，而您的大盤持股幾乎沒動，您會？", 
                  ["受不了，賣大盤換飆股", "有點心動，拿點錢跟風", "不為所動，堅持原本紀律"])
    q6 = st.radio("6. 您認為自己預測「未來半年大盤漲跌」的準確率有多高？", 
                  ["極高，我常精準抓到波段", "普通，偶爾會看對", "無法預測，我只相信長期"])

    st.markdown("#### ⚙️ 投資偏好設定")
    include_bonds = st.checkbox("✅ 包含【債券】(降低整體波動)", value=True)
    include_dividend = st.checkbox("✅ 包含【高股息股票】(提供穩定現金流)", value=False)
    
    st.write("")
    # 按下按鈕後，把答案存起來，並切換狀態
    if st.button("🚀 開始分析", type="primary", use_container_width=True):
        st.session_state.answers = {
            'q1': q1, 'q2': q2, 'q3': q3, 'q4': q4, 'q5': q5, 'q6': q6,
            'bonds': include_bonds, 'div': include_dividend
        }
        st.session_state.submitted = True
        st.rerun() # 重新整理畫面

# ==========================================
# 畫面 2：只顯示分析結果 (按下按鈕之後)
# ==========================================
else:
    # 讀取剛才存起來的答案
    ans = st.session_state.answers
    
    score_map = {
        "必須變賣投資或借貸": 1, "動用存款，但會感到吃力": 2, "輕鬆用閒置資金支付": 3,
        "超過 70% (現金流緊繃)": 1, "40% 到 70% (適中)": 2, "不到 40% (極寬裕)": 3,
        "3年內 (如需買房頭期)": 1, "3到10年 (中期計畫)": 2, "10年以上 (長期/退休)": 3,
        "自我懷疑，立刻停損出場": 1, "放著不管，等待漲回來": 2, "檢查基本面，沒變就加碼": 3,
        "受不了，賣大盤換飆股": 1, "有點心動，拿點錢跟風": 2, "不為所動，堅持原本紀律": 3,
        "極高，我常精準抓到波段": 1, "普通，偶爾會看對": 2, "無法預測，我只相信長期": 3 
    }

    cap_score = score_map[ans['q1']] + score_map[ans['q2']]
    risk_score = score_map[ans['q3']] + score_map[ans['q4']]
    beh_score = score_map[ans['q5']] + score_map[ans['q6']]
    total_score = cap_score + risk_score + beh_score
    
    st.markdown("### 🎯 分析結果與配置建議")
    
    # 畫雷達圖
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=[cap_score, risk_score, beh_score],
        theta=['財務能力', '風險屬性', '行為紀律'],
        fill='toself', marker=dict(color='#00ff88'), fillcolor='rgba(0, 255, 136, 0.3)'
    ))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 6])), showlegend=False, margin=dict(l=30, r=30, t=30, b=30))
    st.plotly_chart(fig_radar, use_container_width=True)

    # 動態決定防禦部位
    defense_label = "現金與活儲"
    defense_color = "#E0E0E0"
    if ans['bonds']:
        defense_label = "固定收益 (避險債券)"
        defense_color = "#82CAFF"
    elif ans['div']:
        defense_label = "防禦型股票 (高股息)"
        defense_color = "#FFD700"

    # 顯示判定結果
    if total_score >= 14:
        st.success("⭐ 系統判定：【積極成長型】")
        allocations = [defense_label, "大盤股票", "科技成長股"]
        values = [20, 50, 30]
        colors = [defense_color, "#00BFFF", "#FF69B4"]
    elif total_score >= 9:
        st.info("⭐ 系統判定：【穩健平衡型】")
        allocations = [defense_label, "大盤股票", "科技成長股"]
        values = [40, 50, 10]
        colors = [defense_color, "#00BFFF", "#FF69B4"]
    else:
        st.warning("⭐ 系統判定：【保守防禦型】")
        allocations = [defense_label, "大盤股票"]
        values = [70, 30]
        colors = [defense_color, "#00BFFF"]

    # 畫圓餅圖
    fig_pie = go.Figure(data=[go.Pie(labels=allocations, values=values, marker=dict(colors=colors), hole=.4)])
    fig_pie.update_layout(margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # 隱藏具體標的
    with st.expander("🔍 點擊查看推薦的具體標的"):
        st.markdown("""
        *   **市值型大盤股票**：VOO (標普500 ETF)、BRK/B (波克夏)、JPM
        *   **科技成長股票**：NVDA (輝達)、GOOGL (Alphabet)、AAOI
        """)
        if ans['bonds']:
            st.markdown("*   **固定收益 (避險債券)**：BND、TLT")
        elif ans['div']:
            st.markdown("*   **防禦型股票 (高股息)**：SCHD、00878")
        else:
            st.markdown("*   **防禦部位 (現金)**：高利活存")

    st.write("")
    # 提供重新測驗的按鈕
    if st.button("🔄 重新測驗", use_container_width=True):
        st.session_state.submitted = False
        st.rerun()
