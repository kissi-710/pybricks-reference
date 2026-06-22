"""
SPIKE Prime ハブ操作テンプレート: システム制御と永続ストレージ
=================================================

ハブのシステム機能を使う方法を示します。
- ハブ情報の取得 (info)
- 停止ボタンの変更 (set_stop_button)
- 永続ストレージへのデータ保存・読み出し (storage)
- ハブのシャットダウン (shutdown)

※ storage に保存したデータは、ハブを正常に電源オフしたときフラッシュに
   書き込まれ、次回プログラム実行時にも残ります（電池を抜いても保持）。
"""

from pybricks.hubs import PrimeHub
from pybricks.parameters import Button, Color
from pybricks.tools import wait

hub = PrimeHub()

# --- 1. ハブ情報を取得 ---
info = hub.system.info()
print("ハブ名:", info["name"])
print("リセット理由:", info["reset_reason"])
print("BLE 接続:", info["host_connected_ble"])
print("USB 接続:", info["host_connected_usb"])

# --- 2. 停止ボタンの変更 ---
# 通常は CENTER ボタンでプログラムが停止する。
# ここでは BLUETOOTH ボタンを停止ボタンにし、CENTER を自由に使えるようにする。
hub.system.set_stop_button(Button.BLUETOOTH)
print("停止ボタンを BLUETOOTH に変更しました")

# --- 3. 永続ストレージ: 起動回数をカウント ---
# offset 0 から 4 バイト読み込み（前回までの起動回数）
try:
    data = hub.system.storage(0, read=4)
    count = int.from_bytes(data, "little")
except Exception:
    count = 0

count += 1
print("このプログラムの累計起動回数:", count)

# 更新した起動回数を書き戻す
hub.system.storage(0, write=count.to_bytes(4, "little"))

# 起動回数をディスプレイに表示（99 まで）
hub.display.number(min(count, 99))
hub.light.on(Color.CYAN)

# --- 4. CENTER ボタンでシャットダウン ---
print("CENTER ボタンを押すとシャットダウンします（停止は BLUETOOTH）")
while Button.CENTER not in hub.buttons.pressed():
    wait(50)

print("シャットダウンします...")
wait(500)
hub.system.shutdown()
