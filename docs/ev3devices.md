# pybricks.ev3devices — EV3 デバイス

## 概要

`pybricks.ev3devices` モジュールは、LEGO® MINDSTORMS® EV3 専用のモーター・センサーを制御するクラスを提供します。EV3Brick と組み合わせて使用します。

```python
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.ev3devices import InfraredSensor, GyroSensor, UltrasonicSensor
from pybricks.parameters import Port
```

---

## Motor — EV3 モーター

```python
from pybricks.ev3devices import Motor
from pybricks.parameters import Port

motor = Motor(Port.A)
```

EV3 モーター（Medium Motor・Large Motor）を制御します。`pybricks._common.Motor` を継承しており、すべてのモーターメソッドが使用できます。

詳細: [motors.md](motors.md)

**使用例**

```python
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Stop

motor = Motor(Port.A)

motor.run(360)                     # 360 deg/s で回転
motor.run_angle(500, 720)          # 720 度回転（2回転）
motor.run_time(400, 3000, then=Stop.BRAKE)  # 3 秒間回転後ブレーキ
motor.run_until_stalled(100)      # ストールするまで回転

print(motor.angle())              # 現在の角度
print(motor.speed())              # 現在の速度
```

---

## TouchSensor — EV3 タッチセンサー

```python
from pybricks.ev3devices import TouchSensor
from pybricks.parameters import Port

sensor = TouchSensor(Port.S1)
```

ボタンが押されているかどうかを検出するシンプルなセンサーです。

### メソッド

#### `pressed() -> bool`

センサーが押されているか確認します。

**戻り値:** `True` なら押されている、`False` なら離されている

**使用例**

```python
from pybricks.ev3devices import TouchSensor
from pybricks.parameters import Port

sensor = TouchSensor(Port.S1)

# 押されるまで待機
while not sensor.pressed():
    pass

print("タッチされた！")
```

---

## ColorSensor — EV3 カラーセンサー

```python
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port

sensor = ColorSensor(Port.S3)
```

色・反射光・環境光・RGB 値を計測します。

### メソッド

#### `color() -> Color`

表面の色を検出します。

**戻り値:** `Color.BLACK`・`Color.BLUE`・`Color.GREEN`・`Color.YELLOW`・`Color.RED`・`Color.WHITE`・`Color.BROWN`・`Color.NONE` のいずれか

#### `ambient() -> int: %`

環境光の強度を計測します。

**戻り値:** 0〜100 %

#### `reflection() -> int: %`

赤色光の反射量を計測します。

**戻り値:** 0〜100 %

#### `rgb() -> Tuple[int, int, int]`

赤・緑・青の反射量を順番に計測します（各色を交互に照射）。

**戻り値:** `(red, green, blue)` のタプル（各 0〜100 %）

**使用例**

```python
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port, Color

sensor = ColorSensor(Port.S3)

c = sensor.color()
if c == Color.RED:
    print("赤を検出")

ref = sensor.reflection()   # ラインセンサーとして使う
r, g, b = sensor.rgb()      # RGB 値
amb = sensor.ambient()      # 環境光
```

---

## InfraredSensor — EV3 赤外線センサー

```python
from pybricks.ev3devices import InfraredSensor
from pybricks.parameters import Port

sensor = InfraredSensor(Port.S4)
```

赤外線で距離計測、ビーコン追尾、リモコンボタン入力ができます。

### メソッド

#### `distance() -> int: %`

センサーと物体の相対距離を返します（0% が最近、100% が最遠）。

#### `beacon(channel) -> Tuple[Optional[int], Optional[int]]`

EV3 Beacon リモコンとの相対距離と角度を返します。検出できない場合は `(None, None)` を返します。

| 引数 | 型 | 説明 |
|---|---|---|
| `channel` | int | リモコンのチャンネル番号 |

**戻り値:** `(距離 %, 角度 [-75〜75 度])` または `(None, None)`

#### `buttons(channel) -> Set[Button]`

赤外線リモコンで押されているボタンのセットを返します（最大2つ同時）。

| 引数 | 型 | 説明 |
|---|---|---|
| `channel` | int | チャンネル番号 |

#### `keypad() -> List[Button]`

赤外線リモコンの上下ボタンを独立して検出します（ビーコンボタンは検出不可、チャンネル1のみ対応）。

**使用例**

```python
from pybricks.ev3devices import InfraredSensor
from pybricks.parameters import Port, Button

sensor = InfraredSensor(Port.S4)

# 距離計測
dist = sensor.distance()

# ビーコン追尾
dist_pct, angle = sensor.beacon(channel=1)

# リモコンボタン
buttons = sensor.buttons(channel=1)
if Button.LEFT_UP in buttons:
    print("左上ボタン押下")
```

---

## GyroSensor — EV3 ジャイロセンサー

```python
from pybricks.ev3devices import GyroSensor
from pybricks.parameters import Port, Direction

sensor = GyroSensor(Port.S2)
```

角速度と積算回転角度を計測します。

### コンストラクタ

```python
GyroSensor(port, direction=Direction.CLOCKWISE)
```

| 引数 | 型 | 説明 |
|---|---|---|
| `port` | Port | センサーが接続されているポート |
| `direction` | Direction | センサー上面の赤い点を上から見たときの正の回転方向 |

### メソッド

#### `speed() -> int: deg/s`

角速度（回転の速さ）を返します。

#### `angle() -> int: deg`

積算回転角度を返します。

#### `reset_angle(angle)`

積算角度を指定値にリセットします。

| 引数 | 型 | 説明 |
|---|---|---|
| `angle` | Number, deg | リセット後の角度値 |

**使用例**

```python
from pybricks.ev3devices import GyroSensor
from pybricks.parameters import Port

sensor = GyroSensor(Port.S2)
sensor.reset_angle(0)

while True:
    print(sensor.angle(), sensor.speed())
```

---

## UltrasonicSensor — EV3 超音波センサー

```python
from pybricks.ev3devices import UltrasonicSensor
from pybricks.parameters import Port

sensor = UltrasonicSensor(Port.S4)
```

超音波で距離を計測します。

### メソッド

#### `distance(silent=False) -> int: mm`

物体までの距離を mm で返します。

| 引数 | 型 | 説明 |
|---|---|---|
| `silent` | bool | `True` で計測後に送信をオフにする（他のセンサーとの干渉軽減）。頻繁に使うとフリーズの原因になるため注意 |

**戻り値:** 距離（mm）

#### `presence() -> bool`

他の超音波センサーの波を検出します。

**戻り値:** `True` なら検出

**使用例**

```python
from pybricks.ev3devices import UltrasonicSensor
from pybricks.parameters import Port

sensor = UltrasonicSensor(Port.S4)

dist = sensor.distance()
if dist < 150:
    print("障害物 150 mm 以内！")
```
