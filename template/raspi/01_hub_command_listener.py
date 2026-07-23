"""
SPIKE Prime × Raspberry Pi テンプレート: ハブ側コマンド待ち受け
=================================================

Raspberry Pi など外部ホストから BLE 経由で送られてくる文字列コマンドを、
プログラムを止めずに非ブロッキングで受信し続けるテンプレートです。

【想定する使い方】
  画像認識などで「今すぐ止めたい／再開したい」といった非同期の指示を
  ホスト側から送りたい場合に使います。
  "Run" は最初に一度だけ実行し、あとは "PAUSE" / "RESUME" コマンドだけを
  随時送って動作を制御する、という運用を想定しています。

【重要な注意】
  Ctrl+C（break, 0x03）はプログラム自体を強制終了させるための信号です。
  Pause/Resume のような「動作の一時停止・再開」を目的とする場合、
  break は使わないでください。プログラムが終了するとモーターの制御も
  失われ、再開できなくなります。
  ここでは while ループを回し続けたまま、stdin からのコマンド文字列だけで
  状態を切り替えます。

【通信方式】
  pybricks.messaging.BLERadio は「ハブ同士」の通信専用です。
  ホストPC（Raspberry Pi等）とハブ間の通信には使えません。
  代わりに Pybricks 標準の stdin/stdout（Nordic UART Service 経由）を
  使います。ホスト側の実装は 02_raspi_ble_controller.py を参照してください。

【事前準備】
  1. Pybricks Code などでこのプログラムをハブに書き込んでおく
  2. Raspberry Pi 側のスクリプトは、ハブに他のアプリ（Pybricks Code等）が
     接続されておらず、プログラムが未実行の状態でないと接続できません
  3. Raspberry Pi 側から接続後、ハブのボタンでこのプログラムを起動する
"""

from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Color
from pybricks.hubs import PrimeHub
from pybricks.tools import wait

# 標準 MicroPython モジュール（stdin の非ブロッキング読み取りに使用）
from usys import stdin, stdout
from uselect import poll

hub = PrimeHub()
motor = Motor(Port.A)

# --- stdin を poll に登録（データが来ているかをブロックせずに確認できる）---
keyboard = poll()
keyboard.register(stdin)

# 現在の状態（True: 動作中 / False: 一時停止中）
running = True
motor.run(300)
hub.light.on(Color.GREEN)

print("コマンド待ち受け開始（RUN / PAUSE / STOP を受け付けます）")

while True:
    # --- 1. コマンドが届いていないか非ブロッキングでチェック ---
    if keyboard.poll(0):
        # 改行区切りで1コマンド分読み取る
        # （ホスト側は必ず末尾に "\n" を付けて送信すること）
        cmd = stdin.buffer.readline().strip()

        if cmd == b"PAUSE":
            motor.hold()
            running = False
            hub.light.on(Color.RED)
            stdout.buffer.write(b"OK:PAUSE\n")

        elif cmd == b"RUN":
            motor.run(300)
            running = True
            hub.light.on(Color.GREEN)
            stdout.buffer.write(b"OK:RUN\n")

        elif cmd == b"STOP":
            # プログラム自体を終了したい場合のみ使う
            motor.stop()
            stdout.buffer.write(b"OK:STOP\n")
            break

        else:
            # 未知のコマンドは無視して通知だけ返す
            stdout.buffer.write(b"NG:UNKNOWN\n")

    # --- 2. 通常動作（走行・センサー処理など）はここに書く ---
    if running:
        pass  # 例: ライントレースや画像認識結果を使わない自律動作など

    wait(10)

hub.light.off()
print("プログラム終了")
