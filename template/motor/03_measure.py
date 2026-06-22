"""
SPIKE Prime モーター制御テンプレート: 状態の取得
=================================================

モーターの現在の状態を読み取る方法を示します。
- angle: 現在の回転角度 (deg)
- speed: 現在の速度 (deg/s)
- load:  推定負荷トルク (mNm)
- reset_angle: 角度カウンターのリセット

モーターを手で回しながら値の変化を観察できます。
"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Color
from pybricks.tools import wait, StopWatch

hub = PrimeHub()
motor = Motor(Port.A)

# --- 1. 角度カウンターをリセット ---
# 現在位置を 0 度の基準にする
motor.reset_angle(0)
print("角度を 0 にリセットしました")

# --- 2. 一定時間、状態を読み取り続ける ---
print("モーターを手で回してみてください（10 秒間）")
timer = StopWatch()

while timer.time() < 10000:
    angle = motor.angle()         # 現在の角度
    speed = motor.speed()         # 現在の速度
    load = motor.load()           # 推定負荷トルク

    print("角度:", angle, "deg | 速度:", speed, "deg/s | 負荷:", load, "mNm")

    # 回転方向でライト色を変える
    if speed > 20:
        hub.light.on(Color.GREEN)
    elif speed < -20:
        hub.light.on(Color.RED)
    else:
        hub.light.on(Color.BLUE)

    wait(200)

hub.light.off()
print("計測デモ終了")
