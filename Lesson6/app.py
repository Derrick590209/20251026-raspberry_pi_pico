"""
MQTT 數據監控儀表板 - Streamlit 應用程式
根據 PRD.md 規格實作
"""
import streamlit as st
import time
import pandas as pd
from pathlib import Path
from mqtt_client import MQTTClient
from data_handler import DataHandler


# 頁面配置
st.set_page_config(
    page_title="MQTT 數據監控儀表板",
    page_icon="📊",
    layout="wide"
)

# 初始化 Session State
if 'mqtt_client' not in st.session_state:
    st.session_state.mqtt_client = None
if 'data_handler' not in st.session_state:
    st.session_state.data_handler = DataHandler(data_dir="data")
    
# 初始化當前數據（載入最後一筆數據作為初始顯示）
if 'current_data' not in st.session_state:
    # 載入最後一筆數據作為初始顯示
    all_data = st.session_state.data_handler.get_all_data()
    if not all_data.empty:
        last_row = all_data.iloc[-1]
        st.session_state.current_data = {
            'light': last_row.get('light', 'unknown') if pd.notna(last_row.get('light')) else 'unknown',
            'temperature': float(last_row.get('temperature')) if pd.notna(last_row.get('temperature')) else None,
            'humidity': float(last_row.get('humidity')) if pd.notna(last_row.get('humidity')) else None,
            'last_update': last_row.get('timestamp')
        }
    else:
        st.session_state.current_data = {
            'light': 'unknown',
            'temperature': None,
            'humidity': None,
            'last_update': None
        }
if 'data_updated' not in st.session_state:
    st.session_state.data_updated = False


def on_mqtt_message(topic, payload, data):
    """MQTT 訊息接收回呼函數"""
    # 解析數據（data 可能是已解析的 JSON 字典或 None）
    # data_handler.parse_message 可以接受字典或 JSON 字串
    if data is not None:
        parsed_data = st.session_state.data_handler.parse_message(data)
    else:
        parsed_data = st.session_state.data_handler.parse_message(payload)
    
    if parsed_data:
        # 更新當前數據
        st.session_state.current_data = {
            'light': parsed_data.get('light', 'unknown'),
            'temperature': parsed_data.get('temperature'),
            'humidity': parsed_data.get('humidity'),
            'last_update': parsed_data.get('timestamp')
        }
        
        # 儲存數據
        st.session_state.data_handler.add_data(parsed_data)
        
        # 標記需要更新 UI
        st.session_state.data_updated = True


def init_mqtt_client():
    """初始化 MQTT 客戶端"""
    if st.session_state.mqtt_client is None:
        mqtt_client = MQTTClient(
            broker_host="localhost",
            broker_port=1883,
            topic="客廳",
            on_message_callback=on_mqtt_message
        )
        
        if mqtt_client.connect():
            st.session_state.mqtt_client = mqtt_client
            return True
        else:
            return False
    return st.session_state.mqtt_client.is_connected()


def disconnect_mqtt():
    """斷開 MQTT 連接"""
    if st.session_state.mqtt_client:
        st.session_state.mqtt_client.disconnect()
        st.session_state.mqtt_client = None


# 主頁面
st.title("📊 MQTT 數據監控儀表板")
st.markdown("---")

# 側邊欄 - 連接控制
with st.sidebar:
    st.header("⚙️ 連接設定")
    
    # MQTT 連接狀態
    if st.session_state.mqtt_client and st.session_state.mqtt_client.is_connected():
        st.success("✓ 已連接")
        status = st.session_state.mqtt_client.get_status()
        
        st.info(f"""
        **主題**: {status['topic']}  
        **接收訊息數**: {status['messages_received']}  
        **最後更新**: {status['last_message_time'] or '無'}
        """)
        
        if st.button("🔌 斷開連接", type="secondary"):
            disconnect_mqtt()
            st.rerun()
    else:
        st.warning("⚠️ 未連接")
        
        if st.button("🔗 連接 MQTT", type="primary"):
            if init_mqtt_client():
                st.success("連接成功！")
                st.rerun()
            else:
                st.error("連接失敗，請檢查 MQTT Broker 是否運行")
    
    st.markdown("---")
    st.header("📋 說明")
    st.caption("""
    此應用程式會訂閱 MQTT 主題「客廳」，
    接收並顯示環境監控數據。
    所有數據會自動儲存到 Excel 檔案。
    """)
    
    # 顯示數據統計
    all_data = st.session_state.data_handler.get_all_data()
    if not all_data.empty:
        st.markdown("---")
        st.markdown("**📊 數據統計**")
        st.caption(f"Excel 檔案中共有 **{len(all_data)}** 筆記錄")
        if 'timestamp' in all_data.columns and len(all_data) > 0:
            min_time = all_data['timestamp'].min()
            max_time = all_data['timestamp'].max()
            if pd.notna(min_time) and pd.notna(max_time):
                st.caption(f"時間範圍：{min_time.strftime('%Y-%m-%d %H:%M')} 至 {max_time.strftime('%Y-%m-%d %H:%M')}")


