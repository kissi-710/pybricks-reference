"""
SPIKE Prime モーター制御テンプレート: 速度・加速度・トルクの設定
=================================================

モーターの動作特性を control 属性で調整する方法を示します。
- control.limits: 最大速度・加速度・トルクの上限設定
  引数なしで呼ぶと現在値を取得できる

加速度を小さくすると滑らかな立ち上がり、大きくすると俊敏な動きになります。
"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait

hub = PrimeHub()
motor = Motor(Port.A)

# --- 1. 現在の設定を確認 ---
# 戻り値は (最大速度 deg/s, 加速度 deg/s^2, 最大トルク) のタプル
speed, acceleration, torque = motor.control.limits()
print("初期設定 -> 速度:", speed, "加速度:", acceleration, "トルク:", torque)

# --- 2. ゆっくり・滑らかな動き（低加速度）---
motor.control.limits(speed=300, acceleration=300)
print("低加速度で 360 度回転")
motor.run_angle(300, 360)
wait(500)

# --- 3. 俊敏な動き（高加速度）---
motor.control.limits(speed=1000, acceleration=2000)
print("高加速度で 360 度回転")
motor.run_angle(1000, 360)
wait(500)

# --- 4. 加速と減速を別々に設定 ---
# acceleration にタプルを渡すと (加速, 減速) を個別指定できる
motor.control.limits(speed=800, acceleration=(2000, 500))
print("速く加速・ゆっくり減速で 720 度回転")
motor.run_angle(800, 720)

print("設定デモ終了")
