"""
SPIKE Prime センサーテンプレート: 超音波距離センサー
=================================================

SPIKE 超音波センサーで距離を測る方法を示します。
- distance: 物体までの距離 (mm)。測定不能時は 2000 を返す
- presence: 他の超音波センサーの存在を検出
- lights:   センサー前面の 4 つのライト制御（"目" の表現に使える）

距離に応じてハブのライト色を変え、近づくと警告音を鳴らします。
"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import UltrasonicSensor
from pybricks.parameters import Port, Color
from pybricks.tools import wait, StopWatch

hub = PrimeHub()

# ポート D に超音波センサーを接続
sensor = UltrasonicSensor(Port.D)

print("センサーの前で手を近づけたり離したりしてください（15 秒間）")
timer = StopWatch()

while timer.time() < 15000:
    distance = sensor.distance()   # mm 単位
    print("距離:", distance, "mm")

    # --- 距離に応じてライト色と警告音を変える ---
    if distance < 100:
        hub.light.on(Color.RED)
        hub.speaker.beep(frequency=880, duration=50)  # 近い: 高音で警告
    elif distance < 300:
        hub.light.on(Color.YELLOW)
    else:
        hub.light.on(Color.GREEN)

    # --- センサーの 4 灯で距離をバー表示 ---
    # 近いほど多くのライトを点ける
    if distance < 100:
        sensor.lights.on((100, 100, 100, 100))
    elif distance < 300:
        sensor.lights.on((100, 100, 0, 0))
    else:
        sensor.lights.on((100, 0, 0, 0))

    wait(100)

sensor.lights.off()
hub.light.off()
print("超音波センサーデモ終了")
