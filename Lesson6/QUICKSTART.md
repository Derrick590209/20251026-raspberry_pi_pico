# 快速開始指南

## 使用 uv 測試（最簡單）

### 一鍵測試

```bash
cd Lesson6
./test_setup.sh
```

### 手動步驟

1. **同步依賴**
   ```bash
   cd /home/pi/Documents/20251026-raspberry_pi_pico
   uv sync
   ```

2. **建立範例數據**
   ```bash
   cd Lesson6
   uv run python create_sample_data.py
   ```

3. **啟動應用程式**
   ```bash
   uv run streamlit run app.py
   ```

## 測試檢查清單

啟動應用程式後，檢查以下項目：

- [ ] 電燈狀態顯示正常
- [ ] 溫度數值顯示（約 25.5°C）
- [ ] 濕度數值顯示（約 62.6%）
- [ ] 溫濕度趨勢圖表顯示
- [ ] 數據表格顯示 48 筆記錄
- [ ] 側邊欄顯示數據統計

## 常用命令

```bash
# 啟動應用程式
uv run streamlit run app.py

# 重新生成範例數據
uv run python create_sample_data.py

# 檢查依賴
uv run python -c "import streamlit, pandas, openpyxl; print('OK')"

# 查看數據檔案
uv run python -c "import pandas as pd; df = pd.read_excel('data/mqtt_data.xlsx'); print(len(df))"
```

## 更多資訊

- 詳細測試說明：查看 [TEST.md](TEST.md)
- uv 使用指南：查看 [UV_TEST.md](UV_TEST.md)
- 完整說明文件：查看 [README.md](README.md)

