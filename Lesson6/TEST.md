# 測試說明

## 範例數據檔案

已建立範例 Excel 檔案 `data/mqtt_data.xlsx`，包含：
- **48 筆記錄**（過去 24 小時的數據，每 30 分鐘一筆）
- **時間範圍**：過去 24 小時
- **溫度範圍**：約 22.7°C 至 26.9°C
- **濕度範圍**：約 54.8% 至 64.6%
- **電燈狀態**：根據時間自動設定（晚上 6 點至早上 6 點為「開」）

## 使用 uv 測試（推薦）

### 1. 同步依賴套件

首先確保所有依賴套件已安裝：

```bash
cd /home/pi/Documents/20251026-raspberry_pi_pico
uv sync
```

### 2. 建立範例數據（如果還沒有）

```bash
cd Lesson6
uv run python create_sample_data.py
```

### 3. 啟動應用程式

使用 uv 運行 Streamlit 應用程式：

```bash
cd Lesson6
uv run streamlit run app.py
```

或者從專案根目錄運行：

```bash
cd /home/pi/Documents/20251026-raspberry_pi_pico
uv run --directory Lesson6 streamlit run Lesson6/app.py
```

## 傳統方法測試

### 1. 啟動應用程式

```bash
cd Lesson6
streamlit run app.py
```

### 2. 檢查界面顯示

應用程式啟動後，應該可以看到：

- ✅ **電燈狀態**：顯示最後一筆記錄的電燈狀態
- ✅ **溫度顯示**：顯示最後一筆記錄的溫度（約 25.5°C）
- ✅ **濕度顯示**：顯示最後一筆記錄的濕度（約 62.6%）
- ✅ **溫濕度趨勢圖表**：顯示過去 24 小時的溫濕度變化曲線
- ✅ **數據表格**：顯示最近的 50 筆記錄（如果有）

### 3. 側邊欄功能

- **連接狀態**：顯示 MQTT 連接狀態（預設為「未連接」）
- **數據統計**：顯示 Excel 檔案中的記錄數和時間範圍

### 4. 重新生成範例數據

#### 使用 uv（推薦）

```bash
cd Lesson6
uv run python create_sample_data.py
```

#### 使用傳統虛擬環境

```bash
cd Lesson6
source ../.venv/bin/activate  # 如果使用虛擬環境
python create_sample_data.py
```

## 預期結果

1. **界面正常顯示**：所有 UI 組件都能正常顯示
2. **圖表正常顯示**：溫濕度趨勢圖表能顯示 48 筆數據的變化
3. **數據表格正常顯示**：表格能顯示最近的記錄
4. **最後更新時間**：顯示最後一筆記錄的時間

## 注意事項

- 範例數據是模擬數據，用於測試界面顯示
- 實際使用時，數據會透過 MQTT 即時接收
- Excel 檔案會持續累積數據，不會覆蓋舊數據

