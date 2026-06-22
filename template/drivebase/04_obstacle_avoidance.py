"""
SPIKE Prime 走行ロボットテンプレート: 障害物回避
=================================================

超音波センサーで前方の障害物を検知し、ぶつかる前に回避しながら
走り続けるロボットです。

【動作】
  - 前方が空いていれば前進
  - 一定距離より近くに障害物があれば、いったん停止 → 後退 → 旋回して回避
"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, UltrasonicSensor
from pybricks.parameters import Port, Direction, Button, Color
from pybricks.robotics import DriveBase
from pybricks.tools import wait

hub = PrimeHub()

left_motor = Motor(Port.A, positive_direction=Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.B, positive_direction=Direction.CLOCKWISE)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=112)

# 前方監視用の超音波センサー（ポート D）
eye = UltrasonicSensor(Port.D)

# 障害物とみなす距離 (mm)
SAFE_DISTANCE = 250

print("CENTER ボタンでスタート、BLUETOOTH ボタンで終了")
while Button.CENTER not in hub.buttons.pressed():
    wait(10)

while True:
    distance = eye.distance()

    if distance > SAFE_DISTANCE:
        # 前方クリア: 前進
        hub.light.on(Color.GREEN)
        robot.drive(150, 0)
    else:
        # 障害物発見: 回避行動
        hub.light.on(Color.RED)
        robot.stop()
        wait(200)
        robot.straight(-150)   # 少し後退
        robot.turn(90)         # 右へ 90 度旋回して向きを変える

    if Button.BLUETOOTH in hub.buttons.pressed():
        break

    wait(50)

robot.stop()
hub.light.off()
print("障害物回避デモ終了")
