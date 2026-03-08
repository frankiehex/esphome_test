# 本地編譯和燒錄指南 (Local Build & Flash Guide)

## 🚀 一鍵本地拉取和編譯燒錄

### 快速命令 (Copy & Paste)

```bash
# 1️⃣ 拉取最新代碼
git pull origin claude/2812-led-effects-web-zBRgM

# 2️⃣ 進入項目目錄
cd esphome_test

# 3️⃣ 編譯並燒錄
esphome run esphome_config.yaml
```

---

## 📋 詳細步驟

### 前置要求

```bash
# 檢查 Python 版本（需要 3.7+）
python3 --version

# 檢查 ESPHome 安裝
esphome version

# 若未安裝 ESPHome，執行：
pip install esphome
```

### 完整流程 (Step by Step)

#### 步驟 1: 克隆或進入項目

```bash
# 若已有項目，進入目錄
cd /path/to/esphome_test

# 若初次克隆
git clone <repository_url> esphome_test
cd esphome_test
```

#### 步驟 2: 配置 WiFi 和密鑰

```bash
# 檢查是否有 secrets.yaml
ls secrets.yaml

# 若不存在，從模板複製
cp secrets.yaml.template secrets.yaml

# 編輯配置（用你喜歡的編輯器）
nano secrets.yaml
# 或
vim secrets.yaml
# 或
code secrets.yaml  # VS Code
```

**編輯 secrets.yaml 的必填項目**

```yaml
# WiFi 設定 - 填入你的 WiFi 資訊
wifi_ssid: "YOUR_NETWORK_NAME"
wifi_password: "YOUR_PASSWORD"

# API 加密密鑰 - 生成隨機字符
api_key: "0102030405060708090a0b0c0d0e0f10"

# 密碼設定
ota_password: "your_ota_password"
web_password: "your_web_password"
```

**生成 API 密鑰**

```bash
python3 -c "import secrets; print(secrets.token_hex(16))"
# 輸出範例: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6
```

#### 步驟 3: 拉取最新代碼

```bash
# 更新到最新版本
git pull origin claude/2812-led-effects-web-zBRgM
```

#### 步驟 4: 驗證配置

```bash
# 驗證 YAML 語法和配置
esphome validate esphome_config.yaml

# 成功輸出示例：
# INFO Reading configuration esphome_config.yaml...
# INFO Configuration is valid!
```

若出現錯誤，檢查：
- `secrets.yaml` 是否存在且正確
- YAML 縮排是否使用空格（不是 Tab）
- 所有必填項目是否填寫

#### 步驟 5: 編譯

```bash
# 清除舊編譯快取（可選但建議）
esphome clean esphome_config.yaml

# 編譯配置
esphome compile esphome_config.yaml

# 等待編譯完成（3-5 分鐘）
```

#### 步驟 6: 連接 ESP32

```
1. 用 Micro USB 線連接 ESP32 到電腦
2. 確認電源指示燈亮起
3. 檢查設備是否被識別

# Linux/Mac 檢查
ls /dev/tty* | grep -i usb

# Windows 檢查
# 進入設備管理器，查看 COM 埠
```

#### 步驟 7: 燒錄韌體

```bash
# 方式 1: 自動偵測連接埠（推薦）
esphome run esphome_config.yaml

# 方式 2: 手動指定連接埠
# Linux/Mac
esphome run esphome_config.yaml --device /dev/ttyUSB0

# Windows
esphome run esphome_config.yaml --device COM3

# 方式 3: 若上傳失敗，進入 Bootloader 模式後上傳
# - 按住 BOOT 鍵
# - 短按 RST 鍵
# - 鬆開 BOOT 鍵
# - 執行: esphome run esphome_config.yaml
```

#### 步驟 8: 驗證燒錄成功

成功的標誌：

```
INFO: Successfully compiled program
INFO: Uploading .../firmware.bin
INFO: Upload complete
INFO: Waiting for ESP to reconnect...
INFO: WiFi connected!
INFO: IP Address: 192.168.1.100
```

#### 步驟 9: 訪問網頁介面

```
URL: http://192.168.1.100
用戶: admin
密碼: (你在 secrets.yaml 中設定的 web_password)
```

若無法訪問，使用 mDNS：

```
http://ws2812-led-effects.local
```

---

## 🔄 日常開發流程

### 每次修改後的操作

```bash
# 1. 拉取最新代碼
git pull origin claude/2812-led-effects-web-zBRgM

# 2. 驗證配置
esphome validate esphome_config.yaml

# 3. 清除舊編譯
esphome clean esphome_config.yaml

# 4. 編譯並燒錄
esphome run esphome_config.yaml
```

### 修改配置後的更新

**修改 LED 數量**

```bash
# 編輯配置
nano esphome_config.yaml

# 找到此行並修改
# num_leds: 30  改為你需要的數量，例如 60

# 保存並上傳
esphome run esphome_config.yaml
```

**修改 GPIO 腳位**

```bash
# 編輯配置
nano esphome_config.yaml

# 找到此行並修改
# pin: GPIO4  改為你需要的腳位，例如 GPIO23

# 保存並上傳
esphome run esphome_config.yaml
```

**修改 WiFi 設定**

```bash
# 編輯密鑰
nano secrets.yaml

# 修改
wifi_ssid: "new_network_name"
wifi_password: "new_password"

# 保存並上傳
esphome run esphome_config.yaml
```

---

## 🌐 OTA (Over-The-Air) 無線更新

第一次燒錄後，可以通過 WiFi 無線更新，無需 USB 線。

### OTA 更新步驟

