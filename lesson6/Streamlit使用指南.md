# 🚀 Streamlit 使用指南

## ✅ 安裝狀態

**Streamlit 已安裝完成！**
- 版本：`streamlit 1.52.0`
- 環境：`uv` 虛擬環境
- 狀態：✅ 可以使用

---

## 🎯 啟動 Streamlit 應用

### 方法 1：使用測試範例（推薦）

```bash
cd /home/pi/Documents/GiHub/20251026-raspberry_pi_pico
streamlit run lesson6/streamlit_test.py
```

### 方法 2：創建新應用

```bash
# 創建新的 Python 文件
nano my_app.py

# 啟動應用
streamlit run my_app.py
```

---

## 📱 訪問應用

啟動後，Streamlit 會顯示：

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.16:8501
```

### 本機訪問
```
http://localhost:8501
```

### 其他設備訪問
```
http://你的樹莓派IP:8501
```

---

## 📝 基本 Streamlit 語法

### 1️⃣ **文字顯示**

```python
import streamlit as st

# 標題
st.title("這是標題")
st.header("這是標頭")
st.subheader("這是子標頭")

# 文字
st.write("這是普通文字")
st.text("這是純文字")
st.markdown("**這是粗體** *這是斜體*")

# 代碼
st.code("print('Hello World')", language="python")
```

### 2️⃣ **數據顯示**

```python
import pandas as pd

# 數據表格
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})
st.dataframe(df)
st.table(df)

# JSON
st.json({"name": "John", "age": 30})
```

### 3️⃣ **圖表**

```python
import pandas as pd
import numpy as np

# 線圖
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)
st.line_chart(chart_data)

# 柱狀圖
st.bar_chart(chart_data)

# 區域圖
st.area_chart(chart_data)
```

### 4️⃣ **互動元件**

```python
# 按鈕
if st.button("點擊我"):
    st.write("按鈕被點擊了！")

# 輸入框
name = st.text_input("請輸入名字", "預設值")
st.write(f"你好，{name}！")

# 滑動條
value = st.slider("選擇數值", 0, 100, 50)
st.write(f"當前值：{value}")

# 下拉選單
option = st.selectbox("選擇選項", ["選項1", "選項2", "選項3"])

# 複選框
checked = st.checkbox("同意條款")
if checked:
    st.write("已同意")

# 日期選擇
date = st.date_input("選擇日期")
```

### 5️⃣ **佈局**

```python
# 側邊欄
st.sidebar.title("側邊欄")
st.sidebar.write("這是側邊欄內容")

# 列佈局
col1, col2, col3 = st.columns(3)
with col1:
    st.write("第一列")
with col2:
    st.write("第二列")
with col3:
    st.write("第三列")

# 展開區域
with st.expander("點擊展開"):
    st.write("隱藏的內容")
```

### 6️⃣ **狀態訊息**

```python
# 成功訊息
st.success("操作成功！")

# 資訊訊息
st.info("這是一條資訊")

# 警告訊息
st.warning("這是警告")

# 錯誤訊息
st.error("發生錯誤")

# 異常
st.exception(Exception("這是異常"))
```

---

## 🎨 進階功能

### 1️⃣ **頁面配置**

```python
st.set_page_config(
    page_title="我的應用",
    page_icon="🚀",
    layout="wide",  # 寬版佈局
    initial_sidebar_state="expanded"  # 側邊欄預設展開
)
```

### 2️⃣ **Session State（狀態管理）**

```python
# 初始化狀態
if 'count' not in st.session_state:
    st.session_state.count = 0

# 按鈕計數器
if st.button("增加"):
    st.session_state.count += 1

st.write(f"計數：{st.session_state.count}")
```

### 3️⃣ **快取（提升性能）**

```python
@st.cache_data
def load_data():
    # 這個函數的結果會被快取
    return pd.read_csv("data.csv")

data = load_data()
```

### 4️⃣ **檔案上傳**

```python
uploaded_file = st.file_uploader("上傳檔案", type=['csv', 'txt'])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)
```

---

## 📊 實用範例

### 範例 1：溫濕度監控儀表板

```python
import streamlit as st
import random

