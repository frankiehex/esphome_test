# WS2812 LED 效果控制系統

這是一個完整的 ESP32/ESP8266 WS2812 (NeoPixel) LED 燈效控制系統，包含 ESPHome 配置和網頁控制介面。

## 功能特性

### 🎨 LED 效果
- **Pulse** - 呼吸效果
- **Rainbow** - 彩虹漸變
- **Strobe** - 閃爍效果
- **Scan** - 掃描效果
- **Twinkle** - 閃爍變幻
- **Random** - 隨機顏色

### 🎛️ 控制功能
- 電源開關
- 8 種顏色選擇 (紅、綠、藍、白、紫、青、黃、橙)
- 亮度調整 (0-100%)
- 效果速度控制 (0-100%)
- LED 數量配置
- GPIO 腳位設定

### 🌐 網頁介面
- 響應式設計，支援桌機和行動裝置
- 即時狀態顯示
- 版本資訊展示
- 連線狀態監控

### 📦 版本控制
- 應用程式版本：v1.0.0
- 建置日期：2026-03-08
- 韌體版本追蹤

## 硬體需求

- ESP32 開發板或 ESP8266 模組
- WS2812 / NeoPixel LED 燈條 (推薦 30 顆 LED)
- 5V 電源供應 (充足的電流)
- 資料線接 GPIO4 (可在配置中修改)

## 快速開始

### 1. 設定 WiFi 和密鑰

```bash
# 複製密鑰模板
cp secrets.yaml.template secrets.yaml

# 編輯 secrets.yaml，填入你的 WiFi 信息和密鑰
nano secrets.yaml
```

### 2. 上傳到 ESP32

```bash
# 安裝 esphome 工具
pip install esphome

# 驗證配置
esphome config validate esphome_config.yaml

# 編譯並上傳
esphome run esphome_config.yaml
```

### 3. 訪問網頁介面

上傳完成後，在瀏覽器中訪問：
```
http://<ESP32_IP>
```

用戶名：`admin`
密碼：查看 `secrets.yaml` 中的 `web_password`

## 硬體腳位配置

### 預設配置
- **GPIO4** - WS2812 資料線 (推薦)

### 其他可用腳位
- GPIO23 - 替代腳位
- GPIO5 - 替代腳位
- GPIO25 - PWM 相容腳位

## API 端點

### POST /api/command
發送命令到控制器

```json
{
  "command": "power",
  "state": true
}
```

### GET /api/status
取得當前狀態

### GET /api/info
取得設備資訊和版本

### GET /api/version
取得版本號資訊

## 命令格式

### Power 命令
```json
{"command": "power", "state": true}
```

### Effect 命令
```json
{"command": "effect", "effect": "rainbow"}
```

### Color 命令
```json
{"command": "color", "color": "blue"}
```

### Brightness 命令
```json
{"command": "brightness", "brightness": 75}
```

### Speed 命令
```json
{"command": "speed", "speed": 50}
```

### Config 命令
```json
{"command": "config", "ledCount": 30, "ledPin": 4}
```

## 版本歷史

### v1.0.0 (2026-03-08)
- 初始版本
- 支援 6 種 LED 效果
- 網頁控制介面
- 版本資訊顯示

## 檔案結構

```
esphome_test/
├── esphome_config.yaml      # ESPHome 主配置檔
├── version.yaml             # 版本控制配置
├── web_interface.html       # 網頁控制介面
├── api_handler.py           # API 處理程序
├── secrets.yaml.template    # 密鑰模板
└── README.md               # 本檔案
```

## 故障排除

### LED 不亮
- 檢查 GPIO 腳位設定是否正確
- 確認 5V 電源連接正確
- 檢查資料線接線

### 無法訪問網頁介面
- 確認 ESP32 已連接到 WiFi
- 檢查防火牆設定
- 重啟 ESP32

### 效果不流暢
- 減少 LED 數量
- 降低更新頻率
- 檢查電源是否充足

## 技術細節

### 使用技術
- **ESPHome** - 韌體框架
- **HTML5/CSS3/JavaScript** - 網頁介面
- **Python** - API 處理

### 相容性
- ESP32 Dev Kit
- ESP8266 (部分功能)
- ESPHome 2024.1.0 及以上版本

## 授權

MIT License

## 支援

如有問題，請檢查：
1. ESPHome 官方文件：https://esphome.io/
2. 日誌輸出：檢查 ESP32 串列埠輸出
3. 網頁控制台：http://&lt;ESP32_IP&gt;:80

---

版本：v1.0.0 | 最後更新：2026-03-08
