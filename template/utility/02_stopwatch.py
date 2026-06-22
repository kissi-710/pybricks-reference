"""
SPIKE Prime ユーティリティテンプレート: StopWatch（ストップウォッチ）
=================================================

StopWatch は経過時間を計測するためのクラスです。
- time():   経過時間 (ms) を取得
- pause():  一時停止
- resume(): 再開
- reset():  0 に戻す

「一定時間だけ処理を続ける」「反応速度を測る」などに使えます。
"""

from pybricks.hubs import PrimeHub
from pybricks.parameters import Button, Color
from pybricks.tools import wait, StopWatch

hub = PrimeHub()

# StopWatch を作るとすぐに計測が始まる
timer = StopWatch()

# --- 1. 一定時間だけループを回す ---
# time() が 3000ms に達するまでライトを点滅
print("3 秒間点滅します")
while timer.time() < 3000:
    hub.light.on(Color.GREEN)
    wait(100)
    hub.light.off()
    wait(100)

# --- 2. リセットして反応速度ゲーム ---
print("CENTER ボタンを押す準備...")
wait(1000)
print("今だ！ CENTER ボタンを押せ！")

timer.reset()   # 計測を 0 に戻す
while Button.CENTER not in hub.buttons.pressed():
    wait(1)

reaction = timer.time()
print("反応速度:", reaction, "ms")

# --- 3. pause / resume の例 ---
timer.reset()
wait(1000)
timer.pause()           # ここで計測を止める
print("一時停止時:", timer.time(), "ms")  # 約 1000
wait(2000)              # この 2 秒はカウントされない
timer.resume()          # 計測を再開
wait(1000)
print("再開後:", timer.time(), "ms")      # 約 2000

print("StopWatch デモ終了")
