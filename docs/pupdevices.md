# pybricks.pupdevices — Powered Up デバイス

## 概要

`pybricks.pupdevices` モジュールは、LEGO® Powered Up 規格のモーター・センサー・ライト・リモコンなどを制御するクラスを提供します。SPIKE Prime・BOOST・City Hub・Technic Hub などで使用します。

```python
from pybricks.pupdevices import Motor, DCMotor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.pupdevices import Remote, ColorDistanceSensor, InfraredSensor, Light
from pybricks.pupdevices import TiltSensor, ColorLightMatrix, PFMotor
from pybricks.pupdevices import TechnicMoveHub, MarioHub, DuploTrain
```

---

## Motor — 回転センサー付きモーター ⭐

Powered Up 規格のモーター（Medium Linear Motor・Large Motor・XL Motor・Angular Motor 等）を制御します。詳細な API は [motors.md](motors.md) を参照してください。

```python
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop

motor = Motor(Port.A)
motor.run(500)                    # 500 deg/s で連続回転
motor.run_angle(500, 360)         # 360度回転
motor.run_target(500, 0)          # 0度の位置へ移動
motor.hold()                      # 現在位置でホールド
```

詳細: [motors.md](motors.md)

---

## DCMotor — 回転センサーなしモーター

Powered Up 規格のシンプルモーターを制御します。

```python
from pybricks.pupdevices import DCMotor
from pybricks.parameters import Port

motor = DCMotor(Port.A)
motor.dc(70)      # 70% 出力で回転
motor.stop()      # フリーコースト
motor.brake()     # ブレーキ
```

詳細: [motors.md](motors.md)

---

## ColorSensor — SPIKE カラーセンサー ⭐

```python
from pybricks.pupdevices import ColorSensor
from pybricks.parameters import Port, Color

sensor = ColorSensor(Port.B)
```

LEGO® SPIKE カラーセンサー。色・反射光・環境光を検出します。センサー前面に 3 つのライトを内蔵しており、個別に輝度調整が可能です。

### 属性

| 属性 | クラス | 説明 |
|---|---|---|
| `sensor.lights` | `LightArray3` | 3 つのライトを制御 |

### メソッド

#### `color(surface=True) -> Color` ⭐

表面または外光の色を検出します。

| 引数 | 型 | 説明 |
|---|---|---|
| `surface` | bool | `True`: 物体・表面の色を検出。`False`: 画面など外光源の色を検出 |

**戻り値:** `Color.RED`・`Color.GREEN` など（`detectable_colors` で設定したリスト内の最近似色）

#### `hsv(surface=True) -> Color`

フル解像度の HSV 値で色を返します。`color()` と違い、近似化されず精密な値が得られます。

| 引数 | 型 | 説明 |
|---|---|---|
| `surface` | bool | `True`: 物体の色、`False`: 外光の色 |

**戻り値:** `Color(h=..., s=..., v=...)` オブジェクト

#### `ambient() -> int: %`

環境光の強度を測定します。

**戻り値:** 明度（0〜100 %）

#### `reflection() -> int: %`

センサーが照射した光の反射量を測定します。

**戻り値:** 反射率（0〜100 %）

#### `detectable_colors(colors)` / `detectable_colors() -> Collection[Color]`

`color()` で検出する色のリストを設定します。引数なしで現在のリストを返します。

| 引数 | 型 | 説明 |
|---|---|---|
| `colors` | list[Color] | 検出対象の色リスト |

**使用例**

```python
from pybricks.pupdevices import ColorSensor
from pybricks.parameters import Port, Color

sensor = ColorSensor(Port.B)

# 色の検出
c = sensor.color()
if c == Color.RED:
    print("赤！")

# 精密な HSV 値
hsv = sensor.hsv()
print(f"Hue={hsv.h}, Sat={hsv.s}, Val={hsv.v}")

# 検出対象を絞って精度向上
sensor.detectable_colors([Color.RED, Color.BLUE, Color.GREEN, Color.NONE])

# 反射光と環境光
ref = sensor.reflection()   # 0〜100 %
amb = sensor.ambient()      # 0〜100 %

# ライトを個別に制御
sensor.lights.on(100)              # 全ライト全輝度
sensor.lights.on((100, 0, 100))   # 左中右を個別設定
sensor.lights.off()
```

---

## UltrasonicSensor — SPIKE 超音波センサー

