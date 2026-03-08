# WS2812 LED 效果控制系統 - 安裝指南

## 目錄
1. [系統需求](#系統需求)
2. [硬體連接](#硬體連接)
3. [軟體安裝](#軟體安裝)
4. [配置設定](#配置設定)
5. [上傳韌體](#上傳韌體)
6. [網頁介面訪問](#網頁介面訪問)
7. [故障排除](#故障排除)

## 系統需求

### 硬體
- **主控板**: ESP32 Dev Kit 或相容開發板
  - 替代: ESP8266 (功能受限)
- **LED 燈條**: WS2812 / WS2812B / NeoPixel
  - 推薦: 30 顆 LED (便於測試)
  - 支援範圍: 1-1000 顆
- **電源供應**:
  - 5V DC 供應器 (足夠電流)
  - 計算公式: LED 數量 × 60mA (滿亮度下)
  - 例如: 30 顆 LED 需要約 1.8A
- **連接線**:
  - Micro USB (用於上傳和電源)
  - 杜邦線 (用於 LED 連接)

### 軟體
- Python 3.7+ (安裝 ESPHome)
- ESPHome 2024.1.0 或更新版本
- 網頁瀏覽器 (Chrome / Firefox / Safari / Edge)

## 硬體連接

### 標準連接方式

```
ESP32               WS2812 LED Strip
────────────────────────────────────
GPIO4 ────[470Ω]──→ DIN (資料線)
5V    ───────────→ 5V
GND   ───────────→ GND (接地)

外部 5V 電源
────────────
5V   ───┬────→ LED 5V
        └────→ ESP32 5V (可選)
GND  ────────→ LED GND
        └────→ ESP32 GND
```

### 連接步驟

1. **電源隔離**
   - 確保所有設備斷電

2. **GND 連接**（優先）
   ```
   ESP32 GND → WS2812 GND
   ESP32 GND → 外部 5V 電源 GND
   ```

3. **資料線連接**
   ```
   ESP32 GPIO4 → 470Ω 電阻 → WS2812 DIN
   ```

4. **電源連接**
   ```
   外部 5V 電源 → WS2812 5V
   Optional: ESP32 5V (若有 5V 接線)
   ```

5. **濾波電容**（推薦）
   ```
   在 5V 和 GND 之間連接 100µF 電容
   放在靠近 LED 燈條電源輸入處
   ```

### 替代腳位配置

若 GPIO4 被佔用，可使用其他腳位：

| 腳位 | 說明 | 相容性 |
|------|------|--------|
| GPIO5 | 推薦備選 | ✓ |
| GPIO23 | 備選腳位 | ✓ |
| GPIO25 | PWM 相容 | ✓ |

修改 `esphome_config.yaml` 第 59 行：
```yaml
output:
  - platform: ledc
    pin: GPIO23  # 改成你選擇的腳位
```

## 軟體安裝

### 1. 安裝 ESPHome

```bash
# 使用 pip 安裝
pip install esphome

# 驗證安裝
esphome version
```

### 2. 克隆或下載項目

```bash
# 如使用 git
git clone <repository_url>
cd esphome_test

# 或直接下載所有檔案到目錄
```

### 3. 項目結構

```
esphome_test/
├── esphome_config.yaml       # 主配置檔
├── version.yaml              # 版本定義
├── pins_config.yaml          # 腳位參考
├── secrets.yaml.template     # 密鑰模板
├── secrets.yaml              # 密鑰檔 (需自行創建)
├── web_interface.html        # 網頁介面
├── api_handler.py            # API 處理程序
├── test_api.py              # API 測試指令碼
├── README.md                # 項目說明
├── INSTALLATION.md          # 本檔案
└── USAGE.md                 # 使用指南
```

## 配置設定

### 1. 創建密鑰檔

```bash
# 複製模板
cp secrets.yaml.template secrets.yaml

# 編輯 secrets.yaml
nano secrets.yaml
```

### 2. 編輯 secrets.yaml

```yaml
# WiFi 設定
wifi_ssid: "YOUR_NETWORK_NAME"
wifi_password: "YOUR_NETWORK_PASSWORD"

# API 加密密鑰（生成隨機密鑰）
api_key: "0102030405060708090a0b0c0d0e0f10"

# OTA 更新密碼
ota_password: "change_me"

# 網頁密碼
web_password: "change_me"

# Home Assistant 密碼（可選）
ha_api_password: "change_me"
```

#### 生成 API 密鑰

```bash
# Linux/Mac
python3 -c "import secrets; print(secrets.token_hex(16))"

# 或使用 ESPHome
esphome config esphome_config.yaml
```

### 3. 修改 LED 配置（可選）

編輯 `esphome_config.yaml`：

```yaml
# 修改 GPIO 腳位
output:
  - platform: ledc
    pin: GPIO4  # 改成你需要的腳位

# 修改 LED 數量
light:
  - platform: neopixel
    num_leds: 30  # 改成實際 LED 數量
```

## 上傳韌體

### 使用 USB 連接的 ESP32

```bash
# 1. 驗證配置
esphome validate esphome_config.yaml

# 2. 編譯並上傳
esphome run esphome_config.yaml

# 3. 選擇連接埠（通常是 COM3 或 /dev/ttyUSB0）
```

### 首次上傳失敗的解決方案

```bash
# 清除快取並重試
esphome clean esphome_config.yaml
esphome run esphome_config.yaml

# 強制進入 bootloader 模式
# 按住 BOOT 鍵，短按 RST 鍵，然後上傳
```

### 通過 WiFi 更新（OTA）

第一次上傳後，可以通過 WiFi 更新：

```bash
esphome run esphome_config.yaml --device 192.168.1.100
```

## 網頁介面訪問

### 1. 獲取 ESP32 IP 位址

查看 ESPHome 上傳日誌或路由器連接設備列表。

範例 IP: `192.168.1.100`

### 2. 訪問網頁介面

```
http://192.168.1.100
```

### 3. 認證

- 使用者名稱: `admin`
- 密碼: `secrets.yaml` 中的 `web_password`

### 4. 可用功能

- 🔋 電源控制 (開/關)
- 🎨 6 種 LED 效果
- 🌈 8 種顏色選擇
- 💡 亮度調整 (0-100%)
- ⚡ 效果速度控制 (0-100%)
- ⚙️ LED 配置修改
- 📊 版本資訊顯示

## 故障排除

### 問題 1: LED 不亮

**可能原因**
- 電源連接不良
- GPIO 腳位配置錯誤
- LED 燈條故障

**解決方案**
```bash
# 1. 檢查上傳日誌
esphome logs esphome_config.yaml

# 2. 驗證電源
# - 使用萬用表檢查 5V 電壓
# - 測量 LED 供電電流

# 3. 檢查 GPIO 連接
# - 重新確認腳位號碼
# - 測試用 GPIO4 (預設)

# 4. 測試 LED 燈條
# 用已知工作的 Arduino 或 Raspberry Pi 測試
```

### 問題 2: WiFi 無法連接

**可能原因**
- WiFi SSID 或密碼錯誤
- WiFi 訊號太弱
- 2.4GHz WiFi 不支援 5GHz

**解決方案**
```bash
# 1. 檢查 secrets.yaml
cat secrets.yaml | grep wifi

# 2. 確認 WiFi 頻段
# ESP32 只支援 2.4GHz

# 3. 重新上傳配置
esphome run esphome_config.yaml --device <IP>

# 4. 進入 WiFi 配置模式
# - 斷電 10 秒
# 搜尋 "ws2812-fallback" WiFi 網路
# - 密碼: 12345678
```

### 問題 3: 無法訪問網頁介面

**可能原因**
- ESP32 未連接到 WiFi
- 防火牆阻擋
- IP 位址變更

**解決方案**
```bash
# 1. 檢查 ESP32 是否在線
ping 192.168.1.100

# 2. 查看 ESPHome 日誌
esphome logs esphome_config.yaml --device 192.168.1.100

# 3. 禁用防火牆（暫時測試用）
# 視系統而定

# 4. 使用 mDNS 訪問
http://ws2812-led-effects.local
```

### 問題 4: 效果不流暢或閃爍

**可能原因**
- LED 過多，計算量大
- 電源不足
- WiFi 訊號干擾

**解決方案**
```bash
# 1. 降低 LED 數量
# 在 esphome_config.yaml 中修改 num_leds

# 2. 增加電源容量
# 使用更高電流的 5V 供應器

# 3. 添加濾波電容
# 在 LED 電源側並聯 100µF 電容

# 4. 調整更新頻率
# 在 esphome_config.yaml 中降低 update_interval
```

### 問題 5: API 連線失敗

**可能原因**
- ESP32 掉線
- API 加密金鑰錯誤
- 防火牆阻擋

**解決方案**
```bash
# 1. 重啟 ESP32
# 短按 RST 鍵

# 2. 檢查 API 密鑰
# secrets.yaml 中的 api_key 必須正確

# 3. 查看日誌
esphome logs esphome_config.yaml

# 4. 禁用 API 加密（測試用）
# 在 esphome_config.yaml 中移除 encryption
```

## 進階配置

### Home Assistant 整合

在 Home Assistant configuration.yaml 添加：

```yaml
esphome:
  - name: ws2812-led-effects
```

### MQTT 支援

編輯 `esphome_config.yaml` 新增：

```yaml
mqtt:
  broker: 192.168.1.50
  username: mqtt_user
  password: mqtt_password
```

### 自訂效果

編輯 `api_handler.py` 中的 `AVAILABLE_EFFECTS` 和相應的處理函數。

## 性能優化

### 1. 降低日誌級別

```yaml
logger:
  level: WARN  # 改為 WARN 降低記憶體使用
```

### 2. 優化 LED 數量

- 30 LED: 一般使用，推薦初學者
- 60 LED: 家庭裝飾
- 100+ LED: 專業應用，需強大電源

### 3. 減少更新頻率

```yaml
effects:
  - rainbow:
      update_interval: 50ms  # 改為 100ms 降低 CPU 使用
```

## 測試

執行 API 測試：

```bash
python3 test_api.py
```

此命令測試所有 API 端點和功能。

---

有疑問? 查看 [README.md](README.md) 和 [USAGE.md](USAGE.md)
