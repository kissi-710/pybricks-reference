"""
SPIKE Prime 通信テンプレート: BLE 双方向通信
=================================================

1 台のハブで「送信」と「受信」を同時に行い、2 台のハブを相互通信させます。
2 台にこのプログラムを書き込み、CHANNEL_ME / CHANNEL_OTHER を入れ替えると、
お互いの状態を送り合えます。

【設定方法】
  ハブ A: CHANNEL_ME = 1, CHANNEL_OTHER = 2
  ハブ B: CHANNEL_ME = 2, CHANNEL_OTHER = 1

【動作例】
  自分のボタン状態を送信しつつ、相手のボタン状態を受信してライトに反映する。
"""

from pybricks.hubs import PrimeHub
from pybricks.messaging import BLERadio
from pybricks.parameters import Button, Color
from pybricks.tools import wait

# --- このハブの設定（2 台目では数字を入れ替える）---
CHANNEL_ME = 1      # 自分が送信するチャンネル
CHANNEL_OTHER = 2   # 相手が送信するチャンネル（自分が監視する）

hub = PrimeHub()

# 送信用チャンネルと受信用チャンネルを同時に設定
radio = BLERadio(broadcast_channel=CHANNEL_ME, observe_channels=[CHANNEL_OTHER])

print("双方向通信 開始 (送信:", CHANNEL_ME, "受信:", CHANNEL_OTHER, ")")

while True:
    # --- 1. 自分の状態を送信 ---
    # CENTER ボタンが押されているかを送る
    my_pressed = Button.CENTER in hub.buttons.pressed()
    radio.broadcast(my_pressed)

    # --- 2. 相手の状態を受信 ---
    other_pressed = radio.observe(CHANNEL_OTHER)

    # --- 3. 相手の状態をライトで表示 ---
    if other_pressed is None:
        hub.light.on(Color.RED)        # 相手が見つからない
    elif other_pressed:
        hub.light.on(Color.GREEN)      # 相手がボタンを押している
    else:
        hub.light.on(Color.BLUE)       # 相手は押していない

    print("自分:", my_pressed, "| 相手:", other_pressed)
    wait(100)