```python
from pybricks.pupdevices import UltrasonicSensor
from pybricks.parameters import Port

sensor = UltrasonicSensor(Port.C)
```

超音波で距離を計測します。センサー前面に 4 つのライトを内蔵しています。

### 属性

| 属性 | クラス | 説明 |
|---|---|---|
| `sensor.lights` | `LightArray4` | 4 つのライトを制御 |

### メソッド

#### `distance() -> int: mm` ⭐

物体までの距離を mm 単位で返します。有効な距離が計測できない場合は `2000` を返します。

**戻り値:** 距離（mm）

#### `presence() -> bool`

他の超音波センサーの音波を検出します。

**戻り値:** `True` なら超音波を検出

**使用例**

```python
from pybricks.pupdevices import UltrasonicSensor
from pybricks.parameters import Port

sensor = UltrasonicSensor(Port.C)

dist = sensor.distance()   # mm
if dist < 200:
    print("障害物が近い！")

# ライト制御
sensor.lights.on(50)   # 全ライト 50% 輝度
```

---

## ForceSensor — SPIKE フォースセンサー ⭐

```python
from pybricks.pupdevices import ForceSensor
from pybricks.parameters import Port

sensor = ForceSensor(Port.D)
```

ボタンへの押し込み力を計測します。

### メソッド

#### `force() -> float: N`

センサーに加えられた力を N（ニュートン）で返します（最大約 10 N）。

#### `distance() -> float: mm`

ボタンの押し込み量を mm で返します（最大約 8 mm）。

#### `pressed(force=3) -> bool` ⭐

ボタンが押されているか確認します。

| 引数 | 型 | 説明 |
|---|---|---|
| `force` | Number, N | 「押された」とみなす最小荷重（デフォルト: 3 N） |

**戻り値:** `True` なら押されている

#### `touched() -> bool`

軽い接触を検出します。`pressed()` よりも低い閾値で反応します。

**使用例**

```python
from pybricks.pupdevices import ForceSensor
from pybricks.parameters import Port

sensor = ForceSensor(Port.D)

# 押されるまで待機
while not sensor.pressed():
    pass
print(f"力: {sensor.force():.2f} N")

# 軽いタッチを検出
if sensor.touched():
    print("触れた")
```

---

## ColorDistanceSensor — Powered Up カラー距離センサー

```python
from pybricks.pupdevices import ColorDistanceSensor
from pybricks.parameters import Port

sensor = ColorDistanceSensor(Port.B)
```

色と距離の両方を検出する旧 Powered Up センサーです。

### 属性

| 属性 | クラス |
|---|---|
| `sensor.light` | `ExternalColorLight` |

### メソッド

`ColorSensor` の `color()`・`hsv()`・`ambient()`・`reflection()`・`detectable_colors()` に加え:

#### `distance() -> int: %`

赤外線で相対距離を計測します（0% が最近、100% が最遠）。

**使用例**

```python
from pybricks.pupdevices import ColorDistanceSensor
from pybricks.parameters import Port, Color

sensor = ColorDistanceSensor(Port.B)

c = sensor.color()
d = sensor.distance()   # 0〜100 %
sensor.light.on(Color.BLUE)  # センサーのライトを青に
```

---

## TiltSensor — Powered Up チルトセンサー

```python
from pybricks.pupdevices import TiltSensor
from pybricks.parameters import Port

sensor = TiltSensor(Port.A)
```

### メソッド

#### `tilt() -> Tuple[int, int]: deg`

水平面に対するピッチ角とロール角を返します。

---

## InfraredSensor — Powered Up 赤外線センサー

```python
from pybricks.pupdevices import InfraredSensor
from pybricks.parameters import Port

sensor = InfraredSensor(Port.A)
```

### メソッド

#### `reflection() -> int: %`

赤外線反射量を返します（0〜100 %）。

#### `distance() -> int: %`

赤外線で相対距離を返します（0% 最近、100% 最遠）。

#### `count() -> int`

センサーの前を通過した物体の数を返します。

---

## Light — Powered Up ライト

```python
from pybricks.pupdevices import Light
from pybricks.parameters import Port

light = Light(Port.A)
```

### メソッド

#### `on(brightness=100)`

指定輝度でライトを点灯します（0〜100 %）。

#### `off()`

ライトを消灯します。

---

## ColorLightMatrix — SPIKE 3×3 カラーライトマトリックス

```python
from pybricks.pupdevices import ColorLightMatrix
from pybricks.parameters import Port, Color

matrix = ColorLightMatrix(Port.A)
```

