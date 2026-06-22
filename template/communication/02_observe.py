"""
SPIKE Prime 通信テンプレート: BLE ブロードキャスト受信
=================================================

BLERadio で他のハブが送信（broadcast）したデータを受信（observe）します。

【このプログラム（受信側）の役割】
  channel 1 を監視し、01_broadcast.py が送ってくるデータを受け取る。

【ポイント】
  - observe_channels に監視したいチャンネルのリストを渡す
  - observe(channel) は最新データを返す。1 秒以内に受信が無ければ None
  - 受信専用なら broadcast_channel は指定しなくてよい
"""

from pybricks.hubs import PrimeHub
from pybricks.messaging import BLERadio
from pybricks.parameters import Color
from pybricks.tools import wait

hub = PrimeHub()

# BLERadio を作成し、observe_channels に監視するチャンネルのリストを指定
radio = BLERadio(observe_channels=[1])

print("channel 1 を監視します")

while True:
    # channel 1 の最新データを取得
    data = radio.observe(1)

    if data is None:
        # まだ受信していない、または 1 秒以上途絶えた
        hub.light.on(Color.RED)
        print("受信なし...")
    else:
        # 送信側が (is_pressed, counter) のタプルを送っている前提
        is_pressed, counter = data
        hub.light.on(Color.GREEN if is_pressed else Color.BLUE)
        print("受信:", data, "| 信号強度:", radio.signal_strength(1), "dBm")

    wait(100)
