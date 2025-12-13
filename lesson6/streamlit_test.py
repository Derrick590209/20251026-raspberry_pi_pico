"""
Streamlit 測試應用程式
這是一個簡單的 Streamlit 範例，展示基本功能
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import random

# 設定頁面配置
st.set_page_config(
    page_title="Streamlit 測試應用",
    page_icon="🚀",
    layout="wide"
)

# 標題
st.title("🚀 Streamlit 測試應用程式")
st.write("歡迎使用 Streamlit！這是一個測試範例。")

# 分隔線
st.divider()

# 側邊欄
st.sidebar.header("⚙️ 控制面板")
user_name = st.sidebar.text_input("請輸入你的名字", "訪客")
st.sidebar.write(f"你好，{user_name}！")

# 選擇器
option = st.sidebar.selectbox(
    "選擇一個功能",
    ["首頁", "數據展示", "圖表展示", "互動測試"]
)

st.sidebar.divider()
st.sidebar.info("💡 這是一個測試應用，用於驗證 Streamlit 安裝成功。")

# 主要內容區域
if option == "首頁":
    st.header("📋 首頁")
    st.write(f"當前時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="溫度", value="25.5°C", delta="1.2°C")
    
    with col2:
        st.metric(label="濕度", value="60%", delta="-5%")
    
    with col3:
        st.metric(label="訊息數", value="42", delta="12")

elif option == "數據展示":
    st.header("📊 數據展示")
    
    # 創建範例數據
    data = {
        "時間": [f"{i:02d}:00" for i in range(0, 24, 2)],
        "溫度": [round(20 + random.uniform(-3, 3), 1) for _ in range(12)],
        "濕度": [round(60 + random.uniform(-10, 10), 1) for _ in range(12)],
    }
    df = pd.DataFrame(data)
    
    st.dataframe(df, use_container_width=True)
    
    st.download_button(
        label="📥 下載數據",
        data=df.to_csv(index=False),
        file_name="sensor_data.csv",
        mime="text/csv"
    )

elif option == "圖表展示":
    st.header("📈 圖表展示")
    
    # 創建範例數據
    chart_data = pd.DataFrame(
        {
            "溫度": [round(20 + random.uniform(-3, 3), 1) for _ in range(20)],
            "濕度": [round(60 + random.uniform(-10, 10), 1) for _ in range(20)],
        }
    )
    
    st.line_chart(chart_data)
    
    st.bar_chart(chart_data)

elif option == "互動測試":
    st.header("🎮 互動測試")
    
    # 滑動條
    temperature = st.slider("設定溫度", 0, 40, 25)
    st.write(f"當前溫度：{temperature}°C")
    
    # 按鈕
    if st.button("🎲 產生隨機數據"):
        random_temp = round(random.uniform(18, 30), 2)
        random_humidity = round(random.uniform(40, 80), 2)
        st.success(f"隨機溫度：{random_temp}°C，隨機濕度：{random_humidity}%")
    
    # 複選框
    show_details = st.checkbox("顯示詳細資訊")
    if show_details:
        st.info("""
        ### 📝 Streamlit 特性
        - 簡單易用的 Python 框架
        - 自動重新載入
        - 豐富的互動元件
        - 支援數據視覺化
        """)

# 頁尾
st.divider()
st.caption("© 2025 Streamlit 測試應用 | Raspberry Pi")


