# pybricks.hubs — ハブクラス

## 概要

`pybricks.hubs` モジュールは、各 LEGO® ハブのトップレベルクラスを提供します。ハブのボタン・ライト・ディスプレイ・スピーカー・IMU・バッテリー・システム制御にアクセスします。

```python
from pybricks.hubs import PrimeHub       # SPIKE Prime / Inventor Hub
from pybricks.hubs import TechnicHub    # Technic Hub
from pybricks.hubs import EssentialHub  # SPIKE Essential Hub
from pybricks.hubs import CityHub       # City Hub
from pybricks.hubs import MoveHub       # BOOST Move Hub
from pybricks.hubs import EV3Brick      # MINDSTORMS EV3
```

---

## ハブ対応表

| ハブ | クラス | IMU | ディスプレイ | スピーカー | 充電器 |
|---|---|---|---|---|---|
| SPIKE Prime Hub | `PrimeHub` | ✅（IMU） | ✅（5×5 LED） | ✅ | ✅ |
| MINDSTORMS Inventor Hub | `InventorHub` | ✅（IMU） | ✅（5×5 LED） | ✅ | ✅ |
| SPIKE Essential Hub | `EssentialHub` | ✅（IMU） | ❌ | ❌ | ✅ |
| Technic Hub | `TechnicHub` | ✅（IMU） | ❌ | ❌ | ❌ |
| BOOST Move Hub | `MoveHub` | ✅（加速度計のみ） | ❌ | ❌ | ❌ |
| City Hub | `CityHub` | ❌ | ❌ | ❌ | ❌ |
| MINDSTORMS EV3 | `EV3Brick` | ❌ | ✅（スクリーン） | ✅ | ❌ |

---

## 共通の属性

ほとんどのハブは以下の属性を持ちます。詳細は各属性のドキュメントを参照してください。

| 属性 | クラス | 説明 |
|---|---|---|
| `hub.buttons` | `Keypad` | ボタンの状態取得 |
| `hub.light` | `ColorLight` | ステータスライトの制御 |
| `hub.battery` | `Battery` | バッテリー状態の取得 |
| `hub.imu` | `IMU` または `SimpleAccelerometer` | 傾き・加速度・ジャイロ |
| `hub.system` | `System` | シャットダウン・ストレージ管理 |
| `hub.display` | `LightMatrix` | LED ディスプレイ（一部ハブのみ） |
| `hub.speaker` | `Speaker` | スピーカー（一部ハブのみ） |
| `hub.charger` | `Charger` | 充電状態（一部ハブのみ） |

---

## PrimeHub — SPIKE Prime Hub

```python
from pybricks.hubs import PrimeHub

hub = PrimeHub()
```

LEGO® SPIKE Prime Hub のクラスです。`InventorHub`（MINDSTORMS Inventor Hub）はこのクラスを継承しており、同一の API を使用できます。

### コンストラクタ

```python
PrimeHub(top_side=Axis.Z, front_side=Axis.X)
```

| 引数 | 型 | 説明 |
|---|---|---|
| `top_side` | Axis | 上面を通る軸（デフォルト: `Axis.Z`） |
| `front_side` | Axis | 前面を通る軸（デフォルト: `Axis.X`） |

### 属性

| 属性 | クラス | 説明 |
|---|---|---|
| `hub.buttons` | `Keypad` | LEFT / RIGHT / CENTER / BLUETOOTH ボタン |
| `hub.light` | `ColorLight` | ステータスライト |
| `hub.display` | `LightMatrix` | 5×5 LED ディスプレイ |
| `hub.speaker` | `Speaker` | スピーカー |
| `hub.imu` | `IMU` | ジャイロ・加速度計 |
| `hub.battery` | `Battery` | バッテリー状態 |
| `hub.charger` | `Charger` | USB 充電状態 |
| `hub.system` | `System` | システム制御 |

### 使用例

```python
from pybricks.hubs import PrimeHub
from pybricks.parameters import Color, Button, Icon

hub = PrimeHub()

# ライト制御
hub.light.on(Color.GREEN)
hub.light.off()
hub.light.blink(Color.RED, [500, 500])

# ディスプレイ
hub.display.number(42)
hub.display.text("Hi")
hub.display.icon(Icon.HAPPY)
hub.display.off()

# スピーカー
hub.speaker.beep(frequency=440, duration=200)
hub.speaker.play_notes(["C4/4", "E4/4", "G4/4"])

# ボタン
pressed = hub.buttons.pressed()
if Button.LEFT in pressed:
    print("左ボタンが押されている")

# バッテリー
print(hub.battery.voltage())   # mV
print(hub.battery.current())   # mA

# IMU（ジャイロ）
print(hub.imu.heading())       # ヘディング角度
print(hub.imu.tilt())          # ピッチ・ロール

# システム
hub.system.shutdown()          # シャットダウン
```

---

## TechnicHub — Technic Hub

```python
from pybricks.hubs import TechnicHub

hub = TechnicHub()
```

LEGO® Technic Hub のクラスです。IMU（ジャイロ・加速度計）を搭載しています。

