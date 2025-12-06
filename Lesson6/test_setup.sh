#!/bin/bash
# 快速測試腳本 - 使用 uv 環境

set -e

echo "=========================================="
echo "MQTT 數據監控儀表板 - 快速測試"
echo "=========================================="
echo ""

# 檢查 uv 是否安裝
if ! command -v uv &> /dev/null; then
    echo "❌ 錯誤：未找到 uv 命令"
    echo "請先安裝 uv：curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "✓ uv 已安裝"
echo ""

# 切換到專案根目錄
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "📦 步驟 1: 同步依賴套件..."
uv sync
echo "✓ 依賴套件已同步"
echo ""

# 切換到 Lesson6 目錄
cd Lesson6

echo "📊 步驟 2: 建立/更新範例數據..."
uv run python create_sample_data.py
echo ""

echo "🔍 步驟 3: 驗證依賴套件..."
uv run python -c "
import streamlit
import pandas
import openpyxl
import paho.mqtt.client

print('✓ 所有依賴套件已正確安裝')
print(f'  - Streamlit: {streamlit.__version__}')
print(f'  - Pandas: {pandas.__version__}')
print(f'  - OpenPyXL: {openpyxl.__version__}')
print(f'  - Paho MQTT: 已安裝')
"
echo ""

echo "📁 步驟 4: 驗證範例數據檔案..."
uv run python -c "
import pandas as pd
from pathlib import Path

excel_file = Path('data/mqtt_data.xlsx')
if excel_file.exists():
    df = pd.read_excel(excel_file)
    print(f'✓ Excel 檔案載入成功')
    print(f'  - 檔案路徑: {excel_file.absolute()}')
    print(f'  - 記錄數: {len(df)} 筆')
    print(f'  - 欄位: {list(df.columns)}')
    if len(df) > 0:
        print(f'  - 最後一筆:')
        last = df.iloc[-1]
        print(f'    * 時間: {last[\"timestamp\"]}')
        print(f'    * 電燈: {last[\"light\"]}')
        print(f'    * 溫度: {last[\"temperature\"]}°C')
        print(f'    * 濕度: {last[\"humidity\"]}%')
else:
    print('❌ Excel 檔案不存在')
    exit(1)
"
echo ""

echo "🔧 步驟 5: 測試數據處理模組..."
uv run python -c "
from data_handler import DataHandler

dh = DataHandler(data_dir='data')
all_data = dh.get_all_data()
chart_data = dh.get_chart_data()

print('✓ 數據處理模組測試成功')
print(f'  - 總記錄數: {len(all_data)}')
print(f'  - 圖表數據點: {len(chart_data)}')
if len(all_data) > 0:
    print(f'  - 時間範圍: {all_data[\"timestamp\"].min()} 至 {all_data[\"timestamp\"].max()}')
"
echo ""

echo "=========================================="
echo "✅ 所有測試通過！"
echo "=========================================="
echo ""
echo "🚀 現在可以啟動應用程式："
echo "   cd Lesson6"
echo "   uv run streamlit run app.py"
echo ""
echo "或者直接執行："
echo "   uv run --directory Lesson6 streamlit run Lesson6/app.py"
echo ""

