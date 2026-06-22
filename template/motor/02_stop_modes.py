"""
SPIKE Prime モーター制御テンプレート: 停止方法
=================================================

モーターの止め方には複数の種類があります。用途に応じて使い分けます。
- stop  : 電源を切って自由回転（フリーコースト）。摩擦で自然に止まる
- brake : 受動的にブレーキ。外力に少し抵抗する
- hold  : PID 制御で現在角度を保持し続ける（最も強く位置を維持）

また、run_xxx 系コマンドの then 引数で「動作後の停止方法」を指定できます。
"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait

hub = PrimeHub()
motor = Motor(Port.A)

# --- 1. stop（フリーコースト）---
motor.run(500)
wait(1000)
motor.stop()       # 電源オフ、惰性で止まる
wait(1500)

# --- 2. brake（ブレーキ）---
motor.run(500)
wait(1000)
motor.brake()      # 受動ブレーキ。手で回すと軽い抵抗
wait(1500)

# --- 3. hold（ホールド）---
motor.run(500)
wait(1000)
motor.hold()       # 現在角度を積極的に維持。手で回しても戻ろうとする
wait(1500)
motor.stop()

# --- 4. then 引数で動作後の停止方法を指定 ---
# 目標角度まで回ったあとの挙動を変える
motor.run_angle(500, 360, then=Stop.HOLD)    # 回り終わったら保持
wait(500)
motor.run_angle(500, 360, then=Stop.COAST)   # 回り終わったら自由回転
wait(500)
motor.run_angle(500, 360, then=Stop.BRAKE)   # 回り終わったらブレーキ

print("停止方法デモ終了")
