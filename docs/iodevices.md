# pybricks.iodevices — I/O デバイス

## 概要

`pybricks.iodevices` モジュールは、汎用・カスタム I/O デバイス（I2C・UART・アナログ）や Powered Up プロトコル対応デバイス、Xbox コントローラーなどを制御するクラスを提供します。

```python
from pybricks.iodevices import (
    PUPDevice, LUMPDevice, DCMotor,
    AnalogSensor, I2CDevice, UARTDevice,
    LWP3Device, XboxController
)
```

---

## PUPDevice — Powered Up デバイス（汎用）

```python
from pybricks.iodevices import PUPDevice
from pybricks.parameters import Port

device = PUPDevice(Port.A)
```

Powered Up ポートに接続された任意のモーター・センサーを汎用的に読み書きします。デバイス固有のクラスが存在しない場合に使用します。

### メソッド

#### `info() -> dict`

デバイス情報を返します。

**戻り値:** パッシブデバイスは `{"id": ...}` のみ。UART デバイスは `{"id": ..., "modes": [(名前, 値の数, データ型), ...]}` を含む辞書

#### `read(mode) -> Tuple`

指定モードで値を読み取ります。

| 引数 | 型 | 説明 |
|---|---|---|
| `mode` | int | デバイスのモード番号 |

#### `write(mode, data)`

指定モードにデータを書き込みます。

| 引数 | 型 | 説明 |
|---|---|---|
| `mode` | int | デバイスのモード番号 |
| `data` | tuple | 書き込むデータ |

#### `reset()`

UART デバイスをリセットします（再同期させる）。

**使用例**

```python
from pybricks.iodevices import PUPDevice
from pybricks.parameters import Port

device = PUPDevice(Port.A)

# デバイス情報を確認
info = device.info()
print(info)

# モード 0 で読み取り
values = device.read(0)
print(values)
```

---

## LUMPDevice — LEGO UART デバイス

```python
from pybricks.iodevices import LUMPDevice
```

LEGO UART Messaging Protocol（LUMP）準拠のデバイスにアクセスします。EV3 では UART デバイスのみ対応。`PUPDevice` と同じ API を持ちます。

---

## DCMotor — EV3 DC モーター

```python
from pybricks.iodevices import DCMotor
```

EV3 用の DC モーターです。`pybricks._common.DCMotor` を継承します。詳細: [motors.md](motors.md)

---

## AnalogSensor — アナログセンサー（汎用・カスタム）

```python
from pybricks.iodevices import AnalogSensor
from pybricks.parameters import Port

sensor = AnalogSensor(Port.S1)
# カスタムセンサーの場合
custom = AnalogSensor(Port.S2, custom=True)
```

EV3 のセンサーポートに接続されたアナログセンサー（標準またはカスタム）を読み取ります。

### コンストラクタ

```python
AnalogSensor(port, custom=False)
```

| 引数 | 型 | 説明 |
|---|---|---|
| `port` | Port | 接続ポート |
| `custom` | bool | `True` でカスタムアナログセンサーとして使用 |

### メソッド

#### `voltage() -> int: mV`

アナログ電圧を返します。

#### `resistance() -> int: Ω`

抵抗値を返します（パッシブ負荷を接続している場合）。10 kΩ 内部プルアップを前提とした計算値。

#### `active()`

センサーのピン 5 を HIGH に設定します。NXT 光センサーのライトを点灯するなど、センサーのモードを切り替えます。

#### `passive()`

センサーのピン 5 を LOW に設定します。

**使用例**

```python
from pybricks.iodevices import AnalogSensor
from pybricks.parameters import Port

# NXT 光センサーをカスタム接続として使う
sensor = AnalogSensor(Port.S1, custom=True)
sensor.active()            # ライト点灯（反射光モード）
v = sensor.voltage()       # 反射光の電圧
sensor.passive()           # ライト消灯（周囲光モード）
v = sensor.voltage()       # 周囲光の電圧
```

---

## I2CDevice — I2C デバイス

```python
from pybricks.iodevices import I2CDevice
from pybricks.parameters import Port

device = I2CDevice(Port.S1, address=0x53)
```

I2C プロトコルで通信するカスタムデバイスを制御します。

