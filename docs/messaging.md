# pybricks.messaging — メッセージング・通信

## 概要

`pybricks.messaging` モジュールは、ハブ間の無線通信と EV3 の Bluetooth メールボックスを提供します。BLE ブロードキャスト・観測、または EV3 同士のメールボックス通信に使用します。

```python
from pybricks.messaging import (
    BLERadio, Mailbox, LogicMailbox, NumericMailbox, TextMailbox,
    BluetoothMailboxServer, BluetoothMailboxClient, AppData
)
```

---

## BLERadio — BLE ブロードキャスト通信 ⭐

```python
from pybricks.messaging import BLERadio
```

Bluetooth Low Energy（BLE）を使って、接続なしにデータをブロードキャスト（送信）・オブザーブ（受信）します。複数のハブ間でリアルタイムにデータを共有するときに使います。

> **バージョン:** v4.0 以降（以前はハブクラスの属性として提供）

### コンストラクタ

```python
BLERadio(broadcast_channel=None, observe_channels=[])
```

| 引数 | 型 | 説明 |
|---|---|---|
| `broadcast_channel` | int または None | 送信チャンネル（0〜255）。`None` でブロードキャスト無効 |
| `observe_channels` | list[int] | 受信するチャンネルのリスト |

> **注意:** 同時に多くのチャンネルを観測するとメモリを多く消費します。Bluetooth 接続中は受信の信頼性が下がります。

### メソッド

#### `broadcast(data)`

指定チャンネルにデータをブロードキャストします。

| 引数 | 型 | 説明 |
|---|---|---|
| `data` | bool, int, float, str, bytes, list, None | 送信するデータ（最大 26 バイト） |

**対応型:**
- `bool`: 1 バイト
- `float`: 5 バイト
- `int`: 2〜5 バイト（値に依存）
- `str`, `bytes`: 文字数 + 1 バイト

**例外:**
- `RuntimeError`: `broadcast_channel` が未設定
- `ValueError`: データが 26 バイトを超える
- `TypeError`: 非対応型が含まれる

#### `observe(channel) -> bool | int | float | str | bytes | tuple | None`

指定チャンネルの最新受信データを返します。

| 引数 | 型 | 説明 |
|---|---|---|
| `channel` | int | 観測するチャンネル（`observe_channels` に含まれること） |

**戻り値:** 最後に受信したデータ。1 秒以内に受信がなければ `None`

**例外:** `ValueError`: `channel` が `observe_channels` にない

#### `signal_strength(channel) -> int: dBm`

指定チャンネルの平均信号強度を返します。近いデバイスは約 -40 dBm、遠いものは約 -70 dBm。1 秒以内に受信がなければ -128 を返します。

#### `version() -> str`

Bluetooth チップのファームウェアバージョンを返します。

**使用例（送信側ハブ）**

```python
from pybricks.messaging import BLERadio
from pybricks.tools import wait

radio = BLERadio(broadcast_channel=1)

i = 0
while True:
    radio.broadcast(i)
    i += 1
    wait(100)
```

**使用例（受信側ハブ）**

```python
from pybricks.messaging import BLERadio
from pybricks.tools import wait

radio = BLERadio(observe_channels=[1])

while True:
    value = radio.observe(1)
    if value is not None:
        print("受信:", value)
    wait(100)
```

**使用例（双方向通信）**

```python
from pybricks.messaging import BLERadio
from pybricks.tools import wait

radio = BLERadio(broadcast_channel=0, observe_channels=[1])

while True:
    radio.broadcast([motor.angle(), sensor.distance()])
    data = radio.observe(1)
    if data:
        speed, turn = data
    wait(50)
```

---

## Mailbox — メールボックス（EV3）

```python
from pybricks.messaging import Mailbox, BluetoothMailboxClient

client = BluetoothMailboxClient()
client.connect("EV3_NAME")

mailbox = Mailbox("my_box", connection=client)
```

EV3 同士の Bluetooth 通信でデータをやり取りする汎用メールボックスです。デフォルトではバイト列を送受信します。`encode` / `decode` 関数でカスタム型を扱えます。

### コンストラクタ

```python
Mailbox(name, connection, encode=None, decode=None)
```

| 引数 | 型 | 説明 |
|---|---|---|
| `name` | str | メールボックスの名前（相手側と一致させる） |
| `connection` | Connection | 接続オブジェクト（`BluetoothMailboxClient` 等） |
| `encode` | callable | Python オブジェクト → bytes への変換関数 |
| `decode` | callable | bytes → Python オブジェクトへの変換関数 |

### メソッド

#### `read() -> T`

現在のメールボックスの値を返します（空なら `None`）。

#### `send(value, brick=None)`

メールボックスに値を送信します。

| 引数 | 型 | 説明 |
|---|---|---|
| `value` | T | 送信する値 |
| `brick` | str または None | 送信先の EV3 名または Bluetooth アドレス（`None` で全デバイスへ） |

#### `wait()`

メールボックスがリモートデバイスから更新されるまで待機します。

#### `wait_new() -> T`

現在の値とは異なる新しい値が届くまで待機し、その値を返します。

---

## LogicMailbox — 論理値メールボックス（EV3）

```python
from pybricks.messaging import LogicMailbox, BluetoothMailboxClient

client = BluetoothMailboxClient()
client.connect("EV3_NAME")

box = LogicMailbox("ready", connection=client)
```

`bool` 値のみを扱う `Mailbox` のサブクラスです。EV3-G（EV3 LabVIEW）の "logic" メールボックスと互換性があります。

---

## NumericMailbox — 数値メールボックス（EV3）

