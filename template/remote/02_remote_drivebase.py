"""
SPIKE Prime リモコンテンプレート: リモコンでロボット操縦
=================================================

LEGO Powered Up リモコンで走行ロボット（DriveBase）を操縦します。
- 左側ボタン（+/-）で前進・後退
- 右側ボタン（+/-）で左右旋回
- 前進と旋回を組み合わせてカーブも可能

ラジコンのような操作感でロボットを動かせます。
"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Port, Direction, Button, Color
from pybricks.robotics import DriveBase
from pybricks.tools import wait

hub = PrimeHub()

left_motor = Motor(Port.A, positive_direction=Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.B, positive_direction=Direction.CLOCKWISE)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=112)

# --- リモコンに接続 ---
print("リモコンを探しています...")
remote = Remote()
remote.light.on(Color.GREEN)
print("接続完了。左+/-=前後, 右+/-=旋回, CENTER=終了")

# 速度・旋回率の基準値
DRIVE_SPEED = 200   # mm/s
TURN_RATE = 100     # deg/s

while True:
    pressed = remote.buttons.pressed()

    # 前進・後退の速度を決める
    speed = 0
    if Button.LEFT_PLUS in pressed:
        speed = DRIVE_SPEED
    elif Button.LEFT_MINUS in pressed:
        speed = -DRIVE_SPEED

    # 旋回率を決める
    turn = 0
    if Button.RIGHT_PLUS in pressed:
        turn = TURN_RATE
    elif Button.RIGHT_MINUS in pressed:
        turn = -TURN_RATE

    # 速度と旋回を組み合わせて走行（両方 0 ならその場で停止）
    robot.drive(speed, turn)

    # CENTER で終了
    if Button.CENTER in pressed:
        break

    wait(20)

robot.stop()
remote.light.off()
print("リモコン操縦デモ終了")
