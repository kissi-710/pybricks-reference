"""
SPIKE Prime センサーテンプレート: カラーセンサー
=================================================

SPIKE カラーセンサーで色や明るさを読み取る方法を示します。
- color:      最も近い色を判定（Color.RED など）
- hsv:        色相・彩度・明度の生の値を取得
- reflection: 反射光の強さ（0〜100%）ライントレースに有用
- ambient:    環境光の強さ（0〜100%）
- detectable_colors: 判定対象の色を絞って精度を上げる
- lights:     センサー前面の 3 つのライト制御
"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import ColorSensor
from pybricks.parameters import Port, Color
from pybricks.tools import wait, StopWatch

hub = PrimeHub()

# ポート C にカラーセンサーを接続
sensor = ColorSensor(Port.C)

# --- 1. 判定する色を絞り込む（任意・精度向上）---
# 使う色だけに限定すると誤検出が減る
sensor.detectable_colors([Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW, Color.WHITE, Color.NONE])

# --- 2. 各種測定値を表示 ---
print("センサーの前に色々なものをかざしてください（10 秒間）")
timer = StopWatch()

while timer.time() < 10000:
    detected = sensor.color()        # 最も近い色
    h, s, v = sensor.hsv()           # 色相・彩度・明度
    reflection = sensor.reflection() # 反射光 (%)
    ambient = sensor.ambient()       # 環境光 (%)

    print(
        "色:", detected,
        "| HSV:", (h, s, v),
        "| 反射:", reflection, "%",
        "| 環境光:", ambient, "%",
    )

    # 検出した色をハブのライトにも反映
    if detected is not None and detected != Color.NONE:
        hub.light.on(detected)
    else:
        hub.light.off()

    wait(300)

# --- 3. センサーのライトを操作する例 ---
# 3 つのライトの明るさを個別に設定（左, 中, 右）
sensor.lights.on((100, 50, 0))
wait(1000)
sensor.lights.off()

hub.light.off()
print("カラーセンサーデモ終了")
