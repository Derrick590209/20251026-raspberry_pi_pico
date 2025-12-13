# 🚀 Streamlit 快速啟動指南

## ⚠️ 重要提醒

**在 `uv` 環境中，必須使用 `uv run` 命令啟動 Streamlit！**

---

## ✅ 正確的啟動方式

### 方法 1：使用快速啟動腳本（推薦）⭐

```bash
cd /home/pi/Documents/GiHub/20251026-raspberry_pi_pico
./lesson6/啟動streamlit.sh
```

### 方法 2：直接使用 uv run

```bash
cd /home/pi/Documents/GiHub/20251026-raspberry_pi_pico
uv run streamlit run lesson6/streamlit_test.py
```

### 方法 3：允許外部訪問

```bash
cd /home/pi/Documents/GiHub/20251026-raspberry_pi_pico
uv run streamlit run lesson6/streamlit_test.py \
    --server.address 0.0.0.0 \
    --server.port 8501
```

---

## ❌ 錯誤的啟動方式

### ❌ 不要直接使用 streamlit

```bash
streamlit run app.py  # ❌ 錯誤！會找不到模組
```

**原因：** 系統 Python 中沒有安裝 streamlit，只在 `uv` 虛擬環境中有。

---

## 🌐 訪問應用

啟動成功後，你會看到：

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.16:8501
```

### 本機訪問
```
http://localhost:8501
```

### 從其他設備訪問
```
http://你的樹莓派IP:8501
```

**獲取樹莓派 IP：**
```bash
hostname -I | awk '{print $1}'
```

---

## 🛑 停止應用

在終端按：
```
Ctrl + C
```

---

## 🎯 快速測試步驟

### 步驟 1：啟動應用
```bash
./lesson6/啟動streamlit.sh
```

### 步驟 2：開啟瀏覽器
訪問 `http://localhost:8501`

### 步驟 3：測試功能
- 在側邊欄輸入名字
- 選擇不同功能（首頁、數據展示、圖表展示、互動測試）
- 點擊按鈕測試互動

### 步驟 4：停止應用
按 `Ctrl + C`

---

## 🔧 建立自己的應用

### 1. 創建新的 Python 檔案

```bash
cd /home/pi/Documents/GiHub/20251026-raspberry_pi_pico/lesson6
nano my_app.py
```

### 2. 編寫簡單的 Streamlit 應用

```python
import streamlit as st

st.title("我的第一個應用")
st.write("Hello, Streamlit!")

if st.button("點我"):
    st.balloons()
    st.success("按鈕被點擊了！")
```

### 3. 啟動應用

```bash
cd /home/pi/Documents/GiHub/20251026-raspberry_pi_pico
uv run streamlit run lesson6/my_app.py
```

---

## 🐛 疑難排解

### 問題 1：ModuleNotFoundError: No module named 'streamlit'

**原因：** 沒有使用 `uv run`

**解決：**
```bash
# ❌ 錯誤
streamlit run app.py

# ✅ 正確
uv run streamlit run app.py
```

---

### 問題 2：端口 8501 被佔用

**檢查：**
```bash
sudo lsof -i :8501
```

**解決：**
```bash
# 殺死佔用的進程
sudo kill -9 <PID>

# 或使用不同端口
uv run streamlit run app.py --server.port 8502
```

---

### 問題 3：無法從其他設備訪問

**原因：** 預設只監聽本地連線

**解決：**
```bash
uv run streamlit run app.py --server.address 0.0.0.0
```

或檢查防火牆：
```bash
sudo ufw status
sudo ufw allow 8501
```

---

### 問題 4：應用無法自動重載

**解決：** 完全停止（Ctrl+C）後重新啟動

---

## 📋 常用命令速查

### 啟動應用
```bash
uv run streamlit run app.py
```

### 指定端口
```bash
uv run streamlit run app.py --server.port 8502
```

### 允許外部訪問
```bash
uv run streamlit run app.py --server.address 0.0.0.0
```

### 關閉瀏覽器自動開啟
```bash
uv run streamlit run app.py --server.headless true
```

### 查看版本
```bash
uv run streamlit --version
```

### 組合使用
```bash
uv run streamlit run app.py \
    --server.address 0.0.0.0 \
    --server.port 8501 \
    --server.headless true
```

---

## 💡 開發技巧

### 1. 自動重載
Streamlit 會自動偵測檔案變更並重新載入，不需要手動重啟。

### 2. 除錯
在代碼中使用：
```python
st.write("除錯訊息", variable)
st.json(data)  # 檢查 JSON 資料
```

### 3. 快取資料
使用 `@st.cache_data` 避免重複計算：
```python
@st.cache_data
def load_data():
    return expensive_computation()
```

### 4. 狀態管理
使用 `st.session_state` 保存狀態：
```python
if 'count' not in st.session_state:
    st.session_state.count = 0
```

---

## 📊 範例應用

### 範例 1：即時感測器監控

```python
import streamlit as st
import random
import time

st.title("🌡️ 感測器即時監控")

# 佔位符
temp_placeholder = st.empty()
humidity_placeholder = st.empty()

# 即時更新
while True:
    temp = round(random.uniform(20, 30), 1)
    humidity = round(random.uniform(40, 80), 1)
    
    temp_placeholder.metric("溫度", f"{temp}°C")
    humidity_placeholder.metric("濕度", f"{humidity}%")
    
    time.sleep(1)
```

### 範例 2：MQTT 監控儀表板

```python
import streamlit as st
import paho.mqtt.client as mqtt
import json

st.title("📡 MQTT 監控")

if 'messages' not in st.session_state:
    st.session_state.messages = []

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    st.session_state.messages.append(data)

if st.button("連接 MQTT"):
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2
    )
    client.on_message = on_message
    client.connect("localhost", 1883)
    client.subscribe("客廳/感測器")
    client.loop_start()

# 顯示最新訊息
if st.session_state.messages:
    latest = st.session_state.messages[-1]
    col1, col2 = st.columns(2)
    with col1:
        st.metric("溫度", f"{latest['temperature']}°C")
    with col2:
        st.metric("濕度", f"{latest['humidity']}%")
```

---

## 🎉 開始使用

現在你可以啟動 Streamlit 了！

```bash
cd /home/pi/Documents/GiHub/20251026-raspberry_pi_pico
./lesson6/啟動streamlit.sh
```

然後在瀏覽器開啟：`http://localhost:8501`

---

## 📚 更多資源

- **完整指南**: `lesson6/Streamlit使用指南.md`
- **測試應用**: `lesson6/streamlit_test.py`
- **啟動腳本**: `lesson6/啟動streamlit.sh`

---

**記住：在 `uv` 環境中，一定要使用 `uv run` ！** ⭐