```python
from pybricks.messaging import NumericMailbox, BluetoothMailboxClient

client = BluetoothMailboxClient()
client.connect("EV3_NAME")

box = NumericMailbox("speed", connection=client)
```

`float` / `int` 値を扱う `Mailbox` のサブクラスです。EV3-G の "numeric" メールボックスと互換性があります。

---

## TextMailbox — テキストメールボックス（EV3）

```python
from pybricks.messaging import TextMailbox, BluetoothMailboxClient

client = BluetoothMailboxClient()
client.connect("EV3_NAME")

box = TextMailbox("message", connection=client)
```

`str` 値を扱う `Mailbox` のサブクラスです。EV3-G の "text" メールボックスと互換性があります。

---

## BluetoothMailboxServer — Bluetooth メールボックスサーバー（EV3）

```python
from pybricks.messaging import BluetoothMailboxServer

server = BluetoothMailboxServer()
```

リモートの EV3（またはクライアント）からの接続を待ち受けます。サーバー側として動作します。

### メソッド

#### `wait_for_connection(count=1)`

クライアントが接続するまで待機します。

| 引数 | 型 | 説明 |
|---|---|---|
| `count` | int | 待機する接続数 |

#### `server_close()`

すべての接続を閉じます。

**コンテキストマネージャー対応**

```python
with BluetoothMailboxServer() as server:
    server.wait_for_connection()
    # 通信処理...
```

**使用例（サーバー側）**

```python
from pybricks.messaging import BluetoothMailboxServer, NumericMailbox

with BluetoothMailboxServer() as server:
    server.wait_for_connection()
    
    box = NumericMailbox("speed", server)
    
    while True:
        speed = box.read()
        if speed is not None:
            motor.run(speed)
```

---

## BluetoothMailboxClient — Bluetooth メールボックスクライアント（EV3）

```python
from pybricks.messaging import BluetoothMailboxClient

client = BluetoothMailboxClient()
```

サーバーとして動作している EV3 に接続を開始します。クライアント側として動作します。

### メソッド

#### `connect(brick)`

サーバー側の EV3 に接続します。相手はペアリング済みで `wait_for_connection()` を実行中である必要があります。

| 引数 | 型 | 説明 |
|---|---|---|
| `brick` | str | 接続先の EV3 の名前または Bluetooth アドレス |

#### `close()`

すべての接続を閉じます。

**コンテキストマネージャー対応**

```python
with BluetoothMailboxClient() as client:
    client.connect("EV3_SERVER_NAME")
    # 通信処理...
```

**使用例（クライアント側）**

```python
from pybricks.messaging import BluetoothMailboxClient, NumericMailbox

with BluetoothMailboxClient() as client:
    client.connect("SERVER_EV3")
    
    box = NumericMailbox("speed", client)
    
    while True:
        box.send(motor.speed())
```

---

## EV3 Bluetooth メールボックス通信の全体例

```python
# === サーバー側（EV3 A）===
from pybricks.hubs import EV3Brick
from pybricks.messaging import BluetoothMailboxServer, TextMailbox

ev3 = EV3Brick()

with BluetoothMailboxServer() as server:
    server.wait_for_connection()
    
    text_box = TextMailbox("chat", server)
    text_box.wait()
    message = text_box.read()
    ev3.screen.print("受信:", message)
    text_box.send("こんにちは！")


# === クライアント側（EV3 B）===
from pybricks.hubs import EV3Brick
from pybricks.messaging import BluetoothMailboxClient, TextMailbox

ev3 = EV3Brick()

with BluetoothMailboxClient() as client:
    client.connect("EV3_A_NAME")
    
    text_box = TextMailbox("chat", client)
    text_box.send("やあ！")
    text_box.wait()
    reply = text_box.read()
    ev3.screen.print("返信:", reply)
```

---

## AppData — アプリデータ通信

```python
from pybricks.messaging import AppData
```

Pybricks Code ホストアプリケーションと USB または Bluetooth を介してデータを交換します。スマートセンサー機能（ビジョンプロセッサー等）で使用します。

インスタンスは同時に 1 つのみ作成可能です。プログラム初期化時に生成し、その後はマルチタスク中でも全メソッドを使用できます。

### コンストラクタ

```python
AppData(modes)
```

| 引数 | 型 | 説明 |
|---|---|---|
| `modes` | list[Tuple[int, int]] | `(モード番号, バッファサイズ)` のリスト。モード番号は 0〜255 で重複不可 |

**例外:**
- `RuntimeError`: AppData インスタンスが既に存在する
- `TypeError`: `modes` が不正な型
- `ValueError`: モード番号が重複している

### メソッド

#### `get_bytes(mode, index=None) -> bytes | int`

ホストから受信したデータを返します。

| 引数 | 型 | 説明 |
|---|---|---|
| `mode` | int | モード番号 |
| `index` | int | 指定すると、そのバイト位置の 1 バイト（int）を返す。`None` でバッファ全体（bytes）を返す |

#### `write_bytes(data)`

ホストにバイトデータを送信します。

| 引数 | 型 | 説明 |
|---|---|---|
| `data` | bytes | 送信するデータ |

#### `configure(mode, parameter, value)`

ホストのモード設定を送信します。`[0x01, mode, parameter] + value` のヘッダーを付けて `write_bytes` を呼び出すラッパーです。

| 引数 | 型 | 説明 |
|---|---|---|
| `mode` | int | 設定するモード番号 |
| `parameter` | int | モード内のパラメータ識別子 |
| `value` | bytes | 設定値 |

#### `close()`

コールバックを無効化し、受信バッファを解放します。ガベージコレクション時にも自動的に呼ばれます。
