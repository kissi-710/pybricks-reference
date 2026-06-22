# Pybricks APIリファレンス

pybricks ライブラリの APIリファレンスです。LEGO® ハブ・モーター・センサーをプログラムで制御するためのすべてのクラス・関数・定数を網羅しています。

---

## モジュール一覧

| モジュール | 説明 | ドキュメント |
|---|---|---|
| `pybricks.parameters` | 定数・列挙型（Color, Port, Stop, Direction, Button, Side, Icon, Axis） | [parameters.md](parameters.md) |
| `pybricks.tools` | ユーティリティ（wait, StopWatch, DataLog, Matrix, multitask 等） | [tools.md](tools.md) |
| `pybricks.hubs` | ハブクラス（EV3Brick, PrimeHub, TechnicHub 等） | [hubs.md](hubs.md) |
| `pybricks.pupdevices` | Powered Up デバイス（Motor, ColorSensor, UltrasonicSensor 等） | [pupdevices.md](pupdevices.md) |
| `pybricks.ev3devices` | EV3 デバイス（Motor, TouchSensor, GyroSensor 等） | [ev3devices.md](ev3devices.md) |
| `pybricks.nxtdevices` | NXT デバイス（TouchSensor, LightSensor 等） | [nxtdevices.md](nxtdevices.md) |
| `pybricks.robotics` | ロボティクス（DriveBase, Car） | [robotics.md](robotics.md) |
| `pybricks.iodevices` | I/O デバイス（PUPDevice, UARTDevice, XboxController 等） | [iodevices.md](iodevices.md) |
| `pybricks.messaging` | メッセージング・通信（BLERadio, Mailbox 等） | [messaging.md](messaging.md) |
| `pybricks._common` | 共通クラス（Motor, Control, IMU 等の基底クラス） | [motors.md](motors.md) |

---

## よく使う機能クイックリファレンス

### モーターを動かす

```python
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop

motor = Motor(Port.A)

motor.run(500)                            # 500 deg/s で連続回転
motor.run_time(500, 2000)                 # 2秒間回転
motor.run_angle(500, 360)                 # 360度回転
motor.run_target(500, 90)                 # 角度90度まで回転
motor.run_until_stalled(500)             # 停止するまで回転
motor.hold()                             # 現在位置でホールド
motor.stop()                             # 自由に回転（フリーコースト）
motor.brake()                            # ブレーキ停止
```

### センサーを読む

```python
from pybricks.pupdevices import ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Port, Color

color = ColorSensor(Port.B)
ultrasonic = UltrasonicSensor(Port.C)
force = ForceSensor(Port.D)

detected_color = color.color()           # Color.RED など
hsv_value = color.hsv()                  # Color(h=0, s=100, v=100)
ambient = color.ambient()                # 0〜100 %
reflection = color.reflection()          # 0〜100 %

distance = ultrasonic.distance()         # mm 単位

force_n = force.force()                  # N 単位
is_pressed = force.pressed()             # True / False
```

### ハブを操作する

```python
from pybricks.hubs import PrimeHub
from pybricks.parameters import Color, Button

hub = PrimeHub()

hub.light.on(Color.GREEN)                # ライトを緑に
hub.light.off()                          # ライトを消す

hub.speaker.beep(frequency=440, duration=200)  # 440 Hz で 200ms ビープ

hub.display.number(42)                   # 数字を表示
hub.display.text("Hi")                   # テキストを表示

buttons = hub.buttons.pressed()          # 押されているボタンのセット
voltage = hub.battery.voltage()          # バッテリー電圧 (mV)

hub.system.shutdown()                    # シャットダウン
```

### ロボット走行

```python
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase

hub = PrimeHub()
left = Motor(Port.A)
right = Motor(Port.B)
robot = DriveBase(left, right, wheel_diameter=56, axle_track=112)

robot.straight(300)                      # 300 mm 直進
robot.turn(90)                           # 90度右旋回
robot.arc(radius=200, angle=90)          # 半径200 mm で 90度弧走行
robot.drive(200, 0)                      # 速度200 mm/s で直進
robot.stop()                             # 停止
```

### 非同期処理（multitask）

```python
from pybricks.tools import multitask, run_task, wait

async def task1():
    await wait(1000)

async def task2():
    await wait(500)

async def main():
    await multitask(task1(), task2())

run_task(main())
```

---

## ハブ対応表

| ハブ | クラス | 搭載センサー等 |
|---|---|---|
| LEGO® MINDSTORMS® EV3 | `EV3Brick` | ボタン、スクリーン、スピーカー、ライト、バッテリー |
| LEGO® BOOST Move Hub | `MoveHub` | ボタン、ライト、加速度計、バッテリー |
| LEGO® City Hub | `CityHub` | ボタン、ライト、バッテリー |
| LEGO® Technic Hub | `TechnicHub` | ボタン、ライト、IMU、バッテリー |
| LEGO® SPIKE Essential Hub | `EssentialHub` | ボタン、ライト、IMU、充電器、バッテリー |
| LEGO® SPIKE Prime Hub | `PrimeHub` | ボタン、ライト、5×5 LED ディスプレイ、スピーカー、IMU、充電器、バッテリー |
| LEGO® MINDSTORMS® Inventor Hub | `InventorHub` | `PrimeHub` と同等 |
