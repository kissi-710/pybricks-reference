"""
SPIKE Prime センサーテンプレート: フォース（力）センサー
=================================================

SPIKE フォースセンサーで押す力を測る方法を示します。
- force:    加えられた力 (N、最大約 10N)
- distance: ボタンの押し込み量 (mm、最大約 8mm)
- pressed:  指定の力以上で押されているか（しきい値指定可）
- touched:  わずかに触れているか（force より敏感）

押す強さに応じて表示やビープ音を変えるデジタル楽器風のデモです。
"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import ForceSensor
from pybricks.parameters import Port, Color
from pybricks.tools import wait, StopWatch

hub = PrimeHub()

# ポート E にフォースセンサーを接続
sensor = ForceSensor(Port.E)

print("センサーを押してみてください（15 秒間）")
timer = StopWatch()

while timer.time() < 15000:
    # --- 1. 軽い接触の検出 ---
    if sensor.touched():
        force = sensor.force()         # 力 (N)
        distance = sensor.distance()   # 押し込み量 (mm)

        print("力:", round(force, 2), "N | 押し込み:", round(distance, 2), "mm")

        # --- 2. 押す強さでフィードバックを変える ---
        if sensor.pressed(force=5):
            # 強く押した（5N 以上）
            hub.light.on(Color.RED)
            hub.display.char("!")
            # 力に応じて音程を変える（200〜2000Hz 程度）
            freq = 200 + int(force * 180)
            hub.speaker.beep(frequency=freq, duration=50)
        elif sensor.pressed():
            # 軽く押した（デフォルト 3N 以上）
            hub.light.on(Color.YELLOW)
            hub.display.char("o")
        else:
            # 触れているだけ
            hub.light.on(Color.GREEN)
            hub.display.char(".")
    else:
        # 触れていない
        hub.light.off()
        hub.display.off()

    wait(50)

hub.light.off()
hub.display.off()
print("フォースセンサーデモ終了")
