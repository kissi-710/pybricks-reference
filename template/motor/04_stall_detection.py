"""
SPIKE Prime モーター制御テンプレート: ストール検出
=================================================

「ストール」とは、最大出力でも回せない状態（壁や機構の端に当たった等）です。
- run_until_stalled: ストールするまで回し、止まった角度を返す
- stalled: 現在ストール中かどうかを判定

機構の端（リミット）を見つけて基準にする、といった用途に便利です。
"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Stop, Color
from pybricks.tools import wait, StopWatch

hub = PrimeHub()
motor = Motor(Port.A)

# --- 1. run_until_stalled で端まで回す ---
# duty_limit でトルク（出力）を制限すると、機構に優しく当てられる（%）。
# then で当たった後の挙動を指定（COAST/HOLD など）。
print("端に当たるまでゆっくり回します...")
end_angle = motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=40)
print("ストールした角度:", end_angle, "deg")

# ここを基準（0 度）に設定する
motor.reset_angle(0)
hub.light.on(Color.GREEN)
wait(1000)

# --- 2. 反対側の端も探す ---
print("反対側の端まで回します...")
other_end = motor.run_until_stalled(-200, then=Stop.HOLD, duty_limit=40)
print("反対の端の角度:", other_end, "deg")

# 可動範囲の中央へ移動
center = other_end / 2
motor.run_target(300, center)
print("可動範囲の中央へ移動:", center, "deg")

# --- 3. stalled() でリアルタイムにストール判定 ---
print("モーターを手で押さえてみてください（5 秒間監視）")
motor.run(300)
timer = StopWatch()
while timer.time() < 5000:
    if motor.stalled():
        hub.light.on(Color.RED)
        print("ストール検出！")
    else:
        hub.light.on(Color.GREEN)
    wait(100)

motor.stop()
hub.light.off()
print("ストール検出デモ終了")
