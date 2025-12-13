#!/bin/bash

# Streamlit 啟動腳本
# 在 uv 環境中啟動 Streamlit 應用

echo "🚀 啟動 Streamlit 測試應用..."
echo "================================================"
echo ""
echo "📡 應用將在以下地址啟動："
echo "   本機訪問: http://localhost:8501"
echo "   網路訪問: http://$(hostname -I | awk '{print $1}'):8501"
echo ""
echo "💡 提示："
echo "   - 按 Ctrl+C 停止應用"
echo "   - 修改代碼後會自動重新載入"
echo ""
echo "================================================"
echo ""

cd /home/pi/Documents/GiHub/20251026-raspberry_pi_pico

# 使用 uv run 在虛擬環境中啟動 streamlit
uv run streamlit run lesson6/streamlit_test.py \
    --server.address 0.0.0.0 \
    --server.port 8501 \
    --server.headless true


