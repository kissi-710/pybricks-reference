"""
SPIKE Prime ハブ操作テンプレート: ボタン入力
=================================================

ハブ本体のボタン（LEFT / CENTER / RIGHT / BLUETOOTH）の状態を読み取る方法を示します。
- ボタンが押されているかの判定
- 特定ボタンが押されるまで待機
- 複数ボタンの同時押し判定
"""

from pybricks.hubs import PrimeHub
from pybricks.parameters import Button, Color
from pybricks.tools import wait

# ハブを初期化
hub = PrimeHub()

# --- 1. ボタンが押されるまで待つ ---
hub.display.char("?")
print("CENTER ボタンを押してください")

# pressed() は現在押されているボタンの集合 (set) を返す
while Button.CENTER not in hub.buttons.pressed():
    wait(10)  # CPU を占有しないよう少し待つ

print("CENTER が押されました！")
hub.light.on(Color.GREEN)
wait(500)

# --- 2. 押されたボタンに応じて処理を分岐 ---
print("LEFT / RIGHT / CENTER を押すと色が変わります（BLUETOOTH で終了）")

while True:
    pressed = hub.buttons.pressed()

    if Button.LEFT in pressed:
        hub.light.on(Color.RED)
        hub.display.char("L")
    elif Button.RIGHT in pressed:
        hub.light.on(Color.BLUE)
        hub.display.char("R")
    elif Button.CENTER in pressed:
        hub.light.on(Color.YELLOW)
        hub.display.char("C")

    # --- 3. 複数ボタンの同時押し判定 ---
    # LEFT と RIGHT を同時に押したらアニメ表示
    if {Button.LEFT, Button.RIGHT}.issubset(pressed):
        hub.display.char("X")
        hub.light.on(Color.MAGENTA)

    # BLUETOOTH ボタンでループを抜ける
    if Button.BLUETOOTH in pressed:
        break

    wait(10)

hub.light.off()
hub.display.off()
print("終了しました")
