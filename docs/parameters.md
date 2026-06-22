# pybricks.parameters — 定数・パラメータ

## 概要

`pybricks.parameters` モジュールは、pybricks API 全体で使用する定数・列挙型・型エイリアスを提供します。モーターの方向指定、センサーのポート番号、色の定義など、あらゆる場面で参照する値が含まれています。

```python
from pybricks.parameters import Color, Port, Stop, Direction, Button, Side, Axis, Icon
```

---

## Number

```python
Number = Union[int, float]
```

引数型として登場する `Number` は、`int` と `float` の両方を受け付けます。ただし、内部では整数に丸められる場合があります。

> **注意:** BOOST Move Hub は浮動小数点非対応のため、整数のみ使用可能です。

---

## Axis — 座標軸

```python
from pybricks.parameters import Axis
```

座標系の単位軸ベクトルを表します。`IMU` の軸指定や、ハブの向き設定に使用します。

| 属性 | 説明 |
|---|---|
| `Axis.X` | X 軸方向の単位ベクトル |
| `Axis.Y` | Y 軸方向の単位ベクトル |
| `Axis.Z` | Z 軸方向の単位ベクトル |

**使用例**

```python
from pybricks.hubs import TechnicHub
from pybricks.parameters import Axis

# ハブの上面が Z 軸、前面が X 軸になるよう配置
hub = TechnicHub(top_side=Axis.Z, front_side=Axis.X)

# IMU でX軸方向の加速度を取得
accel = hub.imu.acceleration(Axis.X)
```

---

## Color — 色

```python
from pybricks.parameters import Color
```

光やセンサーで検出する色を表します。HSV（色相・彩度・明度）で表現されます。

### コンストラクタ

```python
Color(h, s=100, v=100)
```

| 引数 | 型 | 説明 |
|---|---|---|
| `h` | Number, deg | 色相（0〜359） |
| `s` | Number, % | 彩度（0〜100） |
| `v` | Number, % | 明度（0〜100） |

### 定義済み定数

| 定数 | HSV 値 | 説明 |
|---|---|---|
| `Color.NONE` | h=0, s=0, v=0 | 色なし（検出できない） |
| `Color.BLACK` | h=0, s=0, v=10 | 黒 |
| `Color.GRAY` | h=0, s=0, v=50 | グレー |
| `Color.WHITE` | h=0, s=0, v=100 | 白 |
| `Color.RED` | h=0, s=100, v=100 | 赤 |
| `Color.ORANGE` | h=30, s=100, v=100 | オレンジ |
| `Color.BROWN` | h=30, s=100, v=50 | 茶 |
| `Color.YELLOW` | h=60, s=100, v=100 | 黄 |
| `Color.GREEN` | h=120, s=100, v=100 | 緑 |
| `Color.CYAN` | h=180, s=100, v=100 | シアン |
| `Color.BLUE` | h=240, s=100, v=100 | 青 |
| `Color.VIOLET` | h=270, s=100, v=100 | 紫 |
| `Color.MAGENTA` | h=300, s=100, v=100 | マゼンタ |

### 属性

| 属性 | 型 | 説明 |
|---|---|---|
| `color.h` | int | 色相（0〜359） |
| `color.s` | int | 彩度（0〜100） |
| `color.v` | int | 明度（0〜100） |

### 演算子

| 演算 | 説明 |
|---|---|
| `color * scale` | 明度をスケーリング（暗くする） |
| `color / scale` | 明度をスケーリング（明るくする） |
| `color >> shift` | 色相をシフト（右回り） |
| `color << shift` | 色相をシフト（左回り） |

**使用例**

```python
from pybricks.parameters import Color

# 定義済み色
c = Color.RED

# カスタム色（HSV で指定）
my_color = Color(h=200, s=80, v=90)

# アンパックで h, s, v を取得
h, s, v = my_color

# 明度を半分にする
dim = Color.GREEN / 2

# 色相を 30 度シフト
shifted = Color.RED >> 30    # オレンジ相当

# センサーで検出した色と比較
from pybricks.pupdevices import ColorSensor
from pybricks.parameters import Port
sensor = ColorSensor(Port.B)
if sensor.color() == Color.RED:
    print("赤を検出！")
```

---

## Port — ポート

```python
from pybricks.parameters import Port
```

ハブ上のモーターやセンサーが接続されるポートを表します。

| 定数 | 説明 |
|---|---|
| `Port.A` | ポート A |
| `Port.B` | ポート B |
| `Port.C` | ポート C |
| `Port.D` | ポート D |
| `Port.E` | ポート E |
| `Port.F` | ポート F |
| `Port.S1` | NXT/EV3 センサーポート 1 |
| `Port.S2` | NXT/EV3 センサーポート 2 |
| `Port.S3` | NXT/EV3 センサーポート 3 |
| `Port.S4` | NXT/EV3 センサーポート 4 |

**使用例**

```python
from pybricks.pupdevices import Motor
from pybricks.parameters import Port

motor = Motor(Port.A)
```

---

## Stop — 停止方法

```python
from pybricks.parameters import Stop
```

モーターが目標に達した後、またはコマンド終了後の動作を指定します。

| 定数 | 説明 |
|---|---|
| `Stop.COAST` | モーターを自由回転させる（摩擦で自然停止） |
| `Stop.COAST_SMART` | 自由回転。次の相対角度コマンドでは、最後の目標角度を新たな開始点として使用（累積誤差を軽減） |
| `Stop.BRAKE` | 受動的にブレーキをかける（外力に対して抵抗） |
| `Stop.HOLD` | PID 制御で現在角度を保持し続ける |
| `Stop.NONE` | 目標到達時に減速しない。次のコマンドがなければそのまま走り続ける |

