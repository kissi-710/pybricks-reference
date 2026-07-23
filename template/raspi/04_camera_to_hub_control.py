"""
SPIKE Prime × Raspberry Pi テンプレート: カメラ検出 → ハブ制御 統合
=================================================

※ このファイルは Raspberry Pi 上で実行するホスト側スクリプトです。
   01_hub_command_listener.py をハブ側で実行しておき、このスクリプトが
   カメラの検出結果に応じて "PAUSE" / "RUN" コマンドを BLE 経由で送信します。

【全体の流れ】
  1. 毎フレーム、色検出ロジック（03_camera_object_detection.py と同じもの）で
     物体を検出する
  2. 検出状態が「未検出→検出」に変化した瞬間に "PAUSE" を送信
  3. 検出状態が「検出→未検出」に変化した瞬間に "RUN" を送信
     （状態が変化した時だけ送信することで、通信を無駄に増やさない）

【03 との関係】
  検出ロジックは 03_camera_object_detection.py と同一です。他のテンプレート
  同様、このファイル単体でコピーして動かせるように、あえてインポートせず
  同じ内容を埋め込んでいます。検出条件を変更する場合は、このファイル内の
  LOWER_RED_* / UPPER_RED_* / MIN_AREA を編集してください
  （03 側と揃えたい場合は両方を修正してください）。

【事前準備】
  - raspi/README.md の「セットアップ手順」を参照し、bleak と
    python3-picamera2 / python3-opencv を利用可能にしておく
  - ハブに 01_hub_command_listener.py を書き込んでおく（まだ実行しない）
  - このスクリプトの HUB_NAME を自分のハブ名に合わせて変更する
"""

import asyncio
from contextlib import suppress

import cv2
import numpy as np
from bleak import BleakClient, BleakScanner
from picamera2 import Picamera2

PYBRICKS_COMMAND_EVENT_CHAR_UUID = "c5f50002-8280-46da-89f4-6d8051e4aeef"

# 自分のハブの Bluetooth 名に合わせて変更する
HUB_NAME = "Pybricks Hub"

# 状態が変化してから次の送信までの最小間隔（秒）。チャタリング防止用
DEBOUNCE_SEC = 0.5

# --- 検出したい色の HSV 範囲（デフォルト: 赤）。詳細は 03 のコメントを参照 ---
LOWER_RED_1 = np.array([0, 120, 70])
UPPER_RED_1 = np.array([10, 255, 255])
LOWER_RED_2 = np.array([170, 120, 70])
UPPER_RED_2 = np.array([180, 255, 255])
MIN_AREA = 2000


def detect_object(frame_bgr):
    """1フレームから対象色の物体を検出する（03_camera_object_detection.py と同じロジック）"""
    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, LOWER_RED_1, UPPER_RED_1)
    mask2 = cv2.inRange(hsv, LOWER_RED_2, UPPER_RED_2)
    mask = cv2.bitwise_or(mask1, mask2)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return False, 0

    largest = max(contours, key=cv2.contourArea)
    area = int(cv2.contourArea(largest))
    return area >= MIN_AREA, area


async def main():
    main_task = asyncio.current_task()
    ready_event = asyncio.Event()

    def handle_disconnect(_):
        print("ハブが切断されました")
        if not main_task.done():
            main_task.cancel()

    def handle_rx(_, data: bytearray):
        if data[0] == 0x01:  # write stdout イベント
            payload = data[1:]
            if payload == b"rdy":
                ready_event.set()
            else:
                print("ハブからの応答:", payload)

    print("ハブをスキャン中...")
    device = await BleakScanner.find_device_by_name(HUB_NAME)
    if device is None:
        print(f"ハブが見つかりませんでした（名前: {HUB_NAME}）")
        return

    async with BleakClient(device, disconnected_callback=handle_disconnect) as client:
        await client.start_notify(PYBRICKS_COMMAND_EVENT_CHAR_UUID, handle_rx)

        async def send_command(text: str):
            await client.write_gatt_char(
                PYBRICKS_COMMAND_EVENT_CHAR_UUID,
                b"\x06" + text.encode() + b"\n",
                response=True,
            )

        print("ハブ側のボタンでプログラムを起動してください")
        await asyncio.sleep(3)

        # --- カメラ初期化 ---
        picam2 = Picamera2()
        config = picam2.create_preview_configuration(main={"size": (640, 480)})
        picam2.configure(config)
        picam2.start()

        # 直前に送ったコマンドに対応する状態（None: 未送信 / True: 検出中 / False: 未検出中）
        last_state = None
        last_change_time = 0.0

        print("検出ループを開始します（Ctrl+C で終了）")

        try:
            while True:
                frame_rgb = picam2.capture_array()
                frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

                detected, area = detect_object(frame_bgr)

                now = asyncio.get_running_loop().time()

                # --- 状態が変化し、かつデバウンス時間が経過していたら送信 ---
                if detected != last_state and (now - last_change_time) >= DEBOUNCE_SEC:
                    if detected:
                        print(f"物体検出（面積={area}）→ PAUSE 送信")
                        await send_command("PAUSE")
                    else:
                        print("物体消失 → RUN 送信")
                        await send_command("RUN")

                    last_state = detected
                    last_change_time = now

                await asyncio.sleep(0.05)  # 約20fpsで判定（負荷に応じて調整）

        except KeyboardInterrupt:
            pass
        finally:
            picam2.stop()
            print("終了します")


if __name__ == "__main__":
    with suppress(asyncio.CancelledError, KeyboardInterrupt):
        asyncio.run(main())
