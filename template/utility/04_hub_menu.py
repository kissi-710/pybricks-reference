"""
SPIKE Prime ユーティリティテンプレート: hub_menu（プログラム選択メニュー）
=================================================

hub_menu はハブのディスプレイにメニューを表示し、ボタンで項目を選ばせる
便利関数です。1 つのハブに複数の動作を入れておき、起動時に選ぶ、といった
使い方ができます。

【操作】
  LEFT / RIGHT ボタンで項目を切り替え、CENTER ボタンで決定。
  hub_menu は選ばれた記号（数字や文字）を返す。
"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Color
from pybricks.tools import hub_menu, wait

hub = PrimeHub()
motor = Motor(Port.A)

# --- メニューを表示して選択させる ---
# 引数に並べた記号が選択肢になる（数字・1 文字の文字列）
print("LEFT/RIGHT で選択、CENTER で決定")
selected = hub_menu("1", "2", "3", "A")

print("選択されました:", selected)

# --- 選択結果に応じて処理を分岐 ---
if selected == "1":
    # プログラム 1: ゆっくり 1 回転
    hub.light.on(Color.GREEN)
    motor.run_angle(200, 360)

elif selected == "2":
    # プログラム 2: 速く 2 回転
    hub.light.on(Color.BLUE)
    motor.run_angle(800, 720)

elif selected == "3":
    # プログラム 3: 往復運動
    hub.light.on(Color.YELLOW)
    for i in range(3):
        motor.run_angle(500, 180)
        motor.run_angle(500, -180)

elif selected == "A":
    # プログラム A: 音を鳴らす
    hub.light.on(Color.MAGENTA)
    hub.speaker.play_notes(["C4/4", "E4/4", "G4/4", "C5/2"])

hub.light.off()
print("hub_menu デモ終了")
