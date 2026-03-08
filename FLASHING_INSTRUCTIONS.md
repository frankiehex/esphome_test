# 固件燒錄說明

編譯完成！以下是三個固件文件及其用途：

## 可用的固件文件

### 1. **ws2812-led-effects-factory.bin** (1015 KB)
首次燒錄到 ESP32 時使用此文件

```bash
esphome run esphome_config.yaml
```

或使用 esptool.py：
```bash
python3 -m esptool --chip esp32 --port /dev/ttyUSB0 write_flash 0x0 ws2812-led-effects-factory.bin
```

### 2. **ws2812-led-effects-ota.bin** (951 KB)
用於 OTA（無線）更新現有固件

在 Home Assistant 或直接通過 API：
```bash
esphome upload esphome_config.yaml
```

### 3. **ws2812-led-effects.bin** (951 KB)
標準固件二進制文件（與 .ota.bin 相同）

## 快速開始

### 方式 1：使用 ESPHome CLI（推薦）

1. 確保已安裝依賴：
```bash
source esphome_env/bin/activate
pip install esphome
```

2. 連接 ESP32 到電腦（USB）

3. 執行以下命令：
```bash
esphome run esphome_config.yaml
```

### 方式 2：使用 esptool.py

1. 安裝 esptool：
```bash
pip install esptool
```

2. 找到 USB 端口（Linux/Mac）：
```bash
ls /dev/ttyUSB*   # 或 /dev/tty.usbserial-*
```

3. 燒錄固件：
```bash
python3 -m esptool --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash 0x0 ws2812-led-effects-factory.bin
```

### 方式 3：使用 ESPHome Web 燒錄工具

訪問 [https://web.esphome.io](https://web.esphome.io) 使用網頁燒錄工具

## 燒錄後配置

1. **WiFi 設置**
   - 設備會以 `ws2812-fallback` SSID 廣播 AP
   - 密碼：`12345678`
   - 連接後訪問 `192.168.4.1` 配置 WiFi

2. **Web 介面**
   - 燒錄完成後，訪問設備 IP 地址
   - 用戶名：`admin`
   - 密碼：在 `secrets.yaml` 中配置的 `web_password`

3. **LED 控制**
   - 支持以下效果：
     - Pulse（脈衝）
     - Random（隨機）
     - Strobe（頻閃）

## 故障排除

### 找不到 USB 端口
```bash
# Linux
dmesg | tail -20

# Mac
ls /dev/tty.* | grep usb

# Windows
# 設備管理器中查找 COM 端口
```

### 燒錄超時
- 按住 ESP32 上的 BOOT 按鈕
- 降低波特率至 115200

### 連接失敗
- 檢查 USB 線是否正確連接
- 嘗試更新驅動程序或使用不同的 USB 端口

## 其他命令

```bash
# 驗證配置
esphome validate esphome_config.yaml

# 只編譯不燒錄
esphome compile esphome_config.yaml

# 清潔構建
esphome clean esphome_config.yaml
esphome compile esphome_config.yaml
```

## 安全注意事項

- ⚠️ **備份** `secrets.yaml` - 包含敏感信息
- 🔒 **更改密碼** - 更新 `secrets.yaml` 中的所有密碼
- 🛡️ **設置 WiFi** - 使用強密碼
- 🔑 **API 密鑰** - 已生成唯一的加密密鑰

祝燒錄成功！🎉
