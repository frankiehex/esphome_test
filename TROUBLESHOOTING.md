# 故障排除指南 (Troubleshooting Guide)

完整的問題診斷和解決方案。

## 🔧 常見問題和解決方案

### 📌 分類索引

- [上傳問題](#上傳問題)
- [WiFi 連線問題](#wifi-連線問題)
- [LED 硬體問題](#led-硬體問題)
- [網頁介面問題](#網頁介面問題)
- [API 問題](#api-問題)
- [效能問題](#效能問題)
- [其他問題](#其他問題)

---

## 上傳問題

### ❌ 找不到 COM 埠 / USB 設備

**錯誤訊息**
```
RuntimeError: Please specify a port to use for communication.
Could not auto-detect a serial port.
```

**原因**
- USB 驅動未安裝
- USB 線不支援數據傳輸
- 開發板未被識別
- 不同作業系統的 USB 埠命名不同

**解決方案**

1. **檢查 USB 線**
   ```bash
   # 一些 Micro USB 線只能充電，不能傳輸數據
   # 嘗試另一條線
   ```

2. **Windows - 安裝驅動**
   ```
   1. 下載 CH340 或 CP210x 驅動
   2. 插入 ESP32
   3. 設備管理器 → 尋找黃色感嘆號
   4. 右鍵 → 更新驅動程式
   5. 選擇下載的驅動檔案
   ```

3. **macOS - 檢查權限**
   ```bash
   # 檢查可用的序列埠
   ls -la /dev/cu.*

   # 應該看到類似: /dev/cu.wchusbserial14540
   ```

4. **Linux - 設置權限**
   ```bash
   # 新增用戶到 dialout 群組
   sudo usermod -a -G dialout $USER

   # 重新登入生效
   # 或執行:
   newgrp dialout
   ```

5. **指定 USB 埠**
   ```bash
   # 自動偵測失敗時，手動指定
   esphome run esphome_config.yaml --device /dev/ttyUSB0
   # 或 Windows: COM3
   # 或 macOS: /dev/cu.wchusbserial14540
   ```

### ❌ 上傳超時

**錯誤訊息**
```
Timeout waiting for acknowledgement
```

**原因**
- USB 線品質不佳
- ESP32 進入下載模式失敗
- 電源供應不足
- USB 埠供電不足

**解決方案**

1. **進入 Bootloader 模式**
   ```
   1. 按住 BOOT 按鈕不放
   2. 短按 RST (RESET) 按鈕
   3. 鬆開 BOOT 按鈕
   4. LED 應該熄滅，表示進入 bootloader 模式
   ```

2. **使用外部電源**
   ```bash
   # 某些 USB 埠供電不足，改用 5V 外部電源
   # 同時保持 USB 連接用於通訊
   ```

3. **重新上傳**
   ```bash
   esphome run esphome_config.yaml --device /dev/ttyUSB0
   ```

4. **清除快取**
   ```bash
   esphome clean esphome_config.yaml
   esphome run esphome_config.yaml
   ```

### ❌ 編譯失敗

**錯誤訊息**
```
ERROR: Failed to compile program
```

**原因**
- YAML 格式錯誤
- 缺少必要的配置
- 版本不相容

**解決方案**

1. **驗證配置**
   ```bash
   esphome validate esphome_config.yaml
   ```

2. **檢查 YAML 格式**
   ```bash
   # YAML 對縮排敏感，確保使用空格（不是 Tab）
   # 所有列表項目應以 "-" 開始
   # 所有鍵值對應以冒號分隔
   ```

3. **檢查日誌**
   ```bash
   # 查看詳細的編譯錯誤
   esphome compile esphome_config.yaml --verbose
   ```

4. **更新 ESPHome**
   ```bash
   pip install --upgrade esphome
   ```

---

## WiFi 連線問題

### ❌ WiFi 無法連接

**錯誤訊息**
```
WiFi connection failed. SSID: 'YourSSID' password: '***'
(Reason: 5)
```

**原因代碼**
- 1: 無線網路不可達
- 2: 密碼錯誤
- 3: 無線網路未找到
- 4: 連接超時
- 5: 失去信號

**解決方案**

1. **檢查 SSID 和密碼**
   ```yaml
   # secrets.yaml
   wifi_ssid: "EXACT_NETWORK_NAME"  # 區分大小寫
   wifi_password: "correct_password"  # 檢查空格和特殊字元
   ```

2. **檢查 WiFi 頻段**
   ```
   ESP32 只支援 2.4GHz
   ✓ 2.4GHz WiFi
   ✗ 5GHz WiFi

   如果路由器同時支援雙頻，
   確保 2.4GHz 頻段已啟用
   ```

3. **檢查訊號強度**
   ```bash
   # 在 ESPHome 上傳日誌中查看訊號強度
   # 應該 > -70 dBm (越接近 0 越好)
   ```

4. **嘗試 WiFi 快速連接**
   ```yaml
   wifi:
     fast_connect: true  # 跳過掃描，直接連接
   ```

5. **重新啟動路由器**
   ```
   1. 斷電路由器 10 秒
   2. 重新啟動
   3. 等待完全啟動（約 2 分鐘）
   4. 重新上傳韌體
   ```

### ❌ WiFi 連接後馬上掉線

**原因**
- WiFi 訊號太弱
- 路由器設定問題
- 功率管理問題

**解決方案**

1. **降低功耗設定**
   ```yaml
   wifi:
     ssid: !secret wifi_ssid
     password: !secret wifi_password
     fast_connect: true
   ```

2. **增加連接超時**
   ```yaml
   wifi:
     reboot_timeout: 10s
   ```

3. **禁用睡眠模式（測試用）**
   ```yaml
   wifi:
     power_save_mode: none
   ```

### ❌ 連接了但無法 ping

**原因**
- ESP32 已連接 WiFi 但無網際網路連通性
- 防火牆阻擋了 ICMP (ping)

**解決方案**

1. **使用網頁介面替代**
   ```bash
   # Ping 不通時，仍可訪問網頁
   http://192.168.1.100
   ```

2. **禁用防火牆 ping 限制**
   ```
   視路由器設定而定
   通常在路由器管理介面設定
   ```

3. **使用 mDNS 訪問**
   ```bash
   http://ws2812-led-effects.local
   ```

---

## LED 硬體問題

### ❌ LED 完全不亮

**檢查清單**
- [ ] 5V 電源已連接到 LED
- [ ] GND 已正確接地
- [ ] GPIO4 (或配置的腳位) 有訊號輸出

**診斷步驟**

1. **確認電源**
   ```bash
   # 用萬用表測試
   - 5V 和 GND 之間應有 5V 電壓
   - LED 紅線連接 5V
   - LED 黑線連接 GND
   ```

2. **檢查數據線**
   ```bash
   # GPIO 應該有約 3.3V 的邏輯電平
   # 可以用示波器或邏輯分析儀檢查
   ```

3. **驗證 LED 燈條**
   ```bash
   # 用已知工作的控制器測試 LED
   # 或用 Arduino 和簡單代碼測試
   ```

4. **查看日誌**
   ```bash
   esphome logs esphome_config.yaml
   # 查看是否有與 LED 相關的錯誤
   ```

### ❌ LED 只有部分亮起

**原因**
- LED 燈條損壞
- 電源不足
- 資料線接觸不良

**解決方案**

1. **測試個別段落**
   ```yaml
   # 暫時減少 LED 數量測試
   num_leds: 10  # 先試 10 顆
   ```

2. **檢查接線**
   ```
   確保 DIN 連接到第一顆 LED
   不是連接到中間或末端
   ```

3. **測試電源容量**
   ```bash
   # 30 顆全白色:
   # 應該消耗 1.8A (30 × 60mA)
   # 檢查電源是否有足夠能力
   ```

### ⚠️ LED 閃爍或不穩定

**原因**
- 電源不穩定
- 電源線過長
- 缺少濾波電容
- 電源供應不足

**解決方案**

1. **添加濾波電容**
   ```
   在 LED 5V 和 GND 之間並聯:
   - 100µF 電解電容
   - 位置: 靠近 LED 電源輸入
   ```

2. **升級電源**
   ```bash
   # 檢查電源規格
   # 應該 > 30 LED × 60mA × 1.5 = 2.7A
   # 推薦使用 3-5A 電源
   ```

3. **縮短電源線**
   ```bash
   # 如果電源線很長，
   # 使用粗的電源線 (14 AWG 或更粗)
   ```

4. **添加本地濾波**
   ```yaml
   # 在 esphome_config.yaml 中
   color_correct: [50%, 50%, 50%]
   ```

---

## 網頁介面問題

### ❌ 無法訪問 http://192.168.1.100

**原因**
- ESP32 未連接到 WiFi
- IP 位址已更改
- 防火牆阻擋
- 網頁伺服器未啟動

**解決方案**

1. **確認 ESP32 連接到 WiFi**
   ```bash
   esphome logs esphome_config.yaml
   # 應該看到: "WiFi connected"
   ```

2. **查找實際 IP 位址**
   ```bash
   # 方法 1: ESPHome 日誌
   esphome logs esphome_config.yaml
   # 查找: "IP Address: 192.168.x.x"

   # 方法 2: 路由器管理介面
   # 登入路由器，查看連接設備列表

   # 方法 3: 使用 mDNS
   # http://ws2812-led-effects.local
   ```

3. **禁用防火牆測試**
   ```bash
   # 暫時禁用防火牆以測試連接
   # 確認問題後重新啟用
   ```

4. **重啟 ESP32**
   ```bash
   # 短按 RST 按鈕重啟
   ```

### ❌ 無法登入網頁

**原因**
- 密碼錯誤
- 密碼未在 secrets.yaml 中設定

**解決方案**

1. **檢查密碼**
   ```yaml
   # secrets.yaml
   web_password: "check_this_password"
   ```

2. **重置密碼**
   ```bash
   # 編輯 secrets.yaml
   nano secrets.yaml

   # 修改 web_password
   web_password: "new_password"

   # 重新上傳
   esphome run esphome_config.yaml
   ```

3. **使用預設密碼**
   ```
   用戶名: admin
   密碼: (查看 esphome_config.yaml 中的設定)
   ```

### ❌ 網頁加載但 LED 不响應

**原因**
- API 未正常運行
- 連線已斷開
- 韌體問題

**解決方案**

1. **檢查 API 連線狀態**
   ```
   在網頁上應該看到:
   ✓ 已連接 (綠色)
   或
   ✗ 未連接 (紅色)
   ```

2. **查看伺服器日誌**
   ```bash
   esphome logs esphome_config.yaml
   # 查找 API 相關的錯誤訊息
   ```

3. **重新上傳韌體**
   ```bash
   esphome clean esphome_config.yaml
   esphome run esphome_config.yaml
   ```

---

## API 問題

### ❌ API 命令返回錯誤

**錯誤: 未知效果**
```json
{"error": "Unknown effect: invalid_effect"}
```
**解決方案**: 使用有效的效果名稱 (pulse, rainbow, strobe, scan, twinkle, random)

**錯誤: 未知顏色**
```json
{"error": "Unknown color: invalid_color"}
```
**解決方案**: 使用有效的顏色 (red, green, blue, white, purple, cyan, yellow, orange)

**錯誤: JSON 格式錯誤**
```json
{"error": "Invalid JSON"}
```
**解決方案**:
```bash
# 確保 JSON 格式正確
curl -X POST http://192.168.1.100/api/command \
  -H "Content-Type: application/json" \
  -d '{"command": "power", "state": true}'
  # ↑ 完整的 JSON 物件
```

### ❌ API 無回應

**原因**
- API 伺服器未啟動
- 網路連線失敗
- 加密金鑰不匹配

**解決方案**

1. **檢查 API 日誌**
   ```bash
   esphome logs esphome_config.yaml
   # 查找: "API Server started"
   ```

2. **禁用 API 加密（測試用）**
   ```yaml
   api:
     # encryption:
     #   key: !secret api_key
     (暫時註解加密)
   ```

3. **重新生成加密金鑰**
   ```bash
   python3 -c "import secrets; print(secrets.token_hex(16))"
   # 更新 secrets.yaml 中的 api_key
   ```

---

## 效能問題

### 🐢 LED 效果很慢或卡頓

**原因**
- LED 數量過多
- 更新頻率太高
- 電源供應不足
- WiFi 干擾

**解決方案**

1. **減少 LED 數量**
   ```yaml
   num_leds: 30  # 改為更小的數字
   ```

2. **降低更新頻率**
   ```yaml
   effects:
     - rainbow:
         update_interval: 50ms  # 改為 100ms
   ```

3. **降低亮度**
   ```
   在網頁中將亮度設為 70-80%
   ```

4. **增加電源容量**
   ```bash
   檢查電源規格，升級到更大容量
   ```

### 💾 記憶體不足

**錯誤訊息**
```
Out of memory
```

**解決方案**

1. **禁用日誌**
   ```yaml
   logger:
     level: WARN
   ```

2. **減少 API 日誌**
   ```yaml
   logger:
     logs:
       api: NONE
   ```

---

## 其他問題

### ❌ 設備頻繁重啟

**原因**
- 看門狗超時 (Watchdog timeout)
- 記憶體不足
- 電源不穩定

**解決方案**

1. **增加看門狗超時**
   ```yaml
   logger:
     level: WARN

   # 禁用某些功能
   api:
     reboot_timeout: 15min
   ```

2. **降低日誌級別**
   ```yaml
   logger:
     level: ERROR
   ```

3. **檢查電源**
   ```bash
   使用外部電源而非 USB 供電
   ```

### ❌ 無線訊號不穩定

**原因**
- 2.4GHz 干擾 (WiFi、藍牙、微波爐)
- 距離太遠
- 路由器天線位置不佳

**解決方案**

1. **移近路由器**
   ```bash
   在路由器附近測試
   ```

2. **改變天線方向**
   ```bash
   嘗試不同的天線方向或位置
   ```

3. **減少干擾源**
   ```bash
   遠離微波爐、無繩電話等 2.4GHz 設備
   ```

---

## 🆘 緊急復原程序

如果以上解決方案都不工作，嘗試完全重置：

```bash
# 1. 完全清除快取
esphome clean esphome_config.yaml

# 2. 進入 Bootloader 模式
# - 按住 BOOT 鍵
# - 短按 RST 鍵
# - 鬆開 BOOT 鍵

# 3. 擦除 Flash
esphome erase-flash esphome_config.yaml --device /dev/ttyUSB0

# 4. 重新上傳
esphome run esphome_config.yaml --device /dev/ttyUSB0

# 5. 重新配置 WiFi
# 首次啟動時會建立 "ws2812-fallback" WiFi 熱點
# 連接後在線上設定 WiFi 憑證
```

---

## 📞 獲取幫助

| 問題類型 | 資源 |
|---------|------|
| 硬體配置 | [INSTALLATION.md](INSTALLATION.md) |
| 使用說明 | [USAGE.md](USAGE.md) |
| 安裝檢查 | [PRE_FLASH_CHECKLIST.md](PRE_FLASH_CHECKLIST.md) |
| 快速開始 | [QUICKSTART.md](QUICKSTART.md) |

---

版本: v1.0.0 | 最後更新: 2026-03-08

仍然無法解決？查看 ESPHome 官方文件：https://esphome.io/guides/faq.html
