# 刷機前檢查清單 (Pre-Flash Checklist)

在上傳韌體前，請完成此檢查清單以確保設置正確。

## 📋 硬體檢查

### 開發板和 LED 燈條

- [ ] ESP32 開發板完好無損
- [ ] WS2812 / NeoPixel LED 燈條完好
- [ ] LED 燈條的 DIN、5V、GND 標籤清晰可見
- [ ] 電源供應器輸出 5V (用萬用表檢測)
- [ ] 電源供應器電流足夠 (30 LED 至少 2A, 推薦 3A)

### 連線檢查

- [ ] Micro USB 線完好，可傳輸數據（非充電線）
- [ ] 470Ω 電阻已備妥（可選但推薦）
- [ ] 100µF 濾波電容已備妥（推薦）
- [ ] 杜邦線或焊接線準備好

### 電源檢查

- [ ] 5V 電源供應器未接入任何負載
- [ ] 所有設備都已斷電
- [ ] 電源線絕緣無損
- [ ] 無短路或接觸不良跡象

## 📂 軟體檢查

### Python 環境

- [ ] Python 3.7+ 已安裝
  ```bash
  python3 --version  # 應顯示 3.7 以上版本
  ```

- [ ] pip 已安裝
  ```bash
  pip --version
  ```

### 依賴安裝

- [ ] ESPHome 已安裝
  ```bash
  pip install esphome
  ```

- [ ] ESPHome 版本 2024.1.0+
  ```bash
  esphome version
  ```

### 項目檔案

- [ ] 所有必要檔案已下載或複製:
  - [ ] esphome_config.yaml
  - [ ] version.yaml
  - [ ] secrets.yaml.template
  - [ ] 其他文檔

- [ ] 檔案位置正確
  ```bash
  ls -la esphome_config.yaml
  ```

## 🔐 配置檢查

### secrets.yaml 設定

- [ ] secrets.yaml 已從 template 複製
  ```bash
  cp secrets.yaml.template secrets.yaml
  ```

- [ ] WiFi SSID 已輸入
  ```yaml
  wifi_ssid: "YOUR_NETWORK_NAME"
  ```

- [ ] WiFi 密碼已輸入
  ```yaml
  wifi_password: "YOUR_PASSWORD"
  ```

- [ ] WiFi 網路是 2.4GHz
  （ESP32 不支援 5GHz）

- [ ] API 密鑰已生成
  ```bash
  python3 -c "import secrets; print(secrets.token_hex(16))"
  ```

- [ ] OTA 密碼已設定
  ```yaml
  ota_password: "strong_password"
  ```

- [ ] 網頁密碼已設定
  ```yaml
  web_password: "web_password"
  ```

### esphome_config.yaml 檢查

- [ ] 檔案格式正確 (YAML 縮排)
  ```bash
  esphome validate esphome_config.yaml
  ```

- [ ] LED 數量設定正確
  ```yaml
  num_leds: 30  # 改成實際 LED 數量
  ```

- [ ] GPIO 腳位設定正確
  ```yaml
  pin: GPIO4  # 確認腳位號
  ```

- [ ] WiFi 配置正確
  ```yaml
  wifi:
    ssid: !secret wifi_ssid
    password: !secret wifi_password
  ```

### 硬體配置檢查

#### GPIO 腳位

- [ ] 已確定使用的 GPIO 腳位
  - [ ] GPIO4 (預設推薦)
  - [ ] GPIO5 (替代)
  - [ ] GPIO23 (替代)
  - [ ] GPIO25 (備選)

- [ ] 該腳位未被其他設備使用

- [ ] 配置檔中的腳位與實際接線一致

#### LED 燈條數量

- [ ] LED 數量已測量或確認
  - [ ] 30 顆 (推薦起點)
  - [ ] 60 顆
  - [ ] 其他: \_\_\_\_\_

- [ ] 配置中的 num_leds 與實際一致

#### 電源容量

- [ ] 計算所需電源:
  - LED 數量: \_\_\_\_\_
  - 每顆 LED 60mA × \_\_\_\_ = \_\_\_\_\_A
  - 推薦 1.5 倍: \_\_\_\_\_A

- [ ] 電源供應器能提供所需電流
  - 實際電源: \_\_\_\_\_A (查看電源標籤)

