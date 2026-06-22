"""
SPIKE Prime ハブ操作テンプレート: IMU（慣性計測ユニット）
=================================================

ハブ内蔵の IMU（ジャイロ＋加速度計）を使う方法を示します。
- どの面が上を向いているかの判定 (up)
- 傾き（ピッチ・ロール）の取得 (tilt)
- 方位角（ヘディング）の取得とリセット (heading)
- 加速度・角速度の取得
- 静止判定 (stationary)

※ IMU はハブごとに個体差があります。起動直後は数秒静止させて
   キャリブレーションを完了させると精度が上がります。
"""

from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis, Color
from pybricks.tools import wait, StopWatch

hub = PrimeHub()

# --- 1. IMU が使用可能になるまで待つ ---
print("ハブを水平に置いて静止させてください...")
while not hub.imu.ready():
    wait(100)
print("IMU 準備完了")

# ヘディング（方位角）を 0 にリセット
hub.imu.reset_heading(0)

# --- 2. メインループ: 各種値を表示 ---
print("ハブを傾けたり回したりしてみてください（CENTER は使わず10秒間表示）")

timer = StopWatch()

while timer.time() < 10000:
    # どの面が上か（Side.TOP / BOTTOM / FRONT / BACK / LEFT / RIGHT）
    up_side = hub.imu.up()

    # 傾き: (ピッチ, ロール) を度で取得
    pitch, roll = hub.imu.tilt()

    # 方位角: 起動時/リセット時を 0 とした累積回転角（時計回りが正）
    heading = hub.imu.heading()

    # Z 軸まわりの角速度 (deg/s)
    turn_rate = hub.imu.angular_velocity(Axis.Z)

    # 静止しているか
    still = hub.imu.stationary()

    print(
        "上面:", up_side,
        "| ピッチ:", pitch, "ロール:", roll,
        "| 方位:", round(heading),
        "| 角速度:", round(turn_rate),
        "| 静止:", still,
    )

    # 上面の向きでライト色を変える
    hub.light.on(Color.GREEN if still else Color.RED)

    wait(200)

hub.light.off()
print("IMU デモ終了")
