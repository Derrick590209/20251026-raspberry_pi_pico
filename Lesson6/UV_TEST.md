# 使用 uv 測試指南

本專案使用 [uv](https://github.com/astral-sh/uv) 作為 Python 套件管理器和專案管理工具。

## 前置準備

### 1. 確認 uv 已安裝

```bash
uv --version
```

如果未安裝，可以從 [uv 官方網站](https://github.com/astral-sh/uv) 安裝。

### 2. 同步依賴套件

在專案根目錄執行：

```bash
cd /home/pi/Documents/20251026-raspberry_pi_pico
uv sync
```

這會根據 `pyproject.toml` 和 `uv.lock` 安裝所有必要的依賴套件。

## 測試步驟

### 步驟 1：建立範例數據

在 Lesson6 目錄下執行：

```bash
cd Lesson6
uv run python create_sample_data.py
```

這會建立包含 48 筆記錄的範例 Excel 檔案 `data/mqtt_data.xlsx`。

**預期輸出：**
```
✓ 範例 Excel 檔案已建立：data/mqtt_data.xlsx
  - 共 48 筆記錄
  - 時間範圍：... 至 ...
  - 溫度範圍：...°C 至 ...°C
  - 濕度範圍：...% 至 ...%
```

### 步驟 2：啟動 Streamlit 應用程式

```bash
cd Lesson6
uv run streamlit run app.py
```

或者從專案根目錄：

```bash
uv run --directory Lesson6 streamlit run Lesson6/app.py
```

**預期結果：**
- 瀏覽器會自動打開應用程式（通常是 `http://localhost:8501`）
- 終端會顯示 Streamlit 伺服器資訊

### 步驟 3：檢查應用程式界面

應用程式啟動後，應該可以看到：

#### 主要顯示區域
- ✅ **電燈狀態**：顯示最後一筆記錄的電燈狀態（開/關）
- ✅ **溫度顯示**：顯示最後一筆記錄的溫度（約 25.5°C）
- ✅ **濕度顯示**：顯示最後一筆記錄的濕度（約 62.6%）
- ✅ **溫濕度趨勢圖表**：顯示過去 24 小時的溫濕度變化曲線
- ✅ **數據表格**：顯示最近的數據記錄

#### 側邊欄
- **連接狀態**：顯示 MQTT 連接狀態（預設為「未連接」）
- **數據統計**：顯示 Excel 檔案中的記錄數（48 筆）和時間範圍
- **說明**：應用程式使用說明

## 常用 uv 命令

### 安裝/更新依賴

```bash
# 同步所有依賴（根據 pyproject.toml）
uv sync

# 添加新套件
uv add <package-name>

# 移除套件
uv remove <package-name>
```

### 運行 Python 腳本

```bash
# 運行單個 Python 檔案
uv run python script.py

# 運行 Streamlit 應用程式
uv run streamlit run app.py
```

### 進入虛擬環境

```bash
# uv 會自動管理虛擬環境，通常不需要手動進入
# 但如果需要，可以：
uv venv
source .venv/bin/activate  # Linux/Mac
```

### 檢查依賴

```bash
# 查看已安裝的套件
uv pip list

# 查看專案依賴樹
uv tree
```

## 故障排除

### 問題 1：找不到 uv 命令

**解決方法：**
```bash
# 檢查 uv 是否在 PATH 中
which uv

# 如果未安裝，使用以下命令安裝：
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 問題 2：依賴套件安裝失敗

**解決方法：**
```bash
# 清除快取並重新同步
uv sync --refresh
```

### 問題 3：Streamlit 無法啟動

**解決方法：**
1. 確認所有依賴已安裝：`uv sync`
2. 檢查 Python 版本：`uv run python --version`（需要 >= 3.10）
3. 確認端口 8501 未被佔用

### 問題 4：找不到範例數據檔案

**解決方法：**
```bash
# 重新生成範例數據
cd Lesson6
uv run python create_sample_data.py

# 檢查檔案是否存在
ls -lh data/mqtt_data.xlsx
```

## 驗證測試

執行以下命令驗證所有功能正常：

```bash
# 1. 驗證依賴已安裝
uv run python -c "import streamlit, pandas, openpyxl, paho.mqtt.client; print('✓ 所有依賴已安裝')"

# 2. 驗證範例數據檔案
uv run python -c "import pandas as pd; df = pd.read_excel('Lesson6/data/mqtt_data.xlsx'); print(f'✓ Excel 檔案載入成功：{len(df)} 筆記錄')"

# 3. 測試數據處理模組
uv run python -c "from Lesson6.data_handler import DataHandler; dh = DataHandler('Lesson6/data'); print(f'✓ 數據處理器初始化成功，載入 {len(dh.get_all_data())} 筆記錄')"
```

## 開發建議

1. **使用 uv run**：所有 Python 命令都應使用 `uv run` 前綴，確保在正確的環境中執行
2. **保持同步**：當修改 `pyproject.toml` 後，記得執行 `uv sync`
3. **鎖定版本**：`uv.lock` 檔案會鎖定依賴版本，確保環境一致性
4. **清理快取**：如有問題，可以使用 `uv sync --refresh` 清除快取

## 相關檔案

- `pyproject.toml`：專案配置和依賴定義
- `uv.lock`：鎖定的依賴版本
- `Lesson6/data/mqtt_data.xlsx`：範例數據檔案
- `Lesson6/create_sample_data.py`：數據生成腳本