st.title("🌡️ 溫濕度監控")

col1, col2 = st.columns(2)

with col1:
    temp = random.uniform(20, 30)
    st.metric("溫度", f"{temp:.1f}°C", delta="1.2°C")

with col2:
    humidity = random.uniform(40, 80)
    st.metric("濕度", f"{humidity:.1f}%", delta="-3%")

# 自動刷新
if st.button("🔄 刷新數據"):
    st.rerun()
```

### 範例 2：MQTT 訊息監控

```python
import streamlit as st
import paho.mqtt.client as mqtt
import json

st.title("📡 MQTT 訊息監控")

# 初始化訊息列表
if 'messages' not in st.session_state:
    st.session_state.messages = []

# MQTT 回調
def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    st.session_state.messages.append(data)

# 連線按鈕
if st.button("連接 MQTT"):
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2
    )
    client.on_message = on_message
    client.connect("localhost", 1883)
    client.subscribe("客廳/感測器")
    client.loop_start()
    st.success("已連接")

# 顯示訊息
for msg in st.session_state.messages[-10:]:
    st.write(msg)
```

---

## 🔧 常用指令

### 啟動應用
```bash
streamlit run app.py
```

### 指定端口
```bash
streamlit run app.py --server.port 8502
```

### 關閉瀏覽器自動開啟
```bash
streamlit run app.py --server.headless true
```

### 開發模式（自動重載）
```bash
streamlit run app.py --server.runOnSave true
```

### 查看版本
```bash
streamlit version
```

### 顯示配置
```bash
streamlit config show
```

---

## 🌐 遠端訪問設定

### 允許外部訪問

創建 `~/.streamlit/config.toml`：

```toml
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
serverAddress = "0.0.0.0"
serverPort = 8501
```

或使用命令：

```bash
streamlit run app.py \
  --server.address 0.0.0.0 \
  --server.port 8501 \
  --server.headless true
```

---

## 📦 整合其他套件

### 與 Pandas 整合

```python
import streamlit as st
import pandas as pd

df = pd.read_csv("data.csv")
st.dataframe(df)

# 篩選
filtered_df = df[df['temperature'] > 25]
st.line_chart(filtered_df['temperature'])
```

### 與 Matplotlib 整合

```python
import streamlit as st
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
st.pyplot(fig)
```

### 與 Plotly 整合

```python
import streamlit as st
import plotly.express as px

fig = px.line(df, x='date', y='temperature')
st.plotly_chart(fig)
```

---

## 🚨 疑難排解

### 問題 1：連線錯誤

```bash
# 檢查端口是否被佔用
sudo lsof -i :8501

# 殺死佔用進程
sudo kill -9 <PID>
```

### 問題 2：模組找不到

```bash
# 確認在正確的環境中
which streamlit

# 重新安裝
uv pip install streamlit
```

### 問題 3：應用無法刷新

按 `Ctrl + C` 停止應用，然後重新啟動。

---

## 💡 最佳實踐

1. **使用 `st.cache_data`** 快取數據讀取
2. **使用 `st.session_state`** 管理狀態
3. **合理使用佈局** (`columns`, `expander`, `sidebar`)
4. **提供清晰的使用說明**
5. **錯誤處理** 使用 `try-except`
6. **響應式設計** 考慮不同螢幕尺寸

---

## 📚 學習資源

- 官方文檔：https://docs.streamlit.io
- API 參考：https://docs.streamlit.io/library/api-reference
- 範例庫：https://streamlit.io/gallery
- 社群論壇：https://discuss.streamlit.io

---

## 🎉 開始使用

現在你已經準備好使用 Streamlit 了！

```bash
# 測試範例應用
cd /home/pi/Documents/GiHub/20251026-raspberry_pi_pico
streamlit run lesson6/streamlit_test.py
```

**在瀏覽器開啟：** `http://localhost:8501`

祝你使用愉快！🚀