## 🔌 USB 連接檢查

### Windows

- [ ] USB 驅動已安裝
  - [ ] CH340 驅動 (若需要)
  - [ ] CP210x 驅動 (若需要)

- [ ] 設備管理器中可見 COM 埠
  - 端口號: COM\_\_\_

### macOS

- [ ] 可以看到 /dev/cu.wchusbserial* 或類似
  ```bash
  ls /dev/cu.* | grep -i usb
  ```

### Linux

- [ ] 可以看到 /dev/ttyUSB0 或 /dev/ttyACM0
  ```bash
  ls /dev/tty* | grep -i usb
  ```

- [ ] 用戶有 dialout 權限
  ```bash
  groups | grep dialout
  ```

## 📡 網路檢查

### WiFi 網路

- [ ] WiFi 路由器已開啟
- [ ] WiFi 網路頻段是 2.4GHz (不是 5GHz)
- [ ] WiFi 訊號強度良好 (至少 -70dBm)
- [ ] 網路中無特殊安全設定 (WEP, 隱藏 SSID 可能有問題)

### 路由器設定

- [ ] DHCP 已啟用
- [ ] 連接池有可用的 IP 位址
- [ ] 防火牆允許 HTTP (port 80)
- [ ] mDNS 已啟用 (用於 .local 網址)

## ⚠️ 安全檢查

### 密碼和密鑰

- [ ] 所有預設密碼已更改
  - [ ] web_password
  - [ ] ota_password
  - [ ] api_key

- [ ] 密鑰長度足夠
  - [ ] api_key: 至少 16 個字元
  - [ ] 密碼: 至少 8 個字元

- [ ] secrets.yaml 不會被上傳到公開版本控制
  ```bash
  echo "secrets.yaml" >> .gitignore
  ```

### 電安全

- [ ] 所有接線絕緣無損
- [ ] 沒有裸露的金屬接點
- [ ] 接線不會短路
- [ ] 5V 和 GND 正確分離

## 🧪 測試前準備

### 軟體測試

- [ ] ESPHome 可以驗證配置
  ```bash
  esphome validate esphome_config.yaml
  ```

- [ ] 沒有 YAML 格式錯誤

### 硬體測試

- [ ] 萬用表已準備
  - [ ] 測試電源電壓: 應為 5V
  - [ ] 測試接地: 應為 0V
  - [ ] 檢查短路: 無蜂鳴聲

## ✨ 最終檢查清單

```
電源檢查
☐ 5V 電源連接: ESP32 5V 和 LED 5V
☐ GND 接地: ESP32 GND、LED GND、5V 電源 GND 都連接
☐ 無短路跡象

資料線
☐ GPIO4 → 470Ω 電阻 → LED DIN
☐ 絕緣無損

軟體準備
☐ secrets.yaml 已配置完整
☐ esphome_config.yaml 驗證通過
☐ WiFi SSID 和密碼正確

最終確認
☐ 所有設備斷電
☐ 所有連線檢查完畢
☐ 準備好上傳韌體
```

## 🚀 準備刷機

當以上所有項目都已勾選，你可以:

```bash
# 1. 連接 ESP32 到電腦
# 2. 執行以下命令
esphome run esphome_config.yaml

# 3. 選擇正確的 USB 埠
# 4. 等待上傳完成

# 5. 上傳完成後，ESP32 會自動重啟
```

## ✅ 上傳成功標誌

刷機成功的跡象:

```
✓ 日誌顯示 "Took ... seconds"
✓ 日誌顯示 "Upload complete"
✓ 日誌顯示 "WiFi connected"
✓ 日誌顯示 "API Server started"
✓ 日誌顯示 "Web server started"
```

## 📞 遇到問題?

| 問題 | 查看 |
|------|------|
| 硬體連接 | [INSTALLATION.md - 硬體連接](#硬體連接) |
| USB 驅動 | [INSTALLATION.md - 故障排除](#問題5-上傳失敗) |
| WiFi | [INSTALLATION.md - 故障排除](#問題2-wifi-無法連接) |
| 驗證失敗 | [INSTALLATION.md - 故障排除](#故障排除) |

---

✅ 準備好刷機了嗎？

`esphome run esphome_config.yaml`

祝你刷機順利！🚀
