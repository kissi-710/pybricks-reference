# pybricks.robotics — ロボティクス

## 概要

`pybricks.robotics` モジュールは、2輪差動ロボットや舵取りモーターを持つ車型ロボットを高レベルに制御するクラスを提供します。モーターの個別制御と違い、「何ミリメートル進む」「何度旋回する」という直感的なコマンドでロボットを動かせます。

```python
from pybricks.robotics import DriveBase, Car
```

---

## DriveBase — 差動2輪ロボット ⭐

```python
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase

hub = PrimeHub()
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)

robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=112)
```

2つのモーターで駆動する差動2輪ロボット用クラス。ロボットの寸法を指定するだけで、直進・旋回・円弧走行が可能になります。

**座標の規約:**
- 正の距離・速度 = 前進、負 = 後退
- 正の角度・旋回速度 = 右旋回（時計回り）、負 = 左旋回

### コンストラクタ

```python
DriveBase(left_motor, right_motor, wheel_diameter, axle_track)
```

| 引数 | 型 | 説明 |
|---|---|---|
| `left_motor` | Motor | 左輪のモーターオブジェクト |
| `right_motor` | Motor | 右輪のモーターオブジェクト |
| `wheel_diameter` | Number, mm | 車輪の直径 |
| `axle_track` | Number, mm | 両輪の接地点間の距離（車軸長） |

### 属性

| 属性 | クラス | 説明 |
|---|---|---|
| `robot.distance_control` | `Control` | 直進の PID 設定 |
| `robot.heading_control` | `Control` | 旋回の PID 設定 |

---

## よく使う操作クイックリファレンス

```python
robot.straight(300)              # 300 mm 直進
robot.straight(-100)             # 100 mm 後退
robot.turn(90)                   # 右へ 90 度旋回
robot.turn(-45)                  # 左へ 45 度旋回
robot.arc(radius=200, angle=90)  # 半径 200 mm で右へ 90 度弧走行
robot.drive(200, 30)             # 速度 200 mm/s、旋回率 30 deg/s で連続走行
robot.stop()                     # 停止（フリーコースト）
robot.brake()                    # ブレーキ停止
robot.hold()                     # 位置保持

# 状態取得
print(robot.distance())          # 走行距離 (mm)
print(robot.angle())             # 旋回角度 (deg)
d, v, a, w = robot.state()      # 距離, 速度, 角度, 角速度

# ジャイロ補正
robot.use_gyro(True)             # ジャイロを使って正確に走行
```

---

## メソッド詳細

### `straight(distance, then=Stop.HOLD, wait=True)`

指定距離だけ直進して停止します。

| 引数 | 型 | 説明 |
|---|---|---|
| `distance` | Number, mm | 走行距離（正: 前進、負: 後退） |
| `then` | Stop | 停止後の動作（デフォルト: `Stop.HOLD`） |
| `wait` | bool | `True` で完了まで待機 |

### `turn(angle, then=Stop.HOLD, wait=True, absolute=False)`

その場で旋回して停止します。

| 引数 | 型 | 説明 |
|---|---|---|
| `angle` | Number, deg | 旋回角度（正: 右、負: 左） |
| `then` | Stop | 停止後の動作 |
| `wait` | bool | `True` で完了まで待機 |
| `absolute` | bool | `False`: 現在向きからの相対角度。`True`: 絶対方位角 |

### `arc(radius, angle=None, distance=None, then=Stop.HOLD, wait=True)`

円弧走行します。`angle` または `distance` のどちらか一方を指定してください。

| 引数 | 型 | 説明 |
|---|---|---|
| `radius` | Number, mm | 円弧の半径（正: 右旋回、負: 左旋回） |
| `angle` | Number, deg | 円弧に沿って走行する角度（`distance` と排他） |
| `distance` | Number, mm | 円弧に沿って走行する距離（`angle` と排他） |
| `then` | Stop | 停止後の動作 |
| `wait` | bool | `True` で完了まで待機 |

**例外:** `angle` と `distance` を両方指定すると `ValueError`。半径 0 は不可（代わりに `turn()` を使用）。

### `drive(speed, turn_rate)`

連続走行します。新しいコマンドが来るまで走り続けます。

| 引数 | 型 | 説明 |
|---|---|---|
| `speed` | Number, mm/s | 走行速度（正: 前進、負: 後退） |
| `turn_rate` | Number, deg/s | 旋回速度（正: 右、負: 左） |

### `stop()`

モーターを自由回転させて停止します。

### `brake()`

受動的にブレーキをかけて停止します。

### `hold()`

現在位置で停止し、PID 制御で保持します。

### `distance() -> int: mm`

前回リセット以降の走行距離を返します。

### `angle() -> float: deg`

前回リセット以降の旋回角度を返します。ジャイロ使用時はジャイロ値を返します。

### `state() -> Tuple[int, int, int, int]`

ロボットの状態をタプルで返します。

**戻り値:** `(distance, speed, angle, turn_rate)` のタプル

### `reset(distance=0, angle=0)`

走行距離と方位角をリセットします。`use_gyro(True)` の場合、ジャイロも指定値にリセットされます。このメソッドは `stop()` も呼び出します。

