"""
SPIKE Prime 走行ロボットテンプレート: ジャイロを使った精密走行
=================================================

DriveBase は内蔵 IMU（ジャイロ）を使うと、より正確にまっすぐ走り、
正確な角度で旋回できます。タイヤの空転や床の摩擦差による誤差を
ジャイロが補正してくれます。

- use_gyro(True): ジャイロ補正を有効化
- straight / turn は同じように使えるが、精度が向上する

※ プログラム開始時はロボットを数秒静止させ、ジャイロを安定させると
   さらに精度が上がります。
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

# --- 1. ジャイロを安定させる ---
print("ロボットを静止させてジャイロを安定させています...")
while not hub.imu.ready():
    wait(100)
print("準備完了")

# --- 2. ジャイロ補正を有効化 ---
robot.use_gyro(True)

# 走行量と角度をリセット（ジャイロの角度も 0 になる）
robot.reset()

# --- 3. 正確な三角形（正三角形=外角120度）を描く ---
print("ジャイロ補正で正三角形を描きます")
for i in range(3):
    robot.straight(300)    # まっすぐ 300mm（ジャイロで直進補正）
    robot.turn(120)        # 正確に 120 度旋回

# --- 4. 絶対角度での旋回 ---
# absolute=True にすると「開始時を基準とした絶対方位」へ向く
print("絶対方位 0 度（スタート方向）に向き直します")
robot.turn(0, absolute=True)

print("最終的なジャイロ角度:", hub.imu.heading(), "deg")
print("ジャイロ走行デモ終了")