> **注意:** `power_pin` オプションは慎重に使用してください。電源を誤って印加すると機器が損傷する場合があります。

### コンストラクタ

```python
I2CDevice(port, address, custom=False, power_pin=0, nxt_quirk=False)
```

| 引数 | 型 | 説明 |
|---|---|---|
| `port` | Port | 接続ポート |
| `address` | int | I2C アドレス（0x00〜0xFF） |
| `custom` | bool | カスタムデバイスの場合 `True` |
| `power_pin` | int | 電源供給ピン（0: なし、1: バッテリー電源を Pin 1 に供給） |
| `nxt_quirk` | bool | 旧 NXT I2C センサー向けのスロータイミングを使用 |

### メソッド

#### `read(reg=None, length=1) -> bytes`

指定レジスタからバイトを読み取ります。

| 引数 | 型 | 説明 |
|---|---|---|
| `reg` | int | 読み取り開始レジスタ（0〜255）。`None` でレジスタ指定なし |
| `length` | int | 読み取るバイト数 |
| `map` | callable | 戻り値を変換する関数（省略可） |

**戻り値:** 読み取ったバイト列（`map` がある場合はその戻り値）

#### `write(reg=None, data=None)`

指定レジスタにデータを書き込みます。

| 引数 | 型 | 説明 |
|---|---|---|
| `reg` | int | 書き込み先レジスタ（0〜255）。`None` でレジスタ指定なし |
| `data` | bytes | 書き込むデータ（`None` でレジスタのみ送信） |

**例外:** `reg` あり + `data` が 32 バイト超の場合 `ValueError`

**使用例**

```python
from pybricks.iodevices import I2CDevice
from pybricks.parameters import Port

device = I2CDevice(Port.S1, address=0x53)

# レジスタ 0x32 から 6 バイト読み取り
data = device.read(0x32, length=6)

# 設定書き込み
device.write(0x2D, b'\x08')

# 変換関数付き読み取り
value = device.read(0x00, length=2, map=lambda b: int.from_bytes(b, 'big'))
```

---

## UARTDevice — UART デバイス

```python
from pybricks.iodevices import UARTDevice
from pybricks.parameters import Port

device = UARTDevice(Port.A, baudrate=9600)
```

UART（シリアル通信）プロトコルで通信するカスタムデバイスを制御します。

> **注意:** `power_pin` オプションは慎重に使用してください。

### コンストラクタ

```python
UARTDevice(port, baudrate=115200, timeout=None, power_pin=0)
```

| 引数 | 型 | 説明 |
|---|---|---|
| `port` | Port | 接続ポート |
| `baudrate` | int | ボーレート（デフォルト: 115200） |
| `timeout` | Number, ms | 読み書きのタイムアウト（`None` で無制限） |
| `power_pin` | int | 電源供給ピン（0: なし。Powered Up ハブは 1 または 2） |

### メソッド

#### `read(length=1) -> bytes`

指定バイト数を受信します（指定バイト数が揃うまでブロック）。

| 引数 | 型 | 説明 |
|---|---|---|
| `length` | int | 読み取るバイト数（1以上） |

#### `read_all() -> bytes`

バッファ内のすべてのバイトを即座に返します。

#### `write(data)`

データを送信します。

| 引数 | 型 | 説明 |
|---|---|---|
| `data` | bytes | 送信するバイトデータ |

#### `waiting() -> int`

バッファ内の未読バイト数を返します。

#### `set_baudrate(baudrate)`

ボーレートを変更します。

#### `wait_until(pattern)`

特定のバイト列が受信されるまで待機します。

| 引数 | 型 | 説明 |
|---|---|---|
| `pattern` | bytes | 待機するバイト列（空でないこと） |

#### `clear()`

受信バッファをクリアします。

**使用例**

```python
from pybricks.iodevices import UARTDevice
from pybricks.parameters import Port

device = UARTDevice(Port.A, baudrate=9600, timeout=1000)

# コマンド送信
device.write(b'\x01\x02\x03')

# 応答受信
response = device.read(5)

# バッファ読み出し
if device.waiting() > 0:
    data = device.read_all()

# 特定パターンを待機
device.wait_until(b'\xFF\xFF')
```

