"""
數據處理模組 - 處理 MQTT 數據並儲存到 Excel 檔案
"""
import os
import json
import pandas as pd
from datetime import datetime
from pathlib import Path


class DataHandler:
    """處理和儲存 MQTT 數據到 Excel 檔案"""
    
    def __init__(self, data_dir="data"):
        """
        初始化數據處理器
        
        Args:
            data_dir: Excel 檔案儲存目錄
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.excel_file = self.data_dir / "mqtt_data.xlsx"
        
        # 初始化 DataFrame
        self.df = self._load_existing_data()
    
    def _load_existing_data(self):
        """載入現有的 Excel 數據"""
        if self.excel_file.exists():
            try:
                df = pd.read_excel(self.excel_file)
                # 確保時間戳記欄位是 datetime 類型
                if 'timestamp' in df.columns:
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                return df
            except Exception as e:
                print(f"載入現有數據時發生錯誤: {e}")
                return pd.DataFrame()
        else:
            return pd.DataFrame()
    
    def parse_message(self, message_payload):
        """
        解析 MQTT 訊息
        
        Args:
            message_payload: MQTT 訊息內容（JSON 字串或字典）
            
        Returns:
            dict: 解析後的數據字典，包含 timestamp, light, temperature, humidity
        """
        try:
            # 如果是字串，嘗試解析為 JSON
            if isinstance(message_payload, str):
                data = json.loads(message_payload)
            elif isinstance(message_payload, dict):
                data = message_payload
            else:
                raise ValueError("不支援的訊息格式")
            
            # 提取數據
            timestamp = datetime.now()
            if 'timestamp' in data:
                try:
                    timestamp = pd.to_datetime(data['timestamp'])
                except:
                    timestamp = datetime.now()
            
            light = data.get('light', 'unknown')
            temperature = data.get('temperature', None)
            humidity = data.get('humidity', None)
            
            return {
                'timestamp': timestamp,
                'light': light,
                'temperature': temperature,
                'humidity': humidity
            }
        except json.JSONDecodeError as e:
            print(f"JSON 解析錯誤: {e}")
            return None
        except Exception as e:
            print(f"解析訊息時發生錯誤: {e}")
            return None
    
    def add_data(self, data_dict):
        """
        添加數據到 DataFrame 並儲存到 Excel
        
        Args:
            data_dict: 包含 timestamp, light, temperature, humidity 的字典
        """
        if data_dict is None:
            return
        
        try:
            # 建立新的 DataFrame 行
            new_row = pd.DataFrame([data_dict])
            
            # 如果 DataFrame 為空，直接使用新行
            if self.df.empty:
                self.df = new_row
            else:
                # 追加新行
                self.df = pd.concat([self.df, new_row], ignore_index=True)
            
            # 儲存到 Excel
            self.save_to_excel()
            
        except Exception as e:
            print(f"添加數據時發生錯誤: {e}")
    
    def save_to_excel(self):
        """將 DataFrame 儲存到 Excel 檔案"""
        try:
            # 確保時間戳記格式正確
            if 'timestamp' in self.df.columns:
                self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
            
            # 儲存到 Excel
            self.df.to_excel(self.excel_file, index=False, engine='openpyxl')
            
        except Exception as e:
            print(f"儲存 Excel 檔案時發生錯誤: {e}")
    
    def get_recent_data(self, limit=100):
        """
        獲取最近的數據記錄
        
        Args:
            limit: 返回的記錄數量
            
        Returns:
            DataFrame: 最近的數據記錄
        """
        if self.df.empty:
            return pd.DataFrame()
        
        # 按時間戳記排序，返回最近的記錄
        sorted_df = self.df.sort_values('timestamp', ascending=False)
        return sorted_df.head(limit)
    
    def get_all_data(self):
        """
        獲取所有數據
        
        Returns:
            DataFrame: 所有數據記錄
        """
        return self.df.copy()
    
    def get_chart_data(self):
        """
        獲取用於繪圖的數據（時間序列）
        
        Returns:
            DataFrame: 包含時間戳記、溫度、濕度的數據
        """
        if self.df.empty:
            return pd.DataFrame()
        
        # 選擇需要的欄位並按時間排序
        chart_df = self.df[['timestamp', 'temperature', 'humidity']].copy()
        chart_df = chart_df.sort_values('timestamp')
        
        # 設定時間戳記為索引
        chart_df = chart_df.set_index('timestamp')
        
        return chart_df