**使用例**

```python
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Stop

motor = Motor(Port.A)

# 指定角度まで回転後、ホールド
motor.run_angle(500, 360, then=Stop.HOLD)

# 指定角度まで回転後、自由回転
motor.run_angle(500, 360, then=Stop.COAST)
```

---

## Direction — 回転方向

```python
from pybricks.parameters import Direction
```

正の速度・角度に対応するモーターの回転方向を定義します。

| 定数 | 説明 |
|---|---|
| `Direction.CLOCKWISE` | 正の速度値で時計回り（デフォルト） |
| `Direction.COUNTERCLOCKWISE` | 正の速度値で反時計回り |

**使用例**

```python
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction

# 正の速度で反時計回りに回転するモーター
motor = Motor(Port.A, positive_direction=Direction.COUNTERCLOCKWISE)
motor.run(500)   # 反時計回りに 500 deg/s
```

---

## Button — ボタン

```python
from pybricks.parameters import Button
```

ハブやリモコンのボタンを表します。`hub.buttons.pressed()` の戻り値（Set）の要素として使われます。

| 定数 | 説明 |
|---|---|
| `Button.CENTER` | 中央ボタン |
| `Button.LEFT` | 左ボタン |
| `Button.RIGHT` | 右ボタン |
| `Button.UP` | 上ボタン |
| `Button.DOWN` | 下ボタン |
| `Button.LEFT_PLUS` / `Button.LEFT_UP` | 左プラス（リモコン用） |
| `Button.LEFT_MINUS` / `Button.LEFT_DOWN` | 左マイナス（リモコン用） |
| `Button.RIGHT_PLUS` / `Button.RIGHT_UP` | 右プラス（リモコン用） |
| `Button.RIGHT_MINUS` / `Button.RIGHT_DOWN` | 右マイナス（リモコン用） |
| `Button.BLUETOOTH` | Bluetooth ボタン |
| `Button.BEACON` | ビーコンボタン（EV3 IR リモコン） |

**使用例**

```python
from pybricks.hubs import PrimeHub
from pybricks.parameters import Button

hub = PrimeHub()

# 中央ボタンが押されるまで待つ
while Button.CENTER not in hub.buttons.pressed():
    pass

print("押された！")
```

---

## Side — 面

```python
from pybricks.parameters import Side
```

ハブやセンサーの面（方向）を表します。`IMU.up()` の戻り値や `LightMatrix.orientation()` の引数として使います。

| 定数 | 説明 |
|---|---|
| `Side.TOP` | 上面 |
| `Side.BOTTOM` | 下面 |
| `Side.FRONT` | 前面 |
| `Side.BACK` | 背面 |
| `Side.LEFT` | 左面 |
| `Side.RIGHT` | 右面 |

**使用例**

```python
from pybricks.hubs import TechnicHub

hub = TechnicHub()

# 現在上を向いている面を取得
face_up = hub.imu.up()
print(face_up)   # Side.TOP など
```

---

## Icon — アイコン

```python
from pybricks.parameters import Icon
```

5×5 LED ディスプレイに表示できる組み込みアイコンです。各属性は `Matrix` 型の輝度値です。スケーリングや合成も可能です。

| 属性 | 説明 |
|---|---|
| `Icon.UP` | 上矢印 |
| `Icon.DOWN` | 下矢印 |
| `Icon.LEFT` | 左矢印 |
| `Icon.RIGHT` | 右矢印 |
| `Icon.ARROW_UP` | 細い上矢印 |
| `Icon.ARROW_DOWN` | 細い下矢印 |
| `Icon.ARROW_LEFT` | 細い左矢印 |
| `Icon.ARROW_RIGHT` | 細い右矢印 |
| `Icon.ARROW_RIGHT_UP` | 右斜め上矢印 |
| `Icon.ARROW_RIGHT_DOWN` | 右斜め下矢印 |
| `Icon.ARROW_LEFT_UP` | 左斜め上矢印 |
| `Icon.ARROW_LEFT_DOWN` | 左斜め下矢印 |
| `Icon.HAPPY` | 笑顔 |
| `Icon.SAD` | 悲しい顔 |
| `Icon.HEART` | ハート |
| `Icon.PAUSE` | 一時停止 |
| `Icon.FULL` | 全点灯 |
| `Icon.EMPTY` | 全消灯 |
| `Icon.SQUARE` | 四角 |
| `Icon.CIRCLE` | 円 |
| `Icon.TRIANGLE_UP` | 上向き三角 |
| `Icon.TRIANGLE_DOWN` | 下向き三角 |
| `Icon.TRIANGLE_LEFT` | 左向き三角 |
| `Icon.TRIANGLE_RIGHT` | 右向き三角 |
| `Icon.CLOCKWISE` | 時計回り矢印 |
| `Icon.COUNTERCLOCKWISE` | 反時計回り矢印 |
| `Icon.TRUE` | チェックマーク |
| `Icon.FALSE` | バツ印 |
| `Icon.EYE_LEFT` / `Icon.EYE_RIGHT` | 目（左・右） |
| `Icon.EYE_LEFT_BLINK` / `Icon.EYE_RIGHT_BLINK` | まばたき目 |
| `Icon.EYE_LEFT_BROW` / `Icon.EYE_RIGHT_BROW` | 眉毛 |

**使用例**

```python
from pybricks.hubs import PrimeHub
from pybricks.parameters import Icon

hub = PrimeHub()

# アイコンを表示
hub.display.icon(Icon.HAPPY)

# 明度を 50% に落として表示
hub.display.icon(Icon.HAPPY * 0.5)

# アイコンを合成して表示（左目＋右目）
hub.display.icon(Icon.EYE_LEFT + Icon.EYE_RIGHT)
```
