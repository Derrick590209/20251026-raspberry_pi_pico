#!/bin/bash

echo "======================================================================"
echo "🔍 Jupyter Notebook 問題診斷"
echo "======================================================================"

cd /home/pi/Documents/GiHub/20251026-raspberry_pi_pico

# 1. 檢查 Jupyter 狀態
echo ""
echo "📊 1. Jupyter 進程狀態"
echo "----------------------------------------------------------------------"
if ps aux | grep -v grep | grep jupyter > /dev/null; then
    echo "✅ Jupyter 正在運行"
    JUPYTER_COUNT=$(ps aux | grep -v grep | grep jupyter | wc -l)
    echo "   進程數量: $JUPYTER_COUNT"
else
    echo "❌ Jupyter 沒有運行"
    echo "   請先啟動 Jupyter: uv run jupyter notebook"
    exit 1
fi

# 2. 檢查 Kernel 狀態
echo ""
echo "📊 2. Kernel 進程狀態"
echo "----------------------------------------------------------------------"
if ps aux | grep -v grep | grep ipykernel > /dev/null; then
    KERNEL_COUNT=$(ps aux | grep -v grep | grep ipykernel | wc -l)
    echo "✅ 找到 $KERNEL_COUNT 個 Kernel 進程"
else
    echo "⚠️  沒有找到運行中的 Kernel"
    echo "   可能需要在 Jupyter 中開啟 Notebook"
fi

# 3. 檢查 Mosquitto Broker
echo ""
echo "📊 3. MQTT Broker 狀態"
echo "----------------------------------------------------------------------"
if systemctl is-active --quiet mosquitto; then
    echo "✅ Mosquitto Broker 正在運行"
else
    echo "❌ Mosquitto Broker 沒有運行"
    echo "   啟動 Broker: sudo systemctl start mosquitto"
fi

# 4. 測試 MQTT 連線
echo ""
echo "📊 4. MQTT 連線測試"
echo "----------------------------------------------------------------------"
if timeout 2 mosquitto_pub -h localhost -t "test/診斷" -m "hello" 2>/dev/null; then
    echo "✅ MQTT 發布測試成功"
else
    echo "❌ MQTT 發布測試失敗"
fi

# 5. 檢查 Notebook 檔案
echo ""
echo "📊 5. Notebook 檔案狀態"
echo "----------------------------------------------------------------------"
if [ -f "lesson6/lesson6_1.ipynb" ]; then
    echo "✅ lesson6_1.ipynb 存在"
    
    # 檢查檔案大小
    SIZE=$(stat -f%z "lesson6/lesson6_1.ipynb" 2>/dev/null || stat -c%s "lesson6/lesson6_1.ipynb" 2>/dev/null)
    echo "   檔案大小: $SIZE bytes"
    
    # 檢查是否為有效 JSON
    if python3 -c "import json; json.load(open('lesson6/lesson6_1.ipynb'))" 2>/dev/null; then
        echo "   ✅ JSON 格式正確"
    else
        echo "   ❌ JSON 格式錯誤"
    fi
else
    echo "❌ lesson6_1.ipynb 不存在"
fi

# 6. 測試代碼執行
echo ""
echo "📊 6. 代碼執行測試"
echo "----------------------------------------------------------------------"
echo "正在執行 test_notebook_cells.py（這會測試所有 cells）..."
echo ""

if uv run python lesson6/test_notebook_cells.py 2>&1 | head -50; then
    echo ""
    echo "✅ 代碼可以正常執行"
else
    echo ""
    echo "❌ 代碼執行失敗"
fi

# 總結
echo ""
echo "======================================================================"
echo "📋 診斷總結"
echo "======================================================================"
echo ""
echo "如果以上測試都通過，但 Jupyter Notebook 還是沒有輸出，"
echo "問題可能是："
echo ""
echo "1. ❓ Cell 沒有被執行"
echo "   解決：點擊 Cell，按 Shift + Enter"
echo ""
echo "2. ❓ Kernel 沒有連接到 Notebook"
echo "   解決：Kernel → Restart Kernel → Restart"
echo ""
echo "3. ❓ 輸出區域被隱藏"
echo "   解決：Cell → Current Outputs → Show"
echo ""
echo "4. ❓ 瀏覽器快取問題"
echo "   解決：按 F5 刷新頁面，或清除瀏覽器快取"
echo ""
echo "======================================================================"
echo "💡 建議的下一步"
echo "======================================================================"
echo ""
echo "在 Jupyter Notebook 中："
echo "1. 按 F5 刷新頁面"
echo "2. 點擊 Kernel → Restart Kernel → Restart"
echo "3. 依序執行 Cell 1 → 2 → 3 → 4"
echo "4. 每執行一個 Cell 後檢查是否有輸出"
echo ""
echo "或使用更可靠的命令列測試："
echo "  uv run python lesson6/mqtt_subscribe_test.py  # 終端機 1"
echo "  uv run python lesson6/mqtt_test_simple.py      # 終端機 2"
echo ""
echo "======================================================================"





