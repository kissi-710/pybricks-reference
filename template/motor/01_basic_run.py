"""
SPIKE Prime モーター制御テンプレート: 基本動作
=================================================

モーターの基本的な回し方を示します。
- run: 指定速度で連続回転
- run_time: 指定時間だけ回転
- run_angle: 指定角度だけ回転
- run_target: 目標角度まで回転

速度の単位は deg/s（度/秒）、角度の単位は deg（度）です。
"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.tools import wait

hub = PrimeHub()

# ポート A のモーターを初期化
# positive_direction で正の速度のときの回転方向を指定できる
motor = Motor(Port.A, positive_direction=Direction.CLOCKWISE)

# --- 1. run: 指定速度で回し続ける ---
# 次のコマンドが来るまで回り続ける（ノンブロッキング）
motor.run(500)   # 500 deg/s で回転
wait(2000)       # 2 秒間そのまま

# --- 2. run_time: 指定時間だけ回す ---
# wait=True（デフォルト）なので完了までこの行で待つ
motor.run_time(500, 2000)   # 500 deg/s で 2 秒間回転

# --- 3. run_angle: 指定角度だけ回す ---
motor.run_angle(360, 360)   # 360 deg/s で 360 度（1 回転）
motor.run_angle(360, -180)  # 負の角度で逆方向に 180 度

# --- 4. run_target: 目標角度まで回す ---
# 現在の角度に関わらず、指定した絶対角度まで最短方向で回る
# speed は正負どちらでもよい（方向は自動で決まる）
motor.run_target(500, 90)   # 角度 90 度の位置へ
motor.run_target(500, 0)    # 角度 0 度の位置へ戻る

print("基本動作デモ終了")