```bash
# 1. 連接到同一個 WiFi 網路

# 2. 修改配置（可選）
nano esphome_config.yaml

# 3. 通過 WiFi 編譯並上傳
# 方式 1: 自動發現設備
esphome run esphome_config.yaml

# 方式 2: 指定 IP 位址
esphome run esphome_config.yaml --device 192.168.1.100

# 方式 3: 使用 mDNS 名稱
esphome run esphome_config.yaml --device ws2812-led-effects.local
```

### OTA 更新注意事項

- ✅ 前置條件：ESP32 已連接到 WiFi
- ✅ 無需 USB 線連接
- ✅ 更新需要輸入 OTA 密碼
- ✅ 更新時間：2-5 分鐘

---

## 📊 常用命令速查表

| 操作 | 命令 |
|------|------|
| 驗證配置 | `esphome validate esphome_config.yaml` |
| 查看日誌 | `esphome logs esphome_config.yaml` |
| 編譯 | `esphome compile esphome_config.yaml` |
| 清除快取 | `esphome clean esphome_config.yaml` |
| USB 燒錄 | `esphome run esphome_config.yaml` |
| OTA 無線更新 | `esphome run esphome_config.yaml --device 192.168.1.100` |
| 擦除 Flash | `esphome erase-flash esphome_config.yaml --device /dev/ttyUSB0` |
| 查看版本 | `esphome version` |

---

## 🐛 常見問題和解決方案

### ❌ "esphome: command not found"

```bash
# 安裝 ESPHome
pip install esphome

# 或升級到最新版本
pip install --upgrade esphome
```

### ❌ "secrets.yaml: No such file"

```bash
# 從模板創建
cp secrets.yaml.template secrets.yaml

# 編輯並填寫配置
nano secrets.yaml
```

### ❌ 連接埠找不到

**Linux/Mac:**
```bash
# 列出所有 USB 設備
ls /dev/tty*

# 搜索 USB 相關的
ls /dev/tty* | grep -i usb
```

**Windows:**
```bash
# 打開設備管理器 (devmgmt.msc)
# 查看 "COM 埠" 下的設備
```

### ❌ 上傳超時

```bash
# 1. 進入 Bootloader 模式
# - 按住 BOOT 鍵
# - 短按 RST 鍵
# - 鬆開 BOOT 鍵

# 2. 重試上傳
esphome run esphome_config.yaml
```

### ❌ WiFi 無法連接

```bash
# 1. 檢查 WiFi SSID 和密碼
nano secrets.yaml

# 2. 確認 WiFi 是 2.4GHz（不是 5GHz）

# 3. 重新上傳
esphome run esphome_config.yaml

# 4. 查看日誌
esphome logs esphome_config.yaml --device /dev/ttyUSB0
```

---

## 📚 文檔引用

- **安裝完整指南**: [INSTALLATION.md](INSTALLATION.md)
- **使用說明**: [USAGE.md](USAGE.md)
- **快速開始**: [QUICKSTART.md](QUICKSTART.md)
- **故障排除**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **刷機檢查清單**: [PRE_FLASH_CHECKLIST.md](PRE_FLASH_CHECKLIST.md)

---

## 🎯 完整工作流程示意圖

```
┌─────────────────────────────────────────────────────────────┐
│  開發服務器 (遠端倉庫)                                      │
│  branch: claude/2812-led-effects-web-zBRgM                 │
└────────────────────────┬────────────────────────────────────┘
                         │
                    git pull
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  你的本地電腦                                               │
│                                                             │
│  1️⃣  git pull origin claude/2812-led-effects-web-zBRgM     │
│  2️⃣  nano secrets.yaml (配置 WiFi/密鑰)                   │
│  3️⃣  esphome validate esphome_config.yaml                  │
│  4️⃣  esphome clean esphome_config.yaml                     │
│  5️⃣  esphome run esphome_config.yaml                       │
│       (連接 USB，按提示選擇連接埠)                          │
│  6️⃣  等待上傳完成 (~5 分鐘)                               │
│  7️⃣  訪問 http://192.168.1.100                            │
└─────────────────────────────────────────────────────────────┘
                         │
                    USB/WiFi
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  ESP32 開發板 + WS2812 LED                                  │
│  🎉 完成！LED 效果開始運行                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## ⏱️ 時間預估

| 步驟 | 時間 |
|------|------|
| 拉取代碼 | 1 分鐘 |
| 配置 secrets.yaml | 3 分鐘 |
| 驗證配置 | 2 分鐘 |
| 編譯 | 3-5 分鐘 |
| 上傳 | 2-3 分鐘 |
| **總計** | **11-14 分鐘** |

後續 OTA 更新：5-7 分鐘

---

## 💡 技巧

### 縮短編譯時間

```bash
# 跳過編譯驗證（不推薦）
esphome run esphome_config.yaml --no-logs

# 只編譯不上傳
esphome compile esphome_config.yaml

# 清除所有快取
rm -rf .esphome
esphome run esphome_config.yaml
```

### 調試時查看日誌

```bash
# USB 連接狀態下查看即時日誌
esphome logs esphome_config.yaml

# 遠端 WiFi 連接狀態下查看日誌
esphome logs esphome_config.yaml --device 192.168.1.100
```

### 批量修改設定

```bash
# 修改多個參數後一次提交和上傳
git pull origin claude/2812-led-effects-web-zBRgM
nano esphome_config.yaml
# 修改 num_leds, pin 等
esphome run esphome_config.yaml
```

---

## 📞 需要幫助？

1. 檢查本文檔的「常見問題」章節
2. 查看 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
3. 檢查 [PRE_FLASH_CHECKLIST.md](PRE_FLASH_CHECKLIST.md) 硬體連接
4. 查看 ESPHome 官方文件：https://esphome.io/

---

**版本**: v1.0.0
**最後更新**: 2026-03-08
**下一版本**: v1.1.0 (預計 2026-06-08)
