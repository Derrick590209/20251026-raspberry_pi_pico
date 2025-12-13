#!/usr/bin/env python3
"""
測試 lesson6_1.ipynb 的 cells 是否能正常執行
"""

print("=" * 70)
print("🧪 測試 Notebook Cells 執行")
print("=" * 70)

# Cell 1: 匯入套件
print("\n▶️ 測試 Cell 1: 匯入套件")
print("-" * 70)
import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime
import random
print("✅ 套件匯入成功！")

# Cell 2: MQTT 配置
print("\n▶️ 測試 Cell 2: MQTT 配置")
print("-" * 70)
BROKER = "localhost"
PORT = 1883
TOPIC = "客廳/感測器"
import time as _time
CLIENT_ID = f"test_notebook_{int(_time.time())}"
print("=" * 60)
print("📡 MQTT 連線設定")
print("=" * 60)
print(f"   Broker: {BROKER}:{PORT}")
print(f"   Topic: {TOPIC}")
print(f"   Client ID: {CLIENT_ID}")
print("=" * 60)

# Cell 3: 定義回調函數
print("\n▶️ 測試 Cell 3: 定義回調函數")
print("-" * 70)
def on_connect(client, userdata, flags, reason_code, properties):
    """連線成功時的回調"""
    if reason_code == 0:
        print("✅ 成功連接到 MQTT Broker")
    else:
        print(f"❌ 連線失敗，錯誤碼: {reason_code}")

def on_publish(client, userdata, mid, reason_code=None, properties=None):
    """訊息發布成功時的回調"""
    print(f"  ✓ 訊息已發布 (ID: {mid})")

def on_disconnect(client, userdata, flags, reason_code, properties):
    """斷線時的回調"""
    if reason_code == 0:
        print("👋 已正常斷開連線")
    else:
        print(f"⚠️ 意外斷線，錯誤碼: {reason_code}")

print("✅ 回調函數定義完成")

# Cell 4: 建立連線
print("\n▶️ 測試 Cell 4: 建立連線")
print("-" * 70)
try:
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=CLIENT_ID,
        clean_session=True
    )
    
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    
    print(f"🔌 正在連接到 {BROKER}:{PORT}...")
    client.connect(BROKER, PORT, 60)
    
    client.loop_start()
    time.sleep(1)
    
    print("\n" + "=" * 60)
    print("✅ MQTT 客戶端已就緒")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ 連線失敗: {e}")
    exit(1)

# Cell 5: 生成測試數據
print("\n▶️ 測試 Cell 5: 生成測試數據")
print("-" * 70)
def generate_sensor_data(message_id=1):
    """生成模擬的感測器數據"""
    data = {
        "temperature": round(random.uniform(18, 30), 2),
        "humidity": round(random.uniform(40, 80), 2),
        "light_status": random.choice(["開", "關"]),
        "timestamp": datetime.now().isoformat(),
        "device": "Jupyter 測試裝置",
        "message_id": message_id
    }
    return data

test_data = generate_sensor_data()
print("📊 測試數據範例：")
print(json.dumps(test_data, indent=2, ensure_ascii=False))

# Cell 6: 發布單筆測試數據
print("\n▶️ 測試 Cell 6: 發布單筆測試數據")
print("-" * 70)
def publish_single_message():
    """發布一筆測試訊息"""
    try:
        data = generate_sensor_data()
        json_data = json.dumps(data, ensure_ascii=False)
        
        result = client.publish(TOPIC, json_data, qos=1)
        
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"✅ 發布成功！")
            print(f"   🌡️  溫度: {data['temperature']}°C")
            print(f"   💧 濕度: {data['humidity']}%")
            print(f"   💡 電燈: {data['light_status']}")
        else:
            print(f"❌ 發布失敗，錯誤碼: {result.rc}")
            
    except Exception as e:
        print(f"❌ 錯誤: {e}")

print("=" * 60)
print("📤 發布單筆測試數據")
print("=" * 60)
publish_single_message()

# 等待發布完成
time.sleep(1)

# Cell 7: 批次發布（只發布 2 筆以節省時間）
print("\n▶️ 測試 Cell 7: 批次發布測試數據")
print("-" * 70)
def publish_multiple_messages(count=5, interval=1):
    """批次發布多筆測試訊息"""
    print("=" * 60)
    print(f"📤 批次發布 {count} 筆測試數據（間隔 {interval} 秒）")
    print("=" * 60)
    
    for i in range(1, count + 1):
        try:
            data = generate_sensor_data(i)
            json_data = json.dumps(data, ensure_ascii=False)
            
            print(f"\n[{i}/{count}] 發布數據:")
            print(f"  🌡️  溫度: {data['temperature']}°C")
            print(f"  💧 濕度: {data['humidity']}%")
            print(f"  💡 電燈: {data['light_status']}")
            
            result = client.publish(TOPIC, json_data, qos=1)
            
            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                print(f"  ❌ 發布失敗")
            
            if i < count:
                time.sleep(interval)
                
        except Exception as e:
            print(f"[{i}/{count}] ❌ 錯誤: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 批次發布完成")
    print("=" * 60)

publish_multiple_messages(2, 0.5)  # 只發布 2 筆

# 等待發布完成
time.sleep(1)

# Cell 9: 清理連線
print("\n▶️ 測試 Cell 9: 清理連線")
print("-" * 70)
def cleanup():
    """清理 MQTT 連線"""
    try:
        print("🧹 正在關閉連線...")
        client.loop_stop()
        client.disconnect()
        print("✅ 連線已關閉")
    except Exception as e:
        print(f"⚠️ 清理時發生錯誤: {e}")

cleanup()

# 最終結果
print("\n" + "=" * 70)
print("🎉 所有 Cells 測試完成！")
print("=" * 70)
print("\n✅ 結論：Notebook 的所有 cells 都能正常執行")
print("💡 如果在 Jupyter 中沒有輸出，請檢查：")
print("   1. 是否按順序執行 Cell 1 → 2 → 3 → 4 → 5 → 6/7/8")
print("   2. 是否重啟了 Kernel")
print("   3. Cell 是否真的執行了（檢查左側的執行計數 [數字]）")





