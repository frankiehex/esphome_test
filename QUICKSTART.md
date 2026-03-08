# 快速開始指南 (Quick Start)

## ⚡ 5 分鐘快速入門

### 步驟 1: 準備硬體 (1 分鐘)

✓ 檢查清單:
- [ ] ESP32 開發板
- [ ] WS2812 LED 燈條 (至少 30 顆)
- [ ] 5V 電源供應器
- [ ] Micro USB 線

### 步驟 2: 硬體連接 (2 分鐘)

#### 簡單方案 (推薦)

```
ESP32 GPIO4  ──[470Ω電阻]──> LED DIN
ESP32 GND    ──────────────> LED GND
5V 電源      ──────────────> LED 5V
5V 電源      ──────────────> ESP32 5V (可選)
```

#### 完整方案

```
╔════════════════╗         ╔════════════════╗
║    ESP32       ║         ║   5V 電源      ║
║                ║         ║                ║
║ GPIO4 ─────[470Ω]──┐     │ +5V ──┬────────┤
║ GND ────────────┼──┼─────│ GND   │        │
║ 5V  ────────────┼──┘     └───────┤        │
╚════════════════╝        ╔════════════════╗
                          ║  WS2812 LED    ║
                          ║                ║
                    DIN ──┘ +5V ────────────┤
                    GND ──────────────────┘
                    (加 100µF 濾波電容)
```

### 步驟 3: 軟體設定 (1 分鐘)

```bash
# 複製密鑰模板
cp secrets.yaml.template secrets.yaml

# 編輯 secrets.yaml
# 修改: wifi_ssid, wifi_password
nano secrets.yaml
```

### 步驟 4: 上傳韌體 (1 分鐘)

```bash
# 安裝 ESPHome (如未安裝)
pip install esphome

# 上傳到 ESP32
esphome run esphome_config.yaml

# 選擇連接埠（通常是 COM3 或 /dev/ttyUSB0）
```

## ✅ 驗證設置

### 檢查清單

```
[ ] WiFi 已連接
    → 查看 ESPHome 日誌: "WiFi connected"

[ ] API 已啟動
    → 日誌中顯示: "API Server started"

[ ] 網頁伺服器已啟動
    → 日誌中顯示: "Web server started"

[ ] LED 可控制
    → 在網頁中點 [開啟] 按鈕，LED 亮起
```

## 🌐 訪問網頁介面

```
URL: http://<ESP32_IP>
例如: http://192.168.1.100

登入:
用戶: admin
密碼: <secrets.yaml 中的 web_password>
```

## 🎨 立即試用

1. **開啟 LED**
   ```
   點擊 [開啟] 按鈕
   ```

2. **選擇效果**
   ```
   選擇: Rainbow
   ```

3. **調整亮度**
   ```
   亮度滑條: 拖到 70%
   ```

4. **觀看效果**
   ```
   彩虹色彩應該在 LED 燈條上循環流動
   ```

## 🐛 如果不工作?

### 問題 1: 找不到 ESP32 IP

```bash
# 檢查 ESPHome 日誌
esphome logs esphome_config.yaml

# 或查看路由器連接設備列表

# 通常形式: 192.168.1.XXX
```

### 問題 2: LED 不亮

```bash
# 檢查硬體連接
☑ 5V 電源已連接
☑ GND 接地正確
☑ GPIO4 資料線已連接

# 驗證配置
esphome validate esphome_config.yaml

# 重新上傳
esphome run esphome_config.yaml
```

### 問題 3: 無法訪問網頁

```bash
# 使用 mDNS 替代 IP
http://ws2812-led-effects.local

# 或 ping 檢查連線
ping 192.168.1.100
```

## 📚 進階設定

### 修改 LED 數量

編輯 `esphome_config.yaml`:

```yaml
light:
  - platform: neopixel
    num_leds: 60  # 改成你的 LED 數量
```

上傳: `esphome run esphome_config.yaml`

### 修改 GPIO 腳位

編輯 `esphome_config.yaml`:

```yaml
output:
  - platform: ledc
    pin: GPIO23  # 改成你需要的腳位
```

上傳: `esphome run esphome_config.yaml`

## 🚀 後續步驟

1. ✓ 閱讀 [USAGE.md](USAGE.md) - 深入了解所有功能
2. ✓ 閱讀 [INSTALLATION.md](INSTALLATION.md) - 完整配置指南
3. ✓ 嘗試 API 控制 - 自動化您的 LED
4. ✓ 探索不同的效果組合

## 📞 需要幫助?

| 問題 | 位置 |
|------|------|
| 硬體接線 | [INSTALLATION.md - 硬體連接](#硬體連接) |
| 使用功能 | [USAGE.md](USAGE.md) |
| API 文檔 | [USAGE.md - 進階功能](#進階功能) |
| 故障排除 | [INSTALLATION.md - 故障排除](#故障排除) |

## 版本資訊

- **版本**: v1.0.0
- **日期**: 2026-03-08
- **狀態**: ✅ 穩定版本

---

🎉 祝賀! 你已成功設置 WS2812 LED 效果控制系統!

有任何問題，查看完整文檔或重新執行 `test_api.py` 驗證系統。