---

## LWP3Device — LEGO Wireless Protocol v3

```python
from pybricks.iodevices import LWP3Device
```

LEGO 公式ファームウェアを実行しているハブに Bluetooth で接続し、LEGO Wireless Protocol v3 でメッセージを送受信します。

### コンストラクタ

```python
LWP3Device(hub_kind, name=None, timeout=10000, pair=False, num_notifications=8, connect=True)
```

| 引数 | 型 | 説明 |
|---|---|---|
| `hub_kind` | int | 接続先ハブのタイプ ID |
| `name` | str | Bluetooth 名（`None` で最初に見つかったものに接続） |
| `timeout` | int, ms | タイムアウト時間 |
| `pair` | bool | セキュア接続のためのペアリングを試みる（一部ハブで必要） |
| `num_notifications` | int | 受信バッファのメッセージ数 |
| `connect` | bool | `False` でスキップし、後で `connect()` を呼ぶ |

### メソッド

#### `connect()`

デバイスに接続します。

#### `name(name)` / `name() -> str`

Bluetooth 名を設定または取得します。

#### `write(buf)`

メッセージを送信します（最大 20 バイト）。

#### `read() -> bytes | None`

最も古いバッファ済みメッセージを返します。メッセージがない場合は `None` を返します。

#### `disconnect()`

接続を切断します。

---

## XboxController — Xbox コントローラー

```python
from pybricks.iodevices import XboxController

controller = XboxController()
```

Microsoft® Xbox® コントローラーを Bluetooth センサーとして使用します。プログラム終了時に自動的に切断されます。

### コンストラクタ

```python
XboxController(joystick_deadzone=10, name=None, timeout=10000, connect=True)
```

| 引数 | 型 | 説明 |
|---|---|---|
| `joystick_deadzone` | Number, % | スティックのデッドゾーン（両軸がこれ以下なら 0 と報告） |
| `name` | str | Bluetooth 名（`None` で任意のコントローラーに接続） |
| `timeout` | Number, ms | 接続タイムアウト |

### 属性

| 属性 | クラス |
|---|---|
| `controller.buttons` | `Keypad`（A, B, X, Y, LB, RB, LJ, RJ, UP, DOWN, LEFT, RIGHT, GUIDE, MENU, VIEW など） |

### メソッド

#### `joystick_left() -> Tuple[int, int]`

左スティックの X・Y 位置を返します（-100〜100 %）。

#### `joystick_right() -> Tuple[int, int]`

右スティックの X・Y 位置を返します（-100〜100 %）。

#### `triggers() -> Tuple[int, int]`

左右トリガーの位置を返します（0〜100 %）。

#### `dpad() -> int`

D パッドの方向を返します（1=上, 2=右上, 3=右, 4=右下, 5=下, 6=左下, 7=左, 8=左上, 0=なし）。

#### `rumble(power=100, duration=200, count=1, delay=100)`

コントローラーを振動させます（フォースフィードバック）。

| 引数 | 型 | 説明 |
|---|---|---|
| `power` | Number or Tuple | 振動強度（単一値: 左右共通。タプル: (左ハンドル, 右ハンドル, 左トリガー, 右トリガー)） |
| `duration` | Number, ms | 振動時間（最大 2500 ms） |
| `count` | int | 振動回数（0〜100） |
| `delay` | Number, ms | 振動間の遅延（`count > 1` のとき有効） |

#### `name() -> str`

接続されたコントローラーの Bluetooth 名を返します。

#### `profile() -> int`

プロファイル番号を返します（Xbox Elite Controller Series 2 のみ）。

#### `state() -> Tuple`

すべての生入力値をタプルで返します。

**使用例**

```python
from pybricks.iodevices import XboxController
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Button

motor = Motor(Port.A)
controller = XboxController()

while True:
    x, y = controller.joystick_left()
    motor.run(y * 5)   # Y 軸でモーター制御

    lt, rt = controller.triggers()
    if rt > 10:
        controller.rumble(power=rt)  # トリガーに応じて振動

    pressed = controller.buttons.pressed()
    if Button.A in pressed:
        print("A ボタン押下")
```

