"""
SPIKE Prime 通信テンプレート: BLE ブロードキャスト送信
=================================================

BLERadio を使い、接続なしで他のハブにデータを「ばらまく」（broadcast）方法です。
ペアリング不要で、同じチャンネルを見ているハブにデータが届きます。

【このプログラム（送信側）の役割】
  センサーの値などを channel 1 に向けて繰り返し送信する。
  受信側は 02_observe.py を実行する。

【送れるデータ】
  bool / int / float / str / bytes と、それらのタプル・リスト（合計 26 バイトまで）
"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import ForceSensor
from pybricks.messaging import BLERadio
from pybricks.parameters import Port, Color
from pybricks.tools import wait

hub = PrimeHub()

# BLERadio を作成し、broadcast_channel に送信チャンネル番号(0〜255)を指定
radio = BLERadio(broadcast_channel=1)

# 送るデータの元になるセンサー（例: フォースセンサー）
sensor = ForceSensor(Port.E)

print("channel 1 でデータを送信します")
hub.light.on(Color.BLUE)

counter = 0
while True:
    # 送りたい値を用意（ここでは「押されているか」と「カウンタ」のタプル）
    is_pressed = sensor.pressed()
    counter += 1

    # タプルでまとめて送信できる
    radio.broadcast((is_pressed, counter))

    print("送信:", (is_pressed, counter))

    # 送信は約 100ms 間隔程度が目安
    wait(100)