| 引数 | 型 | 説明 |
|---|---|---|
| `distance` | Number, mm | リセット後の距離値（デフォルト: 0） |
| `angle` | Number, deg | リセット後の方位角（デフォルト: 0） |

### `settings(straight_speed, straight_acceleration, turn_rate, turn_acceleration)` / `settings() -> Tuple`

走行速度と加速度を設定します。引数なしで現在値を返します。

| 引数 | 型 | 説明 |
|---|---|---|
| `straight_speed` | Number, mm/s | 直進速度（`straight()` の速度） |
| `straight_acceleration` | Number, mm/s² | 直進加速度（タプルで加速・減速を個別設定可） |
| `turn_rate` | Number, deg/s | 旋回速度（`turn()` の角速度） |
| `turn_acceleration` | Number, deg/s² | 旋回加速度 |

### `done() -> bool`

実行中のコマンドが完了したか確認します。

### `stalled() -> bool`

ロボットがストールしているか確認します。

### `move_by(dx, dy, then=Stop.HOLD)`

X-Y 座標系上の移動量を指定して走行します。まず必要な向きに旋回し、その後直進します。

| 引数 | 型 | 説明 |
|---|---|---|
| `dx` | Number, mm | プログラム開始時の前進方向が X 軸の正 |
| `dy` | Number, mm | X 軸の左 90° が Y 軸の正 |
| `then` | Stop | 停止後の動作 |

### `use_gyro(use_gyro)`

ジャイロセンサーを使った精密走行のオン・オフを切り替えます。

| 引数 | 型 | 説明 |
|---|---|---|
| `use_gyro` | bool | `True`: ジャイロ使用、`False`: モーターエンコーダのみ使用 |

---

## 使用例（総合）

```python
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Stop
from pybricks.robotics import DriveBase

hub = PrimeHub()
left = Motor(Port.A)
right = Motor(Port.B)
robot = DriveBase(left, right, wheel_diameter=56, axle_track=112)

# ジャイロ補正を有効化
robot.use_gyro(True)

# 速度設定
robot.settings(straight_speed=200, straight_acceleration=400, turn_rate=180, turn_acceleration=360)

# 走行パターン
robot.straight(500)               # 50 cm 直進
robot.turn(90)                    # 右 90 度旋回
robot.straight(300)               # 30 cm 直進
robot.arc(radius=150, angle=-90)  # 半径 15 cm で左弧走行

# 連続走行（ライントレース等）
robot.drive(150, 0)
while True:
    ref = color_sensor.reflection()
    if ref < 30:
        robot.drive(100, 30)   # 右へ補正
    else:
        robot.drive(100, -30)  # 左へ補正

# 非同期走行
from pybricks.tools import multitask, run_task

async def main():
    await robot.straight(500)
    await robot.turn(90)
    await robot.arc(radius=150, angle=90)

run_task(main())
```

---

## Car — 舵取りモーター付き車型ロボット

```python
from pybricks.robotics import Car
from pybricks.pupdevices import Motor
from pybricks.parameters import Port

steer = Motor(Port.A)
drive = Motor(Port.B)

car = Car(steer_motor=steer, drive_motors=drive)
```

1つのステアリングモーターと1つ以上の駆動モーターを持つ車型ロボット用クラスです。初期化時にステアリングモーターが自動的に中心位置を検出します。

### コンストラクタ

```python
Car(steer_motor, drive_motors, torque_limit=100)
```

| 引数 | 型 | 説明 |
|---|---|---|
| `steer_motor` | Motor | 前輪を操舵するモーター |
| `drive_motors` | Motor または Tuple[Motor, ...] | 駆動モーター（複数の場合はタプル） |
| `torque_limit` | Number, % | ステアリングの限界点を検出するためのトルク上限 |

### メソッド

#### `steer(percentage)`

前輪を指定量ステアリングします。

| 引数 | 型 | 説明 |
|---|---|---|
| `percentage` | Number, % | ステアリング量（100%: 最大右、-100%: 最大左、0%: 直進） |

#### `drive_power(power)`

パワー制御で走行します。リモコン操作のような即時応答に適しています。10% 以下はブレーキの代わりにコーストします。

| 引数 | 型 | 説明 |
|---|---|---|
| `power` | Number, % | 走行出力（正: 前進、負: 後退） |

#### `drive_speed(speed)`

速度制御で走行します。PID 制御で速度を保ちながら加速・減速します。

| 引数 | 型 | 説明 |
|---|---|---|
| `speed` | Number, deg/s | 駆動モーターの角速度 |

**使用例**

```python
from pybricks.robotics import Car
from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Port, Button

steer = Motor(Port.A)
drive = Motor(Port.B)
car = Car(steer_motor=steer, drive_motors=drive)
remote = Remote()

while True:
    pressed = remote.buttons.pressed()
    
    # ステアリング
    if Button.LEFT in pressed:
        car.steer(-50)
    elif Button.RIGHT in pressed:
        car.steer(50)
    else:
        car.steer(0)
    
    # 走行
    if Button.RIGHT_PLUS in pressed:
        car.drive_power(80)
    elif Button.RIGHT_MINUS in pressed:
        car.drive_power(-80)
    else:
        car.drive_power(0)
```
