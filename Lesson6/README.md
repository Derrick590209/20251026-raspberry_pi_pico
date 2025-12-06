# MQTT 數據監控儀表板

根據 [PRD.md](PRD.md) 規格實作的 Streamlit Web 應用程式，用於即時監控客廳環境數據。

> **快速開始**：查看 [QUICKSTART.md](QUICKSTART.md) 了解最快上手方式

## 功能特性

- 📡 MQTT 訂閱者：訂閱「客廳」主題，接收即時環境數據
- 💡 電燈狀態顯示：顯示電燈開關狀態
- 🌡️ 溫度顯示：即時顯示客廳溫度
- 💧 濕度顯示：即時顯示客廳濕度
- 📈 趨勢圖表：顯示溫濕度歷史變化趨勢
- 💾 自動儲存：所有數據自動儲存到 Excel 檔案

## 專案結構

```
Lesson6/
├── app.py                  # Streamlit 主應用程式
├── mqtt_client.py          # MQTT 訂閱者模組
├── data_handler.py         # 數據處理與 Excel 儲存模組
├── create_sample_data.py   # 範例數據生成腳本
├── test_setup.sh          # 自動化測試腳本
├── data/                  # Excel 檔案儲存目錄
│   └── mqtt_data.xlsx    # 數據檔案（自動生成）
├── PRD.md                 # 產品需求文件
├── README.md              # 本說明文件（主要說明）
├── QUICKSTART.md          # 快速開始指南
├── TEST.md                # 測試說明文件
└── UV_TEST.md            # uv 環境測試詳細指南
```

## 快速開始

### 🚀 最簡單的方式

```bash
cd Lesson6
./test_setup.sh          # 一鍵測試和驗證
uv run streamlit run app.py  # 啟動應用程式
```

詳細步驟請查看 [QUICKSTART.md](QUICKSTART.md)

## 安裝與執行

### 方法一：使用 uv（推薦）

