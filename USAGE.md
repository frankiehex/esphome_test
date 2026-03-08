# WS2812 LED 效果控制系統 - 使用指南

## 快速開始

### 1. 訪問網頁介面

```
http://<ESP32_IP>
例如: http://192.168.1.100
```

### 2. 登入

- 使用者名稱: `admin`
- 密碼: 您在 `secrets.yaml` 中設定的密碼

### 3. 開始控制 LED

## 網頁介面說明

### 頭部區域

#### 版本資訊
- **版本號**: 應用程式版本（v1.0.0）
- **建置日期**: 韌體建置日期（2026-03-08）
- **設備**: 設備名稱（WS2812 LED Controller）

### 功能區域

#### 1️⃣ 電源控制

```
[開啟]  [關閉]
```

點選按鈕控制 LED 燈條的開/關。

- **開啟**: LED 燈條亮起，執行當前效果
- **關閉**: LED 燈條關閉，所有 LED 熄滅

#### 2️⃣ LED 效果選擇

| 效果 | 描述 | 適用場景 |
|------|------|--------|
| **Pulse** | 呼吸效果，亮度漸進變化 | 舒緩、睡眠氛圍 |
| **Rainbow** | 彩虹漸變，循環輪轉 | 派對、裝飾 |
| **Strobe** | 快速閃爍，支援多色 | 動感、警示 |
| **Scan** | 掃描效果，光點移動 | 科技、互動 |
| **Twinkle** | 閃爍變幻，隨機亮滅 | 星空、夢幻 |
| **Random** | 隨機色彩變化 | 動態、隨機 |

使用方法：直接點選效果按鈕。

#### 3️⃣ 顏色選擇

```
🔴 🟢 🔵 ⚪ 🟣 🟦 🟨 🟠
紅 綠 藍 白 紫 青 黃 橙
```

- 點選顏色按鈕應用該顏色
- 不同效果與顏色組合產生不同視覺效果

**顏色組合建議**
| 效果 | 推薦顏色 |
|------|--------|
| Pulse | 白色、青色、紫色 |
| Rainbow | 所有顏色（自動循環） |
| Strobe | 紅色、白色、黃色 |
| Scan | 藍色、綠色、紫色 |
| Twinkle | 白色、黃色 |

#### 4️⃣ 亮度控制

```
亮度: [████████░░] 100%
```

- 滑動條調整亮度（0-100%）
- 0%: 完全關閉
- 50%: 中等亮度，省電模式
- 100%: 最高亮度，耗電最高

**亮度與電源消耗**
```
30 顆 LED 全白色
50% 亮度: 約 0.9A
100% 亮度: 約 1.8A
```

#### 5️⃣ 效果速度

```
效果速度: [████░░░░░░] 50%
```

- 調整 LED 效果的動畫速度
- 0%: 非常慢，靜止狀態
- 50%: 正常速度（推薦）
- 100%: 非常快，高速動畫

**速度建議**
| 效果 | 推薦速度 |
|------|--------|
| Pulse | 30-50% |
| Rainbow | 40-60% |
| Strobe | 60-80% |
| Scan | 50-70% |
| Twinkle | 20-40% |
| Random | 40-60% |

#### 6️⃣ LED 配置

```
LED 數量: [30         ]
GPIO 腳位: [4          ]
```

**LED 數量**
- 範圍: 1-1000
- 預設: 30
- 修改後無需重啟，立即生效

**GPIO 腳位**
- 有效範圍: 0-39 (ESP32)
- 預設: 4 (推薦)
- 替代選項: 5, 23, 25
- 修改後可能需要重啟

### 連接狀態指示

```
✓ [已連接]        設備與伺服器連線中
✗ [未連接]        設備離線或無法通訊
```

- 狀態會自動每 5 秒更新一次
- 綠色: 連線正常
- 紅色: 連線失敗

## 使用場景範例

### 場景 1: 舒眠模式

```
1. 點選 [開啟]
2. 選擇效果: Pulse
3. 選擇顏色: 青色
4. 亮度: 20%
5. 速度: 30%
```

效果: 溫和的呼吸效果，有利於放鬆和入睡。

### 場景 2: 派對模式

```
1. 點選 [開啟]
2. 選擇效果: Strobe
3. 選擇顏色: 紅色
4. 亮度: 100%
5. 速度: 75%
```

效果: 快速閃爍，營造派對氛圍。

### 場景 3: 工作環境

```
1. 點選 [開啟]
2. 選擇效果: Rainbow
3. 選擇顏色: 白色（Rainbow 自動循環）
4. 亮度: 60%
5. 速度: 40%
```

效果: 柔和的彩虹漸變，提升工作環境氛圍。

### 場景 4: 夜間照明

```
1. 點選 [開啟]
2. 選擇效果: Twinkle
3. 選擇顏色: 黃色
4. 亮度: 40%
5. 速度: 25%
```

效果: 溫暖的閃爍，提供柔和照明。

