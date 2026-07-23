"""
SPIKE Prime × Raspberry Pi テンプレート: Pi 側コマンド送信
=================================================

※ このファイルは SPIKE Prime ハブ上ではなく、Raspberry Pi（または
   その他の Linux/Windows/Mac PC）上で実行する「ホスト側」のスクリプトです。
   pybricks ライブラリではなく、汎用 BLE ライブラリ bleak を使用します。

【役割】
  ハブ側で 01_hub_command_listener.py を実行しておくと、このスクリプトから
  "RUN" / "PAUSE" / "STOP" コマンドを BLE 経由で送信し、モーターの動作を
  ハブ側プログラムを止めずに随時制御できます。
  画像認識などの結果に応じて send_command() を呼ぶ想定です。

【事前準備】
  pip install bleak

【接続の仕組み】
  Pybricks ファームウェアが提供する「Pybricks Command/Event Characteristic」
  （UUID: c5f50002-8280-46da-89f4-6d8051e4aeef）を使い、
  0x06（write stdin コマンド）+ 文字列データ を書き込むことで、
  ハブ側の stdin にテキストを送り込みます。
  参考: https://pybricks.com/projects/tutorials/wireless/hub-to-device/pc-communication/

【注意】
  - ハブに Pybricks Code など他のアプリが接続されていると、このスクリプトは
    ハブを見つけられません。他のアプリは切断しておいてください。
  - HUB_NAME は自分のハブの Bluetooth 名に合わせて変更してください
    （Pybricks Code の設定画面で確認・変更できます）。
  - 接続後、ハブ側のボタンでプログラムを起動する必要があります
    （プログラムの自動起動まで自動化したい場合は pybricksdev ライブラリを検討してください）。
"""

import asyncio
from contextlib import suppress
from bleak import BleakScanner, BleakClient

PYBRICKS_COMMAND_EVENT_CHAR_UUID = "c5f50002-8280-46da-89f4-6d8051e4aeef"

# 自分のハブの Bluetooth 名に合わせて変更する
HUB_NAME = "Pybricks Hub"


async def main():
    main_task = asyncio.current_task()
    ready_event = asyncio.Event()

    def handle_disconnect(_):
        print("ハブが切断されました")
        if not main_task.done():
            main_task.cancel()

    def handle_rx(_, data: bytearray):
        # data[0] == 0x01 は「write stdout」イベント（ハブからの出力）
        if data[0] == 0x01:
            payload = data[1:]
            if payload == b"rdy":
                ready_event.set()
            else:
                print("ハブからの応答:", payload)

    # --- 1. ハブをスキャンして発見 ---
    print("ハブをスキャン中...")
    device = await BleakScanner.find_device_by_name(HUB_NAME)
    if device is None:
        print(f"ハブが見つかりませんでした（名前: {HUB_NAME}）")
        return

    # --- 2. 接続して通知を購読 ---
    async with BleakClient(device, disconnected_callback=handle_disconnect) as client:
        await client.start_notify(PYBRICKS_COMMAND_EVENT_CHAR_UUID, handle_rx)

        async def send_command(text: str):
            """ハブの stdin にコマンド文字列（改行区切り）を送信する"""
            await client.write_gatt_char(
                PYBRICKS_COMMAND_EVENT_CHAR_UUID,
                b"\x06" + text.encode() + b"\n",  # 0x06 = write stdin コマンド
                response=True,
            )

        print("ハブ側のボタンでプログラムを起動してください")
        await asyncio.sleep(3)  # ハブ側の起動待ち（環境に応じて調整）

        # --- 3. 動作確認: 一時停止 → 2秒待機 → 再開 ---
        print("PAUSE を送信")
        await send_command("PAUSE")
        await asyncio.sleep(2)

        print("RUN を送信")
        await send_command("RUN")

        # --- 実際の運用イメージ ---
        # 画像認識ループの中で、判定結果に応じて以下のように呼び出す:
        #
        #   if 障害物を検出した:
        #       await send_command("PAUSE")
        #   else:
        #       await send_command("RUN")

        print("動作確認が完了しました。Ctrl+C で終了します。")
        await asyncio.sleep(3600)  # 継続的に接続を維持する場合はここでループ待機


if __name__ == "__main__":
    with suppress(asyncio.CancelledError, KeyboardInterrupt):
        asyncio.run(main())
