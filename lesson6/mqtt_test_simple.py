#!/usr/bin/env python3
"""
簡單的 MQTT PUBLISH 測試腳本
解決重複連線問題
"""

import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime
import random
import sys

# MQTT 配置
BROKER = "localhost"
PORT = 1883
TOPIC = "客廳/感測器"

# 使用唯一的 CLIENT_ID（加入進程 ID 和時間戳記）
import os
CLIENT_ID = f"test_pub_{os.getpid()}_{int(time.time())}"

print("=" * 70)
print("🚀 MQTT PUBLISH 測試程式")
print("=" * 70)
print(f"📡 Broker: {BROKER}:{PORT}")
print(f"📋 Topic: {TOPIC}")
print(f"🆔 Client ID: {CLIENT_ID}")
print("=" * 70)

# 連線狀態標記
connected = False

def on_connect(client, userdata, flags, reason_code, properties):
    """連線回調"""
    global connected
    if reason_code == 0:
        print("✅ 成功連接到 MQTT Broker")
        connected = True
    else:
        print(f"❌ 連線失敗，錯誤碼: {reason_code}")
        connected = False

def on_publish(client, userdata, mid, reason_code=None, properties=None):
    """發布回調"""
    print(f"  ✓ 訊息已發布 (ID: {mid})")

def on_disconnect(client, userdata, flags, reason_code, properties):
    """斷線回調"""
    global connected
    connected = False
    if reason_code == 0:
        print("👋 已正常斷開連線")
    else:
        print(f"⚠️  意外斷線，錯誤碼: {reason_code}")

def generate_sensor_data(msg_id):
    """生成測試數據"""
    return {
        "temperature": round(random.uniform(18, 30), 2),
        "humidity": round(random.uniform(40, 80), 2),
        "light_status": random.choice(["開", "關"]),
        "timestamp": datetime.now().isoformat(),
        "device": "測試裝置",
        "message_id": msg_id
    }

def main():
    """主程式"""
    global connected
    
    try:
        # 建立客戶端
        client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=CLIENT_ID,
            clean_session=True
        )
        
        # 設定回調
        client.on_connect = on_connect
        client.on_publish = on_publish
        client.on_disconnect = on_disconnect
        
        # 連線
        print("\n🔌 正在連接...")
        client.connect(BROKER, PORT, 60)
        
        # 啟動網路迴圈
        client.loop_start()
        
        # 等待連線建立
        timeout = 5
        start = time.time()
        while not connected and (time.time() - start) < timeout:
            time.sleep(0.1)
        
        if not connected:
            print("❌ 連線超時")
            return
        
        # 發布測試數據
        print("\n" + "=" * 70)
        print("📤 開始發布測試數據")
        print("=" * 70)
        
        for i in range(5):
            if not connected:
                print("⚠️  連線中斷，停止發布")
                break
            
            data = generate_sensor_data(i + 1)
            json_data = json.dumps(data, ensure_ascii=False)
            
            print(f"\n[{i+1}/5] 發布數據:")
            print(f"  溫度: {data['temperature']}°C")
            print(f"  濕度: {data['humidity']}%")
            print(f"  電燈: {data['light_status']}")
            
            result = client.publish(TOPIC, json_data, qos=1)
            
            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                print(f"  ❌ 發布失敗，錯誤碼: {result.rc}")
            
            # 等待訊息發送完成
            result.wait_for_publish(timeout=2)
            
            if i < 4:  # 最後一筆不用等
                time.sleep(1)
        
        print("\n" + "=" * 70)
        print("✅ 測試完成！")
        print("=" * 70)
        
        # 清理
        time.sleep(1)
        client.loop_stop()
        client.disconnect()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  使用者中斷")
        client.loop_stop()
        client.disconnect()
    except Exception as e:
        print(f"\n❌ 發生錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

