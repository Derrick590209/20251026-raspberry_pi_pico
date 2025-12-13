# 🔍 Jupyter Notebook 執行結果跑不出來 - 診斷與解決

## 📊 當前狀態

✅ Jupyter 正在運行（3 個進程）
✅ 有 3 個 Kernel 正在運行
✅ Notebook 檔案正常
⚠️ **所有 cells 都沒有輸出記錄**

---

## 🎯 問題分析

### **可能的情況：**

1. **Cells 從未被執行** ← 最可能
2. **執行了但沒有保存** 
3. **Kernel 有問題導致無法執行**
4. **輸出被清除了**

---

## ✅ 立即解決方案

### **方法 1：逐步測試（推薦）**

在 Jupyter Notebook 中，依照以下步驟：

#### **步驟 1：確認 Kernel 連接**
在 Notebook 右上角查看：
- ✅ 應該顯示：**"Python 3 | Idle"** 或類似狀態
- ❌ 如果顯示：**"No Kernel"** 或 **"Connecting"**
  - 點擊 `Kernel` → `Change Kernel` → 選擇 Python 3

#### **步驟 2：測試簡單 Cell**
在 Notebook 的任何地方新增一個測試 Cell：
```python
print("測試輸出")
1 + 1
```

按 `Shift + Enter` 執行。

**預期結果：**
```
測試輸出
2
```

- ✅ **看到輸出** → Jupyter 正常工作
- ❌ **沒有輸出** → Kernel 有問題，跳到「方法 3」

#### **步驟 3：重啟 Kernel 並清除輸出**
```
選單：Kernel → Restart Kernel and Clear All Outputs → Restart
```

#### **步驟 4：依序執行 Cells**

**特別注意：每執行一個 Cell 後，檢查是否有輸出！**

```
1. 點擊 Cell 1
2. 按 Shift + Enter
3. ⚠️ 檢查：下方是否出現 "✅ 套件匯入成功！"
   - ✅ 有 → 繼續下一個
   - ❌ 沒有 → 停止！問題在這裡

4. 重複上述步驟執行 Cell 2, 3, 4...
```

#### **步驟 5：檢查執行計數**
每個 Cell 左側應該顯示：
```
In [1]:  ← Cell 1 已執行
In [2]:  ← Cell 2 已執行
In [3]:  ← Cell 3 已執行
...
```

如果顯示 `In [ ]:` 表示該 Cell **未執行**。

---

### **方法 2：使用「Run All」測試**

#### **步驟 1：重啟 Kernel**
```
Kernel → Restart Kernel → Restart
```

#### **步驟 2：執行所有 Cells**
```
Cell → Run All
```

#### **步驟 3：觀察執行過程**
- 每個 Cell 左側會依序顯示 `In [*]`（執行中）→ `In [1]`, `In [2]`...（已完成）
- 應該會看到輸出逐漸出現

#### **步驟 4：等待執行完成**
- Cell 4 需要連接 MQTT Broker（約 1-2 秒）
- Cell 7 需要發布 5 筆數據（約 5 秒）
- 全部執行完成大約需要 10-15 秒

#### **如果中途卡住：**
按 `⏹️` (Interrupt Kernel) 按鈕，或：
```
Kernel → Interrupt Kernel
```

---

### **方法 3：Kernel 重新安裝（如果 Kernel 有問題）**

在終端機執行：

```bash
cd /home/pi/Documents/GiHub/20251026-raspberry_pi_pico

# 重新安裝 ipykernel
uv pip install --upgrade ipykernel

# 安裝 Jupyter Kernel
uv run python -m ipykernel install --user --name=mqtt_test --display-name="MQTT Test"

echo "✅ Kernel 已重新安裝"
```

然後在 Jupyter 中：
```
Kernel → Change Kernel → MQTT Test
```

---

### **方法 4：使用命令列驗證（100% 可靠）**

如果 Jupyter 一直有問題，先用這個驗證代碼是正確的：

```bash
cd /home/pi/Documents/GiHub/20251026-raspberry_pi_pico
uv run python lesson6/test_notebook_cells.py
```

**預期看到：**
```
======================================================================
🧪 測試 Notebook Cells 執行
======================================================================

▶️ 測試 Cell 1: 匯入套件
----------------------------------------------------------------------
✅ 套件匯入成功！

▶️ 測試 Cell 2: MQTT 配置
----------------------------------------------------------------------
============================================================
📡 MQTT 連線設定
...
✅ 發布成功！
...
🎉 所有 Cells 測試完成！
```

如果這個能正常輸出，證明：
- ✅ 代碼正確
- ✅ MQTT Broker 正常
- ❓ 問題在 Jupyter 的執行環境

---

## 🔧 常見問題和解決方法

### **問題 1：按了 Shift+Enter 但沒反應**

**原因：** Cell 可能正在執行其他操作

**檢查：**
- Cell 左側是否顯示 `In [*]`？
- 右上角 Kernel 狀態是否為 "Busy"？

**解決：**
- 等待當前操作完成
- 或按 `⏹️` 中斷執行

---

