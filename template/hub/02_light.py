"""
SPIKE Prime ハブ操作テンプレート: ステータスライト
=================================================

ハブ中央のステータスライト（ボタン周りの LED）を制御する方法を示します。
- 単色点灯 / 消灯
- 点滅 (blink)
- 色のアニメーション (animate)
- カスタム色 (HSV) の使用
"""

from pybricks.hubs import PrimeHub
from pybricks.parameters import Color
from pybricks.tools import wait

hub = PrimeHub()

# --- 1. 単色で点灯 ---
hub.light.on(Color.RED)
wait(1000)
hub.light.on(Color.GREEN)
wait(1000)
hub.light.on(Color.BLUE)
wait(1000)

# --- 2. 消灯 ---
hub.light.off()
wait(500)

# --- 3. カスタム色（HSV: 色相・彩度・明度）---
# 明度を落とした淡いオレンジ
hub.light.on(Color(h=30, s=100, v=40))
wait(1000)

# --- 4. 点滅 (blink) ---
# [点灯ms, 消灯ms, 点灯ms, 消灯ms, ...] のパターンで点滅
# バックグラウンドで点滅し続け、次の行はすぐ実行される
hub.light.blink(Color.YELLOW, [500, 500])
wait(3000)  # 3 秒間点滅させる

# --- 5. 色のアニメーション (animate) ---
# 色のリストを interval ミリ秒ごとに順番に表示し、繰り返す
hub.light.animate(
    [Color.RED, Color.ORANGE, Color.YELLOW, Color.GREEN, Color.BLUE, Color.VIOLET],
    interval=200,
)
wait(4000)  # 4 秒間アニメーション

# 後始末
hub.light.off()
print("ライトデモ終了")
