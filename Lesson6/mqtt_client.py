"""
MQTT 客戶端模組 - 訂閱 MQTT 主題並接收數據
"""
import time
import json
import random
import threading
import paho.mqtt.client as mqtt
from typing import Optional, Callable


class MQTTClient:
    """MQTT 訂閱者客戶端"""
    
    def __init__(
        self,
        broker_host="localhost",
        broker_port=1883,
        topic="客廳",
        on_message_callback: Optional[Callable] = None
    ):
        """
        初始化 MQTT 客戶端
        
        Args:
            broker_host: MQTT Broker 主機地址
            broker_port: MQTT Broker 埠號
            topic: 要訂閱的主題
            on_message_callback: 接收到訊息時的回呼函數
        """
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.topic = topic
        self.on_message_callback = on_message_callback
        
        # 建立客戶端
        client_id = f"streamlit_subscriber_{random.randint(1000, 9999)}"
        self.client = mqtt.Client(client_id=client_id)
        
        # 設定回呼函數
        self.client.on_connect = self._on_connect
        self.client.on_subscribe = self._on_subscribe
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
        
        # 連接狀態
        self.connected = False
        self.connection_error = None
        
        # 背景執行緒
        self.loop_thread: Optional[threading.Thread] = None
        self.running = False
        
        # 接收到的訊息統計
        self.messages_received = 0
        self.last_message_time = None
        self.last_message_data = None
    
    def _on_connect(self, client, userdata, flags, rc):
        """連線回呼函數"""
        if rc == 0:
            self.connected = True
            self.connection_error = None
            print(f"✓ 成功連接到 MQTT Broker: {self.broker_host}:{self.broker_port}")
            
            # 訂閱主題
            result, mid = client.subscribe(self.topic, qos=1)
            if result == mqtt.MQTT_ERR_SUCCESS:
                print(f"✓ 正在訂閱主題: {self.topic}")
            else:
                print(f"✗ 訂閱失敗，錯誤代碼: {result}")
        else:
            self.connected = False
            error_messages = {
                1: "協議版本不正確",
                2: "客戶端 ID 無效",
                3: "伺服器不可用",
                4: "用戶名或密碼錯誤",
                5: "未授權",
            }
            self.connection_error = error_messages.get(rc, f"未知錯誤 (代碼: {rc})")
            print(f"✗ 連接失敗: {self.connection_error}")
    
    def _on_subscribe(self, client, userdata, mid, granted_qos):
        """訂閱成功回呼函數"""
        print(f"✓ 成功訂閱主題 (Message ID: {mid}, QoS: {granted_qos})")
    
    def _on_message(self, client, userdata, msg):
        """接收訊息回呼函數"""
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"\n[{timestamp}] 收到訊息:")
            print(f"  主題: {topic}")
            print(f"  內容: {payload}")
            
            # 嘗試解析 JSON
            data = None
            try:
                data = json.loads(payload)
                self.last_message_data = data
            except json.JSONDecodeError:
                self.last_message_data = {"raw": payload}
            
            # 更新統計
            self.messages_received += 1
            self.last_message_time = timestamp
            
            # 呼叫外部回呼函數（傳遞 payload 和解析後的 data）
            if self.on_message_callback:
                self.on_message_callback(topic, payload, data)
                
        except Exception as e:
            print(f"處理訊息時發生錯誤: {e}")
    
    def _on_disconnect(self, client, userdata, rc):
        """斷線回呼函數"""
        self.connected = False
        if rc != 0:
            print(f"✗ 意外斷線，錯誤代碼: {rc}")
        else:
            print("✓ 已正常斷線")
    
    def connect(self):
        """連接到 MQTT Broker"""
        try:
            print(f"正在連接到 {self.broker_host}:{self.broker_port}...")
            self.client.connect(self.broker_host, self.broker_port, keepalive=60)
            self.running = True
            
            # 在背景執行緒中啟動網路迴圈
            self.loop_thread = threading.Thread(target=self._loop_forever, daemon=True)
            self.loop_thread.start()
            
            # 等待連線完成
            time.sleep(2)
            
            return self.connected
        except Exception as e:
            self.connection_error = str(e)
            print(f"✗ 連接錯誤: {e}")
            return False
    
    def _loop_forever(self):
        """在背景執行緒中運行 MQTT 迴圈"""
        self.client.loop_start()
        while self.running:
            time.sleep(0.1)
        self.client.loop_stop()
    
    def disconnect(self):
        """斷開連接"""
        self.running = False
        if self.client:
            self.client.disconnect()
            print("✓ MQTT 連線已關閉")
    
    def is_connected(self):
        """檢查連接狀態"""
        return self.connected
    
    def get_status(self):
        """獲取連接狀態資訊"""
        return {
            "connected": self.connected,
            "error": self.connection_error,
            "topic": self.topic,
            "messages_received": self.messages_received,
            "last_message_time": self.last_message_time
        }
    
    def get_last_message(self):
        """獲取最後一則訊息"""
        return self.last_message_data