### **問題 2：執行後 Cell 左側沒有數字**

**原因：** Cell 沒有真正執行

**解決：**
1. 確認 Kernel 已連接（右上角不是 "No Kernel"）
2. 點擊 Cell 確保它被選中（左側有藍色或綠色邊框）
3. 再次按 `Shift + Enter`

---

### **問題 3：只看到 In [1] 但沒有輸出**

**原因：** 
- 程式有錯誤
- 或該 Cell 本來就不會產生輸出

**檢查：**
- 有沒有看到紅色錯誤訊息？
- Cell 1 應該會輸出 "✅ 套件匯入成功！"

**解決：**
- 查看錯誤訊息
- 或參考「為什麼沒有輸出.md」

---

### **問題 4：Cell 4 一直卡在執行中**

**原因：** 
- MQTT Broker 沒有運行
- 或連線有問題

**檢查 Broker：**
```bash
systemctl status mosquitto
```

**重啟 Broker：**
```bash
sudo systemctl restart mosquitto
```

---

### **問題 5：看到 "client 不存在" 錯誤**

**原因：** 沒有先執行 Cell 4

**解決：**
1. 重啟 Kernel
2. 依序執行 Cell 1 → 2 → 3 → 4
3. 確認看到 "✅ MQTT 客戶端已就緒"
4. 再執行後續 cells

---

## 📋 完整檢查清單

使用前檢查：
- [ ] Jupyter Notebook 已開啟
- [ ] Kernel 狀態顯示 "Idle"（不是 "No Kernel"）
- [ ] Mosquitto Broker 正在運行
- [ ] 已重啟 Kernel（Kernel → Restart Kernel）

執行檢查：
- [ ] 點擊 Cell 1
- [ ] 按 Shift + Enter
- [ ] **立即檢查：下方是否出現 "✅ 套件匯入成功！"**
- [ ] Cell 左側是否顯示 `In [1]`
- [ ] 依序執行 Cell 2, 3, 4，每次都確認有輸出
- [ ] Cell 4 執行後看到 "✅ MQTT 客戶端已就緒"

如果以上任一步驟失敗：
- [ ] 截圖或記錄錯誤訊息
- [ ] 檢查 Cell 左側顯示什麼（`In [ ]`, `In [*]`, 或數字）
- [ ] 檢查右上角 Kernel 狀態

---

## 🎬 視覺化操作步驟

```
1. 開啟 lesson6_1.ipynb
   ↓
2. 點擊 Kernel → Restart Kernel → Restart
   ↓
3. 點擊 Cell 1（左側出現藍色或綠色邊框）
   ↓
4. 按 Shift + Enter
   ↓
5. ⚠️ 立即檢查：下方是否出現輸出？
   ├─ ✅ 有 → 繼續 Cell 2
   └─ ❌ 沒有 → 停！問題在這裡
      ├─ 檢查 Cell 左側是否有數字
      ├─ 檢查右上角 Kernel 狀態
      └─ 嘗試再執行一次
```

---

## 🚀 快速測試命令

**在新的終端機中執行：**

```bash
cd /home/pi/Documents/GiHub/20251026-raspberry_pi_pico

echo "🧪 測試 1：驗證代碼是否正確"
uv run python lesson6/test_notebook_cells.py

echo ""
echo "🧪 測試 2：驗證 MQTT Broker"
mosquitto_pub -h localhost -t "test" -m "hello"
mosquitto_sub -h localhost -t "test" -C 1

echo ""
echo "🧪 測試 3：檢查 Jupyter 狀態"
ps aux | grep jupyter | grep -v grep

echo ""
echo "✅ 測試完成"
```

---

## 💡 最終建議

### **如果 Jupyter 一直有問題：**

**使用命令列腳本進行實際工作：**

```bash
cd /home/pi/Documents/GiHub/20251026-raspberry_pi_pico

# 終端機 1 - 訂閱者
uv run python lesson6/mqtt_subscribe_test.py

# 終端機 2 - 發布者
uv run python lesson6/mqtt_test_simple.py
```

這個方法：
- ✅ 100% 可靠
- ✅ 不會有 Jupyter 的問題
- ✅ 輸出清晰
- ✅ 容易除錯

### **Jupyter Notebook 的用途：**
- 學習和實驗
- 互動式開發
- 文檔和演示

### **命令列腳本的用途：**
- 實際測試
- 穩定運行
- 自動化任務

---

## 📞 需要更多幫助？

請提供以下資訊：

1. **Cell 左側顯示什麼？**
   - `In [ ]`（未執行）
   - `In [*]`（執行中）
   - `In [1]`（已完成）

2. **右上角 Kernel 狀態？**
   - "Python 3 | Idle"
   - "Python 3 | Busy"
   - "No Kernel"
   - 其他

3. **執行 Cell 1 後有沒有看到輸出？**
   - 有：顯示什麼？
   - 沒有：Cell 左側顯示什麼？

4. **`test_notebook_cells.py` 能正常執行嗎？**
   ```bash
   uv run python lesson6/test_notebook_cells.py
   ```

有了這些資訊，我才能精確診斷問題！





