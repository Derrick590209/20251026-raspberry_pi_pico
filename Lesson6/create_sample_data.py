"""
建立範例 Excel 數據檔案，用於測試應用程式界面
"""
import pandas as pd
from datetime import datetime, timedelta
import random

# 建立範例數據
data = []
start_time = datetime.now() - timedelta(hours=24)  # 從 24 小時前開始

# 生成 48 筆數據（每 30 分鐘一筆）
for i in range(48):
    timestamp = start_time + timedelta(minutes=i * 30)
    
    # 溫度：20-30 度之間，有變化趨勢
    base_temp = 25 + 3 * (i % 24) / 24 - 1.5  # 模擬一天溫度變化
    temperature = round(base_temp + random.uniform(-1, 1), 1)
    
    # 濕度：50-70% 之間
    base_humidity = 60 + 5 * (i % 24) / 24 - 2.5  # 模擬一天濕度變化
    humidity = round(base_humidity + random.uniform(-3, 3), 1)
    
    # 電燈狀態：根據時間判斷（假設晚上 6 點到早上 6 點開燈）
    hour = timestamp.hour
    if 18 <= hour or hour < 6:
        light = "on"
    else:
        light = "off"
    
    data.append({
        'timestamp': timestamp,
        'light': light,
        'temperature': temperature,
        'humidity': humidity
    })

# 建立 DataFrame
df = pd.DataFrame(data)

# 儲存到 Excel
output_file = "data/mqtt_data.xlsx"
df.to_excel(output_file, index=False, engine='openpyxl')

print(f"✓ 範例 Excel 檔案已建立：{output_file}")
print(f"  - 共 {len(df)} 筆記錄")
print(f"  - 時間範圍：{df['timestamp'].min()} 至 {df['timestamp'].max()}")
print(f"  - 溫度範圍：{df['temperature'].min():.1f}°C 至 {df['temperature'].max():.1f}°C")
print(f"  - 濕度範圍：{df['humidity'].min():.1f}% 至 {df['humidity'].max():.1f}%")

