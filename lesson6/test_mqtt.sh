#!/bin/bash
# MQTT 完整測試腳本

echo "======================================================================"
echo "🧪 MQTT Publish/Subscribe 測試"
echo "======================================================================"
echo ""

# 切換到專案目錄
cd /home/pi/Documents/GiHub/20251026-raspberry_pi_pico

# 檢查 Mosquitto 狀態
echo "📡 檢查 Mosquitto Broker 狀態..."
if systemctl is-active --quiet mosquitto; then
    echo "✅ Mosquitto Broker 正在運行"
else
    echo "❌ Mosquitto Broker 未運行"
    echo "正在啟動..."
    sudo systemctl start mosquitto
    sleep 1
fi
echo ""

# 選擇測試模式
echo "請選擇測試模式："
echo "1) 命令列測試（推薦，快速）"
echo "2) Python 腳本測試（完整功能）"
echo "3) 同時運行發布者和訂閱者"
echo ""
read -p "請輸入選項 (1-3): " choice

case $choice in
    1)
        echo ""
        echo "======================================================================"
        echo "📋 模式 1: 命令列測試"
        echo "======================================================================"
        echo ""
        echo "正在啟動訂閱者..."
        echo "💡 提示：開啟另一個終端機執行以下命令來發布訊息："
        echo ""
        echo "   mosquitto_pub -h localhost -t \"客廳/感測器\" -m '{\"temperature\": 25, \"humidity\": 60}'"
        echo ""
        echo "按 Ctrl+C 結束訂閱"
        echo ""
        mosquitto_sub -h localhost -t "客廳/感測器" -v
        ;;
    
    2)
        echo ""
        echo "======================================================================"
        echo "📋 模式 2: Python 腳本測試"
        echo "======================================================================"
        echo ""
        echo "請選擇："
        echo "1) 啟動訂閱者（Subscriber）"
        echo "2) 啟動發布者（Publisher）"
        echo ""
        read -p "請輸入選項 (1-2): " sub_choice
        
        if [ "$sub_choice" = "1" ]; then
            echo ""
            echo "🔔 啟動訂閱者..."
            echo "按 Ctrl+C 結束"
            echo ""
            uv run python lesson6/mqtt_subscribe_test.py
        elif [ "$sub_choice" = "2" ]; then
            echo ""
            echo "📤 啟動發布者..."
            echo ""
            uv run python lesson6/mqtt_test_simple.py
        else
            echo "❌ 無效的選項"
        fi
        ;;
    
    3)
        echo ""
        echo "======================================================================"
        echo "📋 模式 3: 同時運行測試"
        echo "======================================================================"
        echo ""
        echo "正在啟動訂閱者（背景運行）..."
        
        # 啟動訂閱者（背景，15秒後自動結束）
        timeout 15 uv run python lesson6/mqtt_subscribe_test.py > /tmp/mqtt_sub_output.txt 2>&1 &
        SUB_PID=$!
        
        sleep 2
        
        echo "✅ 訂閱者已啟動 (PID: $SUB_PID)"
        echo ""
        echo "正在發布 5 筆測試數據..."
        echo ""
        
        # 執行發布者
        uv run python lesson6/mqtt_test_simple.py
        
        echo ""
        echo "等待訂閱者接收訊息..."
        sleep 2
        
        echo ""
        echo "======================================================================"
        echo "📊 訂閱者接收到的訊息："
        echo "======================================================================"
        cat /tmp/mqtt_sub_output.txt
        
        # 清理
        kill $SUB_PID 2>/dev/null
        rm -f /tmp/mqtt_sub_output.txt
        ;;
    
    *)
        echo "❌ 無效的選項"
        exit 1
        ;;
esac

echo ""
echo "======================================================================"
echo "✅ 測試完成"
echo "======================================================================"