# 主要內容區域
col1, col2, col3 = st.columns(3)

# 電燈狀態顯示
with col1:
    st.subheader("💡 電燈狀態")
    light_status = st.session_state.current_data['light']
    
    if light_status == 'on' or light_status == '開':
        st.success("🟢 開")
    elif light_status == 'off' or light_status == '關':
        st.error("🔴 關")
    else:
        st.info("⚪ 未知")
    
    st.caption(f"狀態: {light_status}")

# 溫度顯示
with col2:
    st.subheader("🌡️ 客廳溫度")
    temperature = st.session_state.current_data['temperature']
    
    if temperature is not None:
        st.metric("溫度", f"{temperature:.1f} °C")
    else:
        st.info("等待數據...")
    
    st.caption("即時監控")

# 濕度顯示
with col3:
    st.subheader("💧 客廳濕度")
    humidity = st.session_state.current_data['humidity']
    
    if humidity is not None:
        st.metric("濕度", f"{humidity:.1f} %")
    else:
        st.info("等待數據...")
    
    st.caption("即時監控")

st.markdown("---")

# 最後更新時間
if st.session_state.current_data['last_update']:
    last_update = st.session_state.current_data['last_update']
    if isinstance(last_update, str):
        st.caption(f"最後更新時間: {last_update}")
    else:
        st.caption(f"最後更新時間: {last_update.strftime('%Y-%m-%d %H:%M:%S')}")

# 溫濕度趨勢圖表
st.subheader("📈 溫濕度趨勢圖表")

# 獲取圖表數據
chart_data = st.session_state.data_handler.get_chart_data()

if not chart_data.empty:
    # 使用 Streamlit 內建圖表
    st.line_chart(
        chart_data,
        height=400,
        use_container_width=True
    )
    
    st.caption("X 軸：日期和時間 | Y 軸：溫度 (°C) 和濕度 (%)")
else:
    st.info("📊 等待數據以顯示圖表...")
    st.caption("當接收到 MQTT 數據後，圖表會自動更新")

st.markdown("---")

# 數據表格
st.subheader("📋 最近數據記錄")

recent_data = st.session_state.data_handler.get_recent_data(limit=50)

if not recent_data.empty:
    # 格式化顯示
    display_data = recent_data.copy()
    
    # 格式化時間戳記
    if 'timestamp' in display_data.columns:
        display_data['timestamp'] = pd.to_datetime(display_data['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 重新排列欄位順序
    column_order = ['timestamp', 'light', 'temperature', 'humidity']
    display_data = display_data[[col for col in column_order if col in display_data.columns]]
    
    # 重新命名欄位為中文
    display_data.columns = ['時間', '電燈狀態', '溫度 (°C)', '濕度 (%)']
    
    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )
    
    st.caption(f"顯示最近 {len(display_data)} 筆記錄")
else:
    st.info("📭 尚無數據記錄")
    st.caption("當接收到 MQTT 數據後，記錄會自動顯示在此")

# 手動刷新按鈕
col_refresh1, col_refresh2, col_refresh3 = st.columns([1, 1, 1])
with col_refresh2:
    if st.button("🔄 刷新數據", use_container_width=True):
        st.rerun()

# 如果數據已更新，顯示提示
if st.session_state.data_updated:
    st.session_state.data_updated = False
    st.success("✓ 數據已更新", icon="✅")

# 頁尾
st.markdown("---")
st.caption("MQTT 數據監控儀表板 | 所有數據自動儲存至 Excel 檔案")
