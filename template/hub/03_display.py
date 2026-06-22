"""
SPIKE Prime ハブ操作テンプレート: 5×5 ライトマトリックス・ディスプレイ
=================================================

ハブ前面の 5×5 LED ディスプレイを制御する方法を示します。
- 数字 / 文字 / テキストの表示
- 組み込みアイコンの表示
- 個別ピクセルの点灯
- アイコンのアニメーション
"""

from pybricks.hubs import PrimeHub
from pybricks.parameters import Icon
from pybricks.tools import wait

hub = PrimeHub()

# --- 1. 数字を表示（-99〜99）---
hub.display.number(42)
wait(1500)

# --- 2. 1 文字を表示 ---
hub.display.char("A")
wait(1500)

# --- 3. テキストをスクロール表示 ---
# on: 各文字の表示時間(ms)、off: 文字間の消灯時間(ms)
hub.display.text("HELLO", on=500, off=50)
wait(500)

# --- 4. 組み込みアイコンを表示 ---
hub.display.icon(Icon.HEART)
wait(1000)
hub.display.icon(Icon.HAPPY)
wait(1000)

# アイコンは明るさをスケーリングできる（0.0〜1.0 倍）
hub.display.icon(Icon.HEART * 0.3)  # 30% の明るさ
wait(1000)

# アイコンは加算で合成できる（両目を表示）
hub.display.icon(Icon.EYE_LEFT + Icon.EYE_RIGHT)
wait(1000)

# --- 5. 個別ピクセルの点灯 ---
# pixel(行, 列, 明るさ%) 行・列は 0 始まり（左上が 0,0）
hub.display.off()
for i in range(5):
    hub.display.pixel(i, i, brightness=100)  # 対角線を点灯
    wait(200)
wait(1000)

# --- 6. アイコンのアニメーション ---
# Icon のリストを interval ミリ秒ごとに切り替えて繰り返す
hub.display.animate(
    [Icon.CLOCKWISE, Icon.CLOCKWISE * 0.5, Icon.COUNTERCLOCKWISE],
    interval=300,
)
wait(3000)

# 後始末
hub.display.off()
print("ディスプレイデモ終了")