### コンストラクタ

```python
TechnicHub(top_side=Axis.Z, front_side=Axis.X)
```

### 属性

| 属性 | クラス |
|---|---|
| `hub.buttons` | `Keypad`（CENTER のみ） |
| `hub.light` | `ColorLight` |
| `hub.imu` | `IMU` |
| `hub.battery` | `Battery` |
| `hub.system` | `System` |

---

## EssentialHub — SPIKE Essential Hub

```python
from pybricks.hubs import EssentialHub

hub = EssentialHub()
```

LEGO® SPIKE Essential Hub のクラスです。

### コンストラクタ

```python
EssentialHub(top_side=Axis.Z, front_side=Axis.X)
```

### 属性

| 属性 | クラス |
|---|---|
| `hub.buttons` | `Keypad`（CENTER のみ） |
| `hub.light` | `ColorLight` |
| `hub.imu` | `IMU` |
| `hub.battery` | `Battery` |
| `hub.charger` | `Charger` |
| `hub.system` | `System` |

---

## CityHub — City Hub

```python
from pybricks.hubs import CityHub

hub = CityHub()
```

LEGO® City Hub（スマートハブ）のクラスです。IMU は搭載していません。

### コンストラクタ

```python
CityHub()
```

### 属性

| 属性 | クラス |
|---|---|
| `hub.buttons` | `Keypad`（CENTER のみ） |
| `hub.light` | `ColorLight` |
| `hub.battery` | `Battery` |
| `hub.system` | `System` |

---

## MoveHub — BOOST Move Hub

```python
from pybricks.hubs import MoveHub

hub = MoveHub()
```

LEGO® BOOST Move Hub のクラスです。加速度計（SimpleAccelerometer）のみ搭載（フルジャイロなし）。

### コンストラクタ

```python
MoveHub(top_side=Axis.Z, front_side=Axis.X)
```

### 属性

| 属性 | クラス |
|---|---|
| `hub.buttons` | `Keypad`（CENTER のみ） |
| `hub.light` | `ColorLight` |
| `hub.imu` | `SimpleAccelerometer` |
| `hub.battery` | `Battery` |
| `hub.system` | `System` |

---

## EV3Brick — MINDSTORMS EV3

```python
from pybricks.hubs import EV3Brick

ev3 = EV3Brick()
```

LEGO® MINDSTORMS® EV3 のクラスです。スクリーン・スピーカーを搭載していますが、IMU はありません。

### 属性

| 属性 | クラス | 説明 |
|---|---|---|
| `ev3.buttons` | `Keypad` | LEFT / RIGHT / CENTER / UP / DOWN ボタン |
| `ev3.screen` | `Image` | EV3 のスクリーン（ev3dev 固有） |
| `ev3.speaker` | `Speaker` | スピーカー |
| `ev3.light` | `ColorLight` | ステータスライト |
| `ev3.battery` | `Battery` | バッテリー状態 |

---

## 共通クラス詳細

### Keypad.pressed() -> Set[Button]

現在押されているボタンのセットを返します。

**使用例**

```python
from pybricks.parameters import Button

buttons = hub.buttons.pressed()
if Button.CENTER in buttons:
    print("中央ボタンが押されている")

# 複数ボタンの同時押し
if {Button.LEFT, Button.RIGHT}.issubset(buttons):
    print("左と右を同時押し")
```

---

### ColorLight — ステータスライト

#### `on(color)`

指定色でライトを点灯します。

| 引数 | 型 | 説明 |
|---|---|---|
| `color` | Color | 色 |

#### `off()`

ライトを消灯します。

#### `blink(color, durations)`

指定色でライトを点滅させます。プログラムが実行中でもバックグラウンドで点滅し続けます。

| 引数 | 型 | 説明 |
|---|---|---|
| `color` | Color | 色 |
| `durations` | list | `[点灯時間1, 消灯時間1, 点灯時間2, ...]` のリスト（ms） |

#### `animate(colors, interval)`

色のリストをアニメーションとして繰り返し表示します。

| 引数 | 型 | 説明 |
|---|---|---|
| `colors` | list[Color] | 表示する色のリスト |
| `interval` | Number, ms | 各色の表示時間 |

**使用例**

```python
from pybricks.parameters import Color

hub.light.on(Color.BLUE)
hub.light.blink(Color.RED, [500, 200, 500, 1000])
hub.light.animate([Color.RED, Color.GREEN, Color.BLUE], 300)
```

---

### LightMatrix — 5×5 LED ディスプレイ

#### `number(number)`

-99〜99 の数値を表示します。

#### `char(char)`

1文字を表示します（英字、記号）。

#### `text(text, on=500, off=50)`

テキストを1文字ずつスクロール表示します。

#### `icon(icon)`

`Matrix` または `Icon` のアイコンを表示します。

#### `pixel(row, column, brightness=100)`

指定のピクセルを点灯します（0 始まり）。

#### `off()`

すべてのピクセルを消灯します。

#### `orientation(up)`