## 進階功能

### API 直接控制

使用 HTTP 請求直接控制 LED（適合自動化）。

#### 基本 URL

```
http://<ESP32_IP>/api/
```

#### 端點列表

##### GET /api/status
取得當前狀態

```bash
curl http://192.168.1.100/api/status
```

回應:
```json
{
  "status": "ok",
  "power": true,
  "effect": "pulse",
  "color": "red",
  "brightness": 100,
  "speed": 50,
  "led_count": 30,
  "led_pin": 4
}
```

##### GET /api/info
取得設備資訊

```bash
curl http://192.168.1.100/api/info
```

回應:
```json
{
  "version": "1.0.0",
  "build_date": "2026-03-08",
  "firmware_version": "1.0.0",
  "available_effects": ["pulse", "rainbow", ...],
  "available_colors": ["red", "green", ...],
  "led_config": {...}
}
```

##### POST /api/command
發送命令

```bash
# 開啟 LED
curl -X POST http://192.168.1.100/api/command \
  -H "Content-Type: application/json" \
  -d '{"command": "power", "state": true}'

# 設定效果
curl -X POST http://192.168.1.100/api/command \
  -H "Content-Type: application/json" \
  -d '{"command": "effect", "effect": "rainbow"}'

# 設定亮度
curl -X POST http://192.168.1.100/api/command \
  -H "Content-Type: application/json" \
  -d '{"command": "brightness", "brightness": 75}'
```

#### 支援的命令

**power**
```json
{"command": "power", "state": true|false}
```

**effect**
```json
{"command": "effect", "effect": "pulse|rainbow|strobe|scan|twinkle|random"}
```

**color**
```json
{"command": "color", "color": "red|green|blue|white|purple|cyan|yellow|orange"}
```

**brightness**
```json
{"command": "brightness", "brightness": 0-100}
```

**speed**
```json
{"command": "speed", "speed": 0-100}
```

**config**
```json
{"command": "config", "ledCount": 1-1000, "ledPin": 0-39}
```

### Python 自動化範例

```python
import requests
import json

ESP_IP = "192.168.1.100"
API_BASE = f"http://{ESP_IP}/api"

def send_command(command, data={}):
    """發送命令到 LED 控制器"""
    payload = {"command": command}
    payload.update(data)

    response = requests.post(
        f"{API_BASE}/command",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    return response.json()

# 範例使用
send_command("power", {"state": True})
send_command("effect", {"effect": "rainbow"})
send_command("brightness", {"brightness": 75})
send_command("color", {"color": "blue"})

# 取得狀態
status = requests.get(f"{API_BASE}/status").json()
print(status)
```

### Home Assistant 整合

在 Home Assistant 中控制 LED:

```yaml
light:
  - platform: http
    name: "WS2812 LED"
    resource: "http://<ESP_IP>/api"
    # 需要額外配置
```

## 故障排除

### 問題: 網頁介面打不開

**檢查清單**
1. ✓ 確認 ESP32 已連接到 WiFi
2. ✓ 確認 IP 位址正確（查看路由器或 ESPHome 日誌）
3. ✓ 確認防火牆允許 HTTP (port 80)
4. ✓ 嘗試使用 mDNS: `http://ws2812-led-effects.local`

### 問題: LED 不響應命令

**檢查清單**
1. ✓ 確認電源已接通
2. ✓ 點選 [開啟] 按鈕啟動 LED
3. ✓ 檢查 LED 燈條連線
4. ✓ 查看 ESPHome 日誌

### 問題: 效果不符預期

**調整建議**
1. 增加亮度
2. 調整速度
3. 切換效果重試
4. 檢查 LED 數量設定

### 問題: API 返回錯誤

**常見錯誤**

```json
{"error": "Unknown effect: invalid_name"}
```
→ 檢查效果名稱拼寫

```json
{"error": "Unknown color: invalid_color"}
```
→ 使用有效顏色名稱

```json
{"error": "Invalid JSON"}
```
→ 檢查 JSON 格式

## 效能提示

### 省電模式

```
- 降低亮度到 30-50%
- 使用 Pulse 或 Twinkle 效果
- 減少 LED 數量
```

省電 50-70%

### 高效能模式

```
- 最大亮度
- 使用 Strobe 或 Scan 效果
- 高速設定
```

消耗 1.5-2A (30 LED)

### 最佳實踐

1. **定期重啟**: 每週重啟一次 ESP32
2. **避免過熱**: 確保良好的通風環境
3. **穩定電源**: 使用品質良好的 5V 供應器
4. **備份配置**: 定期備份 `secrets.yaml`

## 支援的語言

目前網頁介面支援：
- 繁體中文 (Traditional Chinese)
- 英文 (English) - 代碼中使用

## 最後更新

版本: v1.0.0
日期: 2026-03-08

更新日誌詳見 [README.md](README.md)

---

需要幫助? 查看 [INSTALLATION.md](INSTALLATION.md)
