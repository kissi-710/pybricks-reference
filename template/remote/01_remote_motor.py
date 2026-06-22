"""
SPIKE Prime リモコンテンプレート: リモコンでモーター操作
=================================================

LEGO Powered Up リモコン（ハンドセット）でモーターを操作します。
- Remote() でリモコンに Bluetooth 接続
- remote.buttons.pressed() で押されているボタンを取得
- remote.light で リモコンの LED を制御

【リモコンのボタン】
  左側: LEFT_PLUS / LEFT / LEFT_MINUS
  右側: RIGHT_PLUS / RIGHT / RIGHT_MINUS
  中央: CENTER（緑のボタン）

このサンプルでは右側の +/- ボタンでモーターを正逆回転させます。
"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Port, Button, Color
from pybricks.tools import wait

hub = PrimeHub()
motor = Motor(Port.A)

# --- リモコンに接続 ---
# name=None なら最初に見つかったリモコンに接続する
print("リモコンを探しています... リモコンの緑ボタンを押して電源を入れてください")
remote = Remote()
print("リモコンに接続しました")

# リモコンの LED を青に
remote.light.on(Color.BLUE)

print("右 +/- でモーター回転、CENTER で終了")
while True:
    pressed = remote.buttons.pressed()

    if Button.RIGHT_PLUS in pressed:
        motor.run(500)        # 正回転
    elif Button.RIGHT_MINUS in pressed:
        motor.run(-500)       # 逆回転
    else:
        motor.hold()          # ボタンを離したら現在位置を保持

    # CENTER ボタンで終了
    if Button.CENTER in pressed:
        break

    wait(20)

motor.stop()
remote.light.off()
print("リモコンモーターデモ終了")
