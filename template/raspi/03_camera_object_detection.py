"""
SPIKE Prime × Raspberry Pi テンプレート: カメラ物体検出（単体動作確認用）
=================================================

※ このファイルは SPIKE Prime ハブ上ではなく、Raspberry Pi 上で実行する
   「ホスト側」のスクリプトです。pybricks ではなく picamera2 と OpenCV
   を使用します。

【役割】
  Raspberry Pi Camera Module V2 の映像から、特定の色（デフォルトは赤）の
  物体を検出し、検出の有無をコンソールに表示し続けます。
  04_camera_to_hub_control.py に組み込む前の、カメラ・検出ロジック単体の
  動作確認用テンプレートです。

【検出方法】
  厳密な物体認識（機械学習モデル等）ではなく、HSV色空間での色検出という
  軽量な方法を使っています。Raspberry Pi 上でリアルタイムに動かしやすく、
  「特定色のブロックが視界に入ったら止まる」といった単純な用途に向きます。
  より高度な認識（形状・複数物体・機械学習ベース等）が必要な場合は、
  detect_object() 関数の中身を差し替えてください。

【事前準備】
  sudo apt install -y python3-picamera2 python3-opencv
  詳しい手順は raspi/README.md の「セットアップ手順」を参照してください。
"""

import cv2
import numpy as np
from picamera2 import Picamera2

# --- 検出したい色の HSV 範囲（デフォルト: 赤） ---
# 赤は Hue が 0 付近と 180 付近の両方にまたがるため、2つの範囲を用意する
LOWER_RED_1 = np.array([0, 120, 70])
UPPER_RED_1 = np.array([10, 255, 255])
LOWER_RED_2 = np.array([170, 120, 70])
UPPER_RED_2 = np.array([180, 255, 255])

# 検出とみなす最小の面積（ピクセル数）。値が小さいほどノイズを拾いやすい
MIN_AREA = 2000


def detect_object(frame_bgr):
    """
    1フレームから対象色の物体を検出する。

    引数:
        frame_bgr: OpenCV形式（BGR）の画像（numpy配列）

    戻り値:
        (detected: bool, area: int) のタプル
        detected は面積が MIN_AREA を超えた場合に True
    """
    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

    mask1 = cv2.inRange(hsv, LOWER_RED_1, UPPER_RED_1)
    mask2 = cv2.inRange(hsv, LOWER_RED_2, UPPER_RED_2)
    mask = cv2.bitwise_or(mask1, mask2)

    # ノイズ除去（小さい点々を消す）
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return False, 0

    largest = max(contours, key=cv2.contourArea)
    area = int(cv2.contourArea(largest))

    return area >= MIN_AREA, area


def main():
    picam2 = Picamera2()
    # 処理速度を優先し、低めの解像度でプレビュー設定する
    config = picam2.create_preview_configuration(main={"size": (640, 480)})
    picam2.configure(config)
    picam2.start()

    print("カメラ検出を開始します（Ctrl+C で終了）")

    try:
        while True:
            # picamera2 は RGB で返すため、OpenCV(BGR前提)用に変換する
            frame_rgb = picam2.capture_array()
            frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

            detected, area = detect_object(frame_bgr)

            if detected:
                print(f"検出: 面積={area}")
            else:
                print("未検出")

    except KeyboardInterrupt:
        print("終了します")
    finally:
        picam2.stop()


if __name__ == "__main__":
    main()