3×3 のカラー LED マトリックスです。

### メソッド

#### `on(colors)`

ライトを点灯します。

| 引数 | 型 | 説明 |
|---|---|---|
| `colors` | Color または list[Color] | 1色で全 9 灯、リストで各灯個別指定 |

#### `off()`

すべてのライトを消灯します。

**使用例**

```python
matrix.on(Color.RED)             # 全て赤
matrix.on([Color.RED, Color.GREEN, Color.BLUE, ...])  # 9個個別
matrix.off()
```

---

## Remote — Powered Up リモコン

```python
from pybricks.pupdevices import Remote

remote = Remote()
```

LEGO® Powered Up Bluetooth リモコンに接続して、ボタン入力とライト制御を行います。

### コンストラクタ

```python
Remote(name=None, timeout=10000, connect=True)
```

| 引数 | 型 | 説明 |
|---|---|---|
| `name` | str | 接続するリモコンの Bluetooth 名（`None` で最初に見つかったものに接続） |
| `timeout` | Number, ms | タイムアウト時間 |
| `connect` | bool | `False` でスキップ（後で `connect()` を呼ぶ） |

### 属性

| 属性 | クラス | 説明 |
|---|---|---|
| `remote.buttons` | `Keypad` | LEFT_PLUS / LEFT_MINUS / LEFT / CENTER / RIGHT / RIGHT_PLUS / RIGHT_MINUS |
| `remote.light` | `ExternalColorLight` | リモコンのライト |
| `remote.address` | str | Bluetooth アドレス |

**使用例**

```python
from pybricks.pupdevices import Remote, Motor
from pybricks.parameters import Port, Button, Color

motor = Motor(Port.A)
remote = Remote()

remote.light.on(Color.GREEN)

while True:
    pressed = remote.buttons.pressed()
    if Button.RIGHT_PLUS in pressed:
        motor.run(500)
    elif Button.RIGHT_MINUS in pressed:
        motor.run(-500)
    else:
        motor.hold()
```

---

## PFMotor — Power Functions モーター制御

```python
from pybricks.pupdevices import PFMotor, ColorDistanceSensor
from pybricks.parameters import Port, Color, Direction

sensor = ColorDistanceSensor(Port.B)
motor = PFMotor(sensor, channel=1, color=Color.BLUE)
```

`ColorDistanceSensor` の赤外線機能を使って Power Functions モーターを制御します。

### コンストラクタ

```python
PFMotor(sensor, channel, color, positive_direction=Direction.CLOCKWISE)
```

| 引数 | 型 | 説明 |
|---|---|---|
| `sensor` | ColorDistanceSensor | センサーオブジェクト |
| `channel` | int | レシーバーのチャンネル（1〜4） |
| `color` | Color | レシーバーの色マーカー（`Color.BLUE` または `Color.RED`） |

---

## TechnicMoveHub — Technic Move Hub（外部接続）

```python
from pybricks.pupdevices import TechnicMoveHub

hub = TechnicMoveHub()
```

LEGO® Technic Move Hub（設定42176 等）に別のハブから Bluetooth で接続して操作します。

### メソッド

#### `drive(speed, steering)`

モーターを制御します。

| 引数 | 型 | 説明 |
|---|---|---|
| `speed` | int, % | 速度（-100〜100） |
| `steering` | int, % | ステアリング（-100〜100）。正が右、±97 でクランプ |

---

## DuploTrain — Duplo トレインハブ（外部接続）

```python
from pybricks.pupdevices import DuploTrain

train = DuploTrain()
```

LEGO® Duplo トレインハブに別のハブから Bluetooth で接続して操作します。

### メソッド

#### `drive(speed)` — モーターを制御

#### `headlights(color)` — ヘッドライトの色を設定

#### `sound(sound)` — サウンドを再生

`"brake"` / `"depart"` / `"water"` / `"horn"` / `"steam"` から選択

#### `speed() -> int: %` — 速度を取得

#### `color() -> Color` — カラーセンサーの値を取得

---

## MarioHub — Mario ハブ（外部接続）

```python
from pybricks.pupdevices import MarioHub

mario = MarioHub()
```

LEGO® Super Mario フィギュアに別のハブから Bluetooth で接続して、カラーセンサーを読み取ります。

### メソッド

#### `color() -> Color` — 検出された色を取得

#### `hsv() -> Color` — HSV 値で色を取得