ディスプレイの向きを設定します（`Side.TOP` / `LEFT` / `RIGHT` / `BOTTOM`）。

#### `animate(matrices, interval)`

`Matrix` のリストをアニメーションとして繰り返し表示します。

**使用例**

```python
from pybricks.parameters import Icon

hub.display.number(7)
hub.display.char("A")
hub.display.text("Hello", on=500, off=50)
hub.display.icon(Icon.HEART)
hub.display.pixel(2, 2, brightness=50)  # 中央ピクセルを50%輝度で
hub.display.off()
```

---

### Speaker — スピーカー

#### `volume(volume)` / `volume() -> int`

音量を設定または取得します。

| 引数 | 型 | 説明 |
|---|---|---|
| `volume` | Number, % | 音量（0〜100） |

#### `beep(frequency=500, duration=100)`

ビープ音を鳴らします。

| 引数 | 型 | 説明 |
|---|---|---|
| `frequency` | Number, Hz | 周波数（64〜24000 Hz） |
| `duration` | Number, ms | 時間。負の値で無限再生 |

#### `play_notes(notes, tempo=120)`

音符のリストを演奏します。

| 引数 | 型 | 説明 |
|---|---|---|
| `notes` | list[str] | 音符リスト（例: `["C4/4", "D4/4", "E4/2"]`） |
| `tempo` | int, BPM | テンポ（拍/分） |

**音符フォーマット:** `<音名><オクターブ>/<長さ>`（例: `"C4/4"` = 4分音符のC4）

**使用例**

```python
hub.speaker.volume(70)
hub.speaker.beep(frequency=880, duration=500)
hub.speaker.play_notes(["C4/4", "E4/4", "G4/4", "C5/2"])
```

---

### Battery

#### `voltage() -> int: mV`

バッテリー電圧を返します（ミリボルト）。

#### `current() -> int: mA`

バッテリー電流を返します（ミリアンペア）。

---

### Charger（USB 充電器）

#### `connected() -> bool`

USB 充電器が接続されているか確認します。

#### `status() -> int`

充電状態を返します（0: 充電なし、1: 充電中、2: 完了、3: 異常）。

#### `current() -> int: mA`

充電電流を返します。

---

### IMU — ジャイロ・加速度計

全機能搭載の IMU（慣性計測ユニット）です。`TechnicHub`・`EssentialHub`・`PrimeHub` で使用できます。

#### `heading() -> float: deg` ⭐よく使う

ロボットのヘディング（方位）角度を返します。起動時が 0 で、時計回りが正。360度を超えても巻き戻しません。

#### `tilt(calibrated=True) -> Tuple[int, int]`

ピッチ角とロール角を返します。

#### `acceleration(axis=None, calibrated=True)`

加速度を返します。軸を指定すると float、指定なしでベクトルを返します。

#### `angular_velocity(axis=None, calibrated=True)`

角速度を返します（deg/s）。

#### `rotation(axis, calibrated=True) -> float: deg`

指定軸周りの積算回転量を返します。

#### `orientation() -> Matrix`

3×3 の回転行列として3次元姿勢を返します。

#### `up(calibrated=True) -> Side`

現在上を向いている面を返します（`Side.TOP` など）。

#### `ready() -> bool`

IMU が校正済みで使用可能か確認します。

#### `stationary() -> bool`

1秒以上静止しているか確認します。

#### `reset_heading(angle)`

ヘディング角度をリセットします。DriveBase が動いている場合は先に停止が必要です。

#### `settings(...)` / `settings()`

`angular_velocity_threshold`・`acceleration_threshold`・`heading_correction` などのキャリブレーション設定を行います。

**使用例**

```python
from pybricks.hubs import TechnicHub
from pybricks.parameters import Axis

hub = TechnicHub()

# 静止待ち
while not hub.imu.stationary():
    pass

# ヘディング（方位角）
heading = hub.imu.heading()

# 加速度
ax = hub.imu.acceleration(Axis.X)
a_vec = hub.imu.acceleration()   # ベクトル

# IMU が正確な値を返せる状態か
if hub.imu.ready():
    print("IMU 準備完了")

# ヘディングをリセット
hub.imu.reset_heading(0)
```

---

### System — システム制御

#### `shutdown()`

プログラムを停止してハブをシャットダウンします。

#### `set_stop_button(button)`

プログラムを停止するボタンを変更します。`None` で停止ボタンを無効化できます。

#### `storage(offset, read=)` / `storage(offset, write=)`

フラッシュメモリへのバイナリデータの読み書きを行います。次回起動時にも保持されます。

#### `reset_storage()`

ユーザー設定とプログラムをすべてリセットします。

#### `info() -> dict`

ハブ情報（名前、リセット理由、接続状態、プログラム開始方法など）を辞書で返します。

**使用例**

```python
info = hub.system.info()
print(info["name"])            # ハブの名前
print(info["host_connected_ble"])  # BLE 接続状態

# データを保存
hub.system.storage(0, write=b"\x01\x02\x03")

# データを読み込み
data = hub.system.storage(0, read=3)
```