本專案使用 [uv](https://github.com/astral-sh/uv) 作為套件管理器，提供更快的依賴安裝和更可靠的環境管理。

#### 1. 同步依賴套件

```bash
# 在專案根目錄執行
cd /home/pi/Documents/20251026-raspberry_pi_pico
uv sync
```

#### 2. 建立範例數據（建議，用於測試界面）

```bash
cd Lesson6
uv run python create_sample_data.py
```

這會建立包含 48 筆記錄的範例 Excel 檔案，讓您可以在沒有 MQTT 數據的情況下測試應用程式界面。

#### 3. 啟動 Streamlit 應用程式

```bash
cd Lesson6
uv run streamlit run app.py
```

或從專案根目錄：

```bash
uv run --directory Lesson6 streamlit run Lesson6/app.py
```

#### 4. 自動化測試

使用測試腳本驗證所有功能：

```bash
cd Lesson6
./test_setup.sh
```

這會自動：
- 同步依賴套件
- 建立/更新範例數據
- 驗證所有模組功能
- 顯示測試結果

詳細的 uv 使用說明和故障排除請參考 [UV_TEST.md](UV_TEST.md)

### 方法二：使用傳統 pip

#### 1. 確保已安裝依賴套件

```bash
# 安裝專案依賴
pip install -e ..
```

或手動安裝：

```bash
pip install streamlit paho-mqtt pandas openpyxl
```

#### 2. 啟動 Streamlit 應用程式

```bash
cd Lesson6
streamlit run app.py
```

### MQTT Broker 設定

應用程式預設連接到 `localhost:1883`，請確保：
- Mosquitto MQTT Broker 已安裝並運行
- 可以接收來自主題「客廳」的訊息

應用程式會在瀏覽器中自動打開（通常是 `http://localhost:8501`）

## 使用方式

### 基本操作

1. **連接 MQTT**：在側邊欄點擊「連接 MQTT」按鈕（需要 MQTT Broker 運行中）
2. **查看數據**：連接成功後，應用程式會自動接收並顯示 MQTT 訊息
3. **查看圖表**：溫濕度趨勢圖表會自動顯示歷史數據變化
4. **查看記錄**：滾動到頁面下方查看最近的數據記錄表格
5. **刷新數據**：點擊「刷新數據」按鈕以手動更新顯示

### 使用範例數據測試

即使沒有 MQTT 連接，您也可以：
- 查看範例數據的顯示效果
- 測試圖表和表格功能
- 驗證界面顯示是否正常

只需執行 `uv run python create_sample_data.py` 建立範例數據即可。

## MQTT 數據格式

應用程式期望接收以下 JSON 格式的數據：

```json
{
  "light": "on",        // 或 "off"、"開"、"關"
  "temperature": 25.5,  // 溫度數值（浮點數）
  "humidity": 60.2      // 濕度數值（浮點數）
}
```

或者可以包含時間戳記：

```json
{
  "light": "on",
  "temperature": 25.5,
  "humidity": 60.2,
  "timestamp": "2025-12-04 23:00:00"
}
```

## 數據儲存

所有接收到的數據會自動儲存到 `data/mqtt_data.xlsx` 檔案中，包含以下欄位：

- `timestamp`: 數據接收時間
- `light`: 電燈狀態
- `temperature`: 溫度數值
- `humidity`: 濕度數值

## 技術架構

- **前端框架**: Streamlit 1.52.0+
- **MQTT 客戶端**: paho-mqtt 2.1.0+
- **數據處理**: pandas 2.0.0+
- **Excel 儲存**: openpyxl 3.0.0+ (透過 pandas)
- **套件管理**: uv (專案使用 uv 進行依賴管理)
- **Python 版本**: 3.10+

## 測試說明

專案包含完整的測試文件和腳本：

- **[QUICKSTART.md](QUICKSTART.md)**：快速開始指南，適合第一次使用的用戶
- **[TEST.md](TEST.md)**：詳細的測試說明和檢查清單
- **[UV_TEST.md](UV_TEST.md)**：uv 環境的完整使用指南和故障排除
- **test_setup.sh**：自動化測試腳本，驗證所有功能

### 運行測試

```bash
# 自動化測試（推薦）
cd Lesson6
./test_setup.sh

# 或查看詳細測試說明
cat TEST.md
```

## 注意事項

1. **首次執行**：`data/` 資料夾會自動建立
2. **MQTT 連接**：如果 MQTT Broker 未運行，連接會失敗（但可正常查看範例數據）
3. **數據儲存**：數據會持續追加到 Excel 檔案，不會覆蓋舊數據
4. **備份建議**：建議定期備份 `data/mqtt_data.xlsx` 檔案
5. **範例數據**：可以使用 `create_sample_data.py` 建立測試用的範例數據
6. **環境管理**：建議使用 uv 進行依賴管理，確保環境一致性

## 故障排除

### 連接失敗
- 檢查 MQTT Broker 是否運行：`sudo systemctl status mosquitto`
- 檢查埠號是否正確（預設為 1883）
- 檢查防火牆設定

### 沒有接收到數據
- 確認 MQTT 主題名稱正確（預設為「客廳」）
- 檢查發布者是否正常運行
- 查看終端機是否有錯誤訊息

### Excel 檔案錯誤
- 確認有寫入權限
- 檢查磁碟空間是否充足
- 確認 openpyxl 套件已正確安裝
- 使用 `uv sync` 確保所有依賴正確安裝

### 測試相關問題
- 查看 [TEST.md](TEST.md) 了解測試步驟
- 查看 [UV_TEST.md](UV_TEST.md) 了解 uv 環境設定
- 執行 `./test_setup.sh` 進行自動化測試和診斷

## 相關文件

- **[PRD.md](PRD.md)** - 產品需求文件，了解專案規格
- **[QUICKSTART.md](QUICKSTART.md)** - 快速開始指南
- **[TEST.md](TEST.md)** - 測試說明和檢查清單
- **[UV_TEST.md](UV_TEST.md)** - uv 環境詳細使用指南

## 開發資訊

### 模組說明

- **app.py**: Streamlit 主應用程式，包含所有 UI 組件和邏輯整合
- **mqtt_client.py**: MQTT 訂閱者客戶端，處理連接、訂閱和訊息接收
- **data_handler.py**: 數據處理模組，負責解析、儲存和查詢數據
- **create_sample_data.py**: 範例數據生成工具，用於測試和演示

### 貢獻指南

1. 修改代碼前請先閱讀 PRD.md 了解需求
2. 使用 `./test_setup.sh` 確保所有測試通過
3. 遵循現有的代碼風格和結構
4. 更新相關文件（README、TEST 等）

