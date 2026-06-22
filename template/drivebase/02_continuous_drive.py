"""
SPIKE Prime 走行ロボットテンプレート: 連続走行とボタン操作
=================================================

drive() を使った連続走行の方法を示します。
- drive(speed, turn_rate): 指定の速度と旋回率で走り続ける（ノンブロッキング）
  speed:     直進速度 (mm/s)  正=前進 / 負=後退
  turn_rate: 旋回率 (deg/s)   正=右 / 負=左
- stop / brake / hold: 停止
- distance / angle: 走行量の取得

ハブのボタンで前進・後退・左右旋回を操作します。
"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Button
from pybricks.robotics import DriveBase
from pybricks.tools import wait

hub = PrimeHub()

left_motor = Motor(Port.A, positive_direction=Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.B, positive_direction=Direction.CLOCKWISE)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=112)

print("ボタンで操縦: 左/右=旋回, BLUETOOTH=終了")
print("（このサンプルでは CENTER=前進, LEFT/RIGHT=旋回）")

# 走行量カウンターをリセット
robot.reset()

while True:
    pressed = hub.buttons.pressed()

    if Button.CENTER in pressed:
        robot.drive(200, 0)       # 前進
    elif Button.LEFT in pressed:
        robot.drive(100, -90)     # 左へカーブ
    elif Button.RIGHT in pressed:
        robot.drive(100, 90)      # 右へカーブ
    else:
        robot.stop()              # ボタンを離したら停止（フリーコースト）

    # 現在の走行距離・角度を表示
    print("距離:", robot.distance(), "mm | 角度:", robot.angle(), "deg")

    # 終了
    if Button.BLUETOOTH in pressed:
        break

    wait(50)

robot.stop()
print("連続走行デモ終了")
