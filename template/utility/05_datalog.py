"""
SPIKE Prime ユーティリティテンプレート: DataLog（データ記録）
=================================================

DataLog はセンサーやモーターの値を時系列で記録するためのクラスです。
- DataLog(*見出し) で列の名前を指定して作成
- log(値1, 値2, ...) で 1 行分のデータを記録

SPIKE Prime ではファイル保存の代わりに、記録した内容が
プログラム実行中の出力ウィンドウ（コンソール）に表示されます。
モーターの角度・速度などを記録して、後でグラフ化する用途に便利です。
"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait, StopWatch, DataLog

hub = PrimeHub()
motor = Motor(Port.A)

# --- 1. ログを作成（列の見出しを指定）---
# time, angle, speed という 3 列のデータを記録する
log = DataLog("time", "angle", "speed", name="motor_data")

# --- 2. モーターを動かしながらデータを記録 ---
print("モーターを動かしながらデータを記録します")
motor.reset_angle(0)
timer = StopWatch()

# モーターを回し始める
motor.run(500)

# 3 秒間、50ms ごとに記録
while timer.time() < 3000:
    log.log(timer.time(), motor.angle(), motor.speed())
    wait(50)

motor.stop()

# --- 3. 加速・減速の様子も記録 ---
print("加減速の様子を記録します")
timer.reset()
while timer.time() < 2000:
    # 時間に応じて速度を変える（だんだん速く）
    target = timer.time() // 4
    motor.run(target)
    log.log(timer.time(), motor.angle(), motor.speed())
    wait(50)

motor.stop()
print("DataLog デモ終了（記録内容は出力ウィンドウを確認）")
