"""
SPIKE Prime 走行ロボットテンプレート: 基本走行
=================================================

2 つのモーターで動く差動駆動ロボット（DriveBase）の基本操作です。
- straight: 指定距離だけ直進 (mm)
- turn:     その場で指定角度だけ旋回 (deg)
- arc:      円弧を描いて走行
- settings: 速度・加速度の設定

【座標の規約】
  前進・正の距離 = 前   / 後退・負の距離 = 後ろ
  正の角度 = 右回り(時計回り) / 負の角度 = 左回り

【重要】wheel_diameter（車輪の直径）と axle_track（左右車輪の間隔）は
実際のロボットに合わせて mm 単位で正確に測って設定してください。
"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import wait

hub = PrimeHub()

# 左右のモーターを初期化（左右で取り付け向きが逆になるのが一般的）
left_motor = Motor(Port.A, positive_direction=Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.B, positive_direction=Direction.CLOCKWISE)

# DriveBase を作成
#   wheel_diameter: 車輪の直径 (mm) ... 標準の SPIKE ホイールは 56mm
#   axle_track:     左右車輪の接地点間の距離 (mm)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=112)

# --- 1. 走行速度・加速度を設定（任意）---
# settings(直進速度, 直進加速度, 旋回速度, 旋回加速度)
robot.settings(straight_speed=200, straight_acceleration=400,
               turn_rate=150, turn_acceleration=300)

# --- 2. 四角形を描いて走る ---
print("四角形を描いて走行します")
for i in range(4):
    robot.straight(300)   # 300mm 前進
    robot.turn(90)        # 右へ 90 度旋回

wait(500)

# --- 3. 後退と左旋回 ---
robot.straight(-200)      # 200mm 後退
robot.turn(-90)           # 左へ 90 度旋回

wait(500)

# --- 4. 円弧を描く ---
# arc(半径 mm, angle=角度 deg) 正の半径で右、負の半径で左に曲がる
print("円弧を描きます")
robot.arc(radius=150, angle=180)   # 半径 150mm で右に半円
robot.arc(radius=-150, angle=180)  # 半径 150mm で左に半円

print("基本走行デモ終了")
