"""
SPIKE Prime 走行ロボットテンプレート: ライントレース（P制御）
=================================================

カラーセンサーの反射光を使って、黒線と白地の境界に沿って走る基本的な
ライントレースです。比例制御（P制御）でなめらかに線をたどります。

【仕組み】
  境界線上では反射光が「黒(低)と白(高)の中間値」になります。
  この目標値（threshold）と現在の反射光の差（error）に比例して
  旋回率を変えることで、線からズレたら戻るように補正します。

【調整ポイント】
  - threshold: (白の反射光 + 黒の反射光) / 2 で求める
  - GAIN:      大きいほど反応が強い（大きすぎると蛇行する）
"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Port, Direction, Button
from pybricks.robotics import DriveBase
from pybricks.tools import wait

hub = PrimeHub()

left_motor = Motor(Port.A, positive_direction=Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.B, positive_direction=Direction.CLOCKWISE)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=112)

# ライン検出用カラーセンサー（ポート C）
line_sensor = ColorSensor(Port.C)

# --- パラメータ設定 ---
# threshold は「白の反射光」と「黒の反射光」の中間値。
# 例: 白=80%, 黒=10% なら threshold = 45
WHITE = 80
BLACK = 10
threshold = (WHITE + BLACK) // 2

DRIVE_SPEED = 100   # 前進速度 (mm/s)
GAIN = 1.2          # 比例ゲイン（補正の強さ）

print("CENTER ボタンでライントレース開始")
while Button.CENTER not in hub.buttons.pressed():
    wait(10)

print("ライントレース中... BLUETOOTH ボタンで終了")
while True:
    # 反射光を測定
    reflection = line_sensor.reflection()

    # 目標値とのズレ（誤差）を計算
    error = reflection - threshold

    # 誤差に比例した旋回率を与える（P制御）
    turn_rate = GAIN * error

    # 前進しながら補正
    robot.drive(DRIVE_SPEED, turn_rate)

    # 終了判定
    if Button.BLUETOOTH in hub.buttons.pressed():
        break

    wait(10)

robot.stop()
print("ライントレースデモ終了")
