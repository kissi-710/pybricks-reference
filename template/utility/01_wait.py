"""
SPIKE Prime ユーティリティテンプレート: wait（待機）
=================================================

wait(time) はプログラムを指定ミリ秒だけ一時停止する最も基本的な関数です。
- 一定間隔の処理
- 動作と動作の間の「間」を作る
- ループの回しすぎ（CPU 占有）を防ぐ

【注意】wait はその間プログラム全体を止めます。複数の処理を同時に
進めたい場合は utility/03_multitask.py を参照してください。
"""

from pybricks.hubs import PrimeHub
from pybricks.parameters import Color
from pybricks.tools import wait

hub = PrimeHub()

# --- 1. シンプルな待機 ---
print("赤")
hub.light.on(Color.RED)
wait(1000)   # 1 秒（1000 ミリ秒）待つ

print("黄")
hub.light.on(Color.YELLOW)
wait(1000)

print("緑")
hub.light.on(Color.GREEN)
wait(1000)

# --- 2. 一定間隔で繰り返す ---
# ループ内に wait を入れて、決まったテンポで処理する
print("0.5 秒ごとに点滅を 5 回")
for i in range(5):
    hub.light.on(Color.BLUE)
    wait(250)
    hub.light.off()
    wait(250)

# --- 3. カウントダウン ---
for i in range(3, 0, -1):
    hub.display.number(i)
    hub.speaker.beep(frequency=440, duration=100)
    wait(1000)

hub.display.char("!")
hub.speaker.beep(frequency=880, duration=500)

hub.light.off()
hub.display.off()
print("wait デモ終了")
