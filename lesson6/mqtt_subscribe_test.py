#!/usr/bin/env python3
"""
簡單的 MQTT SUBSCRIBE 測試腳本
用於訂閱並顯示接收到的訊息
"""

import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime
import os
import signal
import sys

# MQTT 配置
BROKER = "localhost"
PORT = 1883
TOPIC = "客廳/感測器"

# 使用唯一的 CLIENT_ID
CLIENT_ID = f"test_sub_{os.getpid()}_{int(time.time())}"

# 統計
message_count = 0
start_time = None

def signal_handler(sig, frame):
    """處理 Ctrl+C"""
    print("\n\n" + "=" * 70)
    print("👋 收到中斷信號，正在關閉...")
    print("=" * 70)
    if start_time:
        duration = time.time() - start_time
        print(f"📊 運行時間: {duration:.1f} 秒")
    print(f"📬 總接收訊息數: {message_count}")
    print("=" * 70)
    client.loop_stop()
    client.disconnect()
    sys.exit(0)

def on_connect(client, userdata, flags, reason_code, properties):
    """連線回調"""
    if reason_code == 0:
        print("✅ 成功連接到 MQTT Broker")
        client.subscribe(TOPIC, qos=1)
        print(f"📬 已訂閱主題: {TOPIC}")
        print("\n" + "=" * 70)
        print("⏳ 等待訊息中... (按 Ctrl+C 結束)")
        print("=" * 70)
    else:
        print(f"❌ 連線失敗，錯誤碼: {reason_code}")

def on_message(client, userdata, msg):
    """訊息接收回調"""
    global message_count
    message_count += 1
    
    try:
        payload = msg.payload.decode('utf-8')
        data = json.loads(payload)
        
        print(f"\n{'='*70}")
        print(f"📩 訊息 #{message_count} - {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*70}")
        
        if isinstance(data, dict):
            if 'temperature' in data:
                print(f"🌡️  溫度: {data['temperature']}°C")
            if 'humidity' in data:
                print(f"💧 濕度: {data['humidity']}%")
            if 'light_status' in data:
                print(f"💡 電燈: {data['light_status']}")
            if 'device' in data:
                print(f"📱 裝置: {data['device']}")
        else:
            print(f"📄 數據: {data}")
            
    except json.JSONDecodeError:
        print(f"\n{'='*70}")
        print(f"📩 訊息 #{message_count} (非 JSON)")
        print(f"{'='*70}")
        print(f"內容: {msg.payload.decode('utf-8')}")
    except Exception as e:
        print(f"❌ 處理訊息時發生錯誤: {e}")

def on_disconnect(client, userdata, flags, reason_code, properties):
    """斷線回調"""
    if reason_code == 0:
        print("\n✅ 已正常斷開連線")
    else:
        print(f"\n⚠️ 意外斷線，錯誤碼: {reason_code}")

def main():
    """主程式"""
    global client, start_time
    
    # 設定 Ctrl+C 處理
    signal.signal(signal.SIGINT, signal_handler)
    
    print("=" * 70)
    print("🚀 MQTT SUBSCRIBE 測試程式")
    print("=" * 70)
    print(f"📡 Broker: {BROKER}:{PORT}")
    print(f"📋 Topic: {TOPIC}")
    print(f"🆔 Client ID: {CLIENT_ID}")
    print("=" * 70)
    
    try:
        # 建立客戶端
        client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=CLIENT_ID,
            clean_session=True
        )
        
        # 設定回調
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect
        
        # 連線
        print("\n🔌 正在連接...")
        client.connect(BROKER, PORT, 60)
        
        # 啟動網路迴圈
        start_time = time.time()
        client.loop_forever()
        
    except KeyboardInterrupt:
        print("\n⚠️ 使用者中斷")
    except Exception as e:
        print(f"\n❌ 發生錯誤: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            client.loop_stop()
            client.disconnect()
        except:
            pass

if __name__ == "__main__":
    main()





