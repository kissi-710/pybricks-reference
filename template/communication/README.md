# ハブ間通信テンプレート（communication/）

## 概要

`pybricks.messaging.BLERadio` を使って、複数の SPIKE Prime ハブ間で無線通信を
行うテンプレート集です。Bluetooth Low Energy（BLE）のブロードキャストにより、
ペアリングや接続の確立なしにデータをやり取りできます。

## テンプレート一覧

| ファイル | 説明 | 主な用途 |
|---|---|---|
| [01_broadcast.py](01_broadcast.py) | データの送信（broadcast） | センサー値などを他ハブへ発信 |
| [02_observe.py](02_observe.py) | データの受信（observe） | 他ハブのデータを受信 |
| [03_two_way.py](03_two_way.py) | 双方向通信（送受信を同時に実行） | 2 台のハブの相互連携 |

## BLERadio クラスの使い方

```python
from pybricks.messaging import BLERadio

# 送信用: broadcast_channel を指定
radio = BLERadio(broadcast_channel=1)
radio.broadcast((True, 42))     # タプルでまとめて送信可

# 受信用: observe_channels に監視チャンネルのリストを指定
radio = BLERadio(observe_channels=[1])
data = radio.observe(1)         # 最新データ、無ければ None
```

## 主なメソッド

| メソッド | 説明 |
|---|---|
| `broadcast(data)` | データを送信（`None` で送信停止） |
| `observe(channel)` | 指定チャンネルの最新データを取得（1 秒以内に受信が無ければ `None`） |
| `signal_strength(channel)` | 信号強度 (dBm) を取得 |
| `version()` | Bluetooth チップのバージョン |

## 送れるデータと制限

- **対応型:** `bool` / `int` / `float` / `str` / `bytes`、およびそれらのタプル・リスト
- **サイズ上限:** 合計 26 バイト
  - `bool`: 1 バイト / `float`: 5 バイト / `int`: 2〜5 バイト / `str`・`bytes`: 文字数+1 バイト

## 使い方の流れ

1. 送信側のハブで `01_broadcast.py` を実行
2. 受信側のハブで `02_observe.py` を実行
3. 双方向にやり取りする場合は、2 台とも `03_two_way.py` を実行し、
   チャンネル番号（`CHANNEL_ME` / `CHANNEL_OTHER`）を入れ替える

## 注意点

- 送受信のチャンネル番号（0〜255）を送信側と受信側で一致させる必要があります。
- ハブがコンピュータ等と Bluetooth 接続中だと受信の信頼性が下がります。
