# pybricks.tools — ユーティリティ

## 概要

`pybricks.tools` モジュールは、タイミング制御・データロギング・線形代数・非同期処理など、プログラム全般に必要なユーティリティを提供します。

```python
from pybricks.tools import wait, StopWatch, DataLog, Matrix, vector, cross, multitask, run_task
```

---

## よく使う機能

- `wait(time)` — 指定時間待機する（最も基本的な関数）
- `StopWatch` — ループ内で経過時間を計測
- `multitask` / `run_task` — 複数タスクの並行実行
- `Matrix` / `vector` — IMU 計算やセンサー値の線形演算

---

## wait — 待機

```python
wait(time)
```

プログラムを指定時間一時停止します。`async` 関数内では `await wait(time)` として使用できます。

| 引数 | 型 | 説明 |
|---|---|---|
| `time` | Number, ms | 待機時間（ミリ秒） |

**使用例**

```python
from pybricks.tools import wait

# 1 秒待機
wait(1000)

# 非同期コンテキストで使用
async def blink_loop():
    while True:
        hub.light.on(Color.RED)
        await wait(500)
        hub.light.off()
        await wait(500)
```

---

## StopWatch — ストップウォッチ

```python
from pybricks.tools import StopWatch
```

タイマーとして利用できるストップウォッチです。経過時間の計測、一時停止、リセットが可能です。

### コンストラクタ

```python
sw = StopWatch()
```

初期化直後から計測が始まります。

### メソッド

#### `time() -> int: ms`

現在の経過時間を返します。

**戻り値:** 経過時間（ミリ秒）

#### `pause()`

タイマーを一時停止します。

#### `resume()`

一時停止したタイマーを再開します。

#### `reset()`

タイマーを 0 にリセットします。実行中なら実行を続け、一時停止中なら一時停止のまま 0 に戻ります。

**使用例**

```python
from pybricks.tools import StopWatch, wait

sw = StopWatch()

wait(1000)
print(sw.time())   # 約 1000 ms

sw.pause()
wait(500)
print(sw.time())   # まだ約 1000 ms（一時停止中）

sw.resume()
wait(500)
print(sw.time())   # 約 1500 ms

sw.reset()
print(sw.time())   # 0 ms に戻る
```

---

## DataLog — データロギング

```python
from pybricks.tools import DataLog
```

プログラムの実行中にデータを CSV ファイルに保存します。EV3 などのファイルシステムを持つデバイスで使用します。

### コンストラクタ

```python
DataLog(*headers, name='log', timestamp=True, extension='csv', append=False)
```

| 引数 | 型 | 説明 |
|---|---|---|
| `*headers` | str | 列ヘッダー名（可変長） |
| `name` | str | ファイル名（デフォルト: `'log'`） |
| `timestamp` | bool | `True` でファイル名に日時を追加（ユニーク化） |
| `extension` | str | ファイル拡張子（デフォルト: `'csv'`） |
| `append` | bool | `True` で既存ファイルに追記する |

### メソッド

#### `log(*values)`

1行分のデータをファイルに書き込みます。

| 引数 | 型 | 説明 |
|---|---|---|
| `*values` | any | 書き込む値（可変長） |

**使用例**

```python
from pybricks.tools import DataLog, StopWatch, wait
from pybricks.pupdevices import Motor
from pybricks.parameters import Port

sw = StopWatch()
motor = Motor(Port.A)
log = DataLog('time', 'angle', 'speed', name='motor_log')

motor.run(200)

for _ in range(100):
    log.log(sw.time(), motor.angle(), motor.speed())
    wait(10)
```

---

## Matrix — 行列

```python
from pybricks.tools import Matrix
```

数学的な行列クラスです。加算・減算・行列積・スカラー演算をサポートします。`IMU.orientation()` や `Axis` で返される型です。

### コンストラクタ

```python
Matrix(rows)
```

| 引数 | 型 | 説明 |
|---|---|---|
| `rows` | list[list[float]] | 行のリスト。各行は数値のリスト |

### プロパティ

| プロパティ | 説明 |
|---|---|
| `M.T` | 転置行列を返す |
| `M.shape` | `(行数, 列数)` のタプルを返す |

### 演算子

| 演算 | 説明 |
|---|---|
| `A + B` | 行列の加算 |
| `A - B` | 行列の減算 |
| `A * B` | 行列積（または スカラー乗算） |
| `A / c` | スカラー除算 |

**使用例**

```python
from pybricks.tools import Matrix, vector

# 3x3 行列の生成
M = Matrix([[1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]])

print(M.shape)   # (3, 3)
print(M.T)       # 転置（恒等行列なので同じ）

# ベクトルとの積
v = vector(1, 2, 3)
result = M * v   # 結果もベクトル
```

---

## vector — ベクトル生成

```python
from pybricks.tools import vector
```

`Matrix` オブジェクトとして列ベクトルを生成するヘルパー関数です。

### シグネチャ

```python
vector(x, y) -> Matrix        # 2次元ベクトル (2, 1)
vector(x, y, z) -> Matrix     # 3次元ベクトル (3, 1)
```

| 引数 | 型 | 説明 |
|---|---|---|
| `x` | float | X 成分 |
| `y` | float | Y 成分 |
| `z` | float | Z 成分（オプション） |

**使用例**

```python
from pybricks.tools import vector

v2 = vector(3.0, 4.0)           # 2D ベクトル
v3 = vector(1.0, 0.0, 0.0)     # X 軸方向の単位ベクトル

print(v3.shape)   # (3, 1)
```

---

## cross — クロス積

```python
from pybricks.tools import cross
```

3 次元ベクトルのクロス積（外積）を計算します。

### シグネチャ

```python
cross(a, b) -> Matrix
```

| 引数 | 型 | 説明 |
|---|---|---|
| `a` | Matrix | 3次元ベクトル |
| `b` | Matrix | 3次元ベクトル |

**戻り値:** `a × b` の 3次元ベクトル

**使用例**

```python
from pybricks.tools import vector, cross

a = vector(1, 0, 0)
b = vector(0, 1, 0)
c = cross(a, b)   # vector(0, 0, 1)
```

---

## hub_menu — ハブメニュー

```python
from pybricks.tools import hub_menu
```

ハブのディスプレイにメニューを表示し、ボタン操作で選択肢を選ばせます。複数プログラムを切り替える際に便利です。

### シグネチャ

```python
hub_menu(*symbols) -> int | str
```

| 引数 | 型 | 説明 |
|---|---|---|
| `*symbols` | int または str | メニューに表示する選択肢（可変長） |

**戻り値:** ユーザーが選択したシンボル

**使用例**

```python
from pybricks.tools import hub_menu

selection = hub_menu(1, 2, 3)

if selection == 1:
    print("プログラム1を実行")
elif selection == 2:
    print("プログラム2を実行")
```

---

## multitask — 並行処理

```python
from pybricks.tools import multitask
```

複数のコルーチンを同時に実行します。複数の動作（モーター制御・センサー読み取り・ライト点滅など）を並行させるときに使います。

### シグネチャ

```python
multitask(*coroutines, race=False) -> Tuple
```

| 引数 | 型 | 説明 |
|---|---|---|
| `*coroutines` | coroutine | 並行実行するコルーチン（可変長） |
| `race` | bool | `False`: 全コルーチンが終了するまで待つ。`True`: 1つが終了したら残りをキャンセル |

**戻り値:** 各コルーチンの戻り値のタプル（未完了のものは `None`）

**使用例**

```python
from pybricks.tools import multitask, run_task, wait
from pybricks.hubs import PrimeHub
from pybricks.parameters import Color

hub = PrimeHub()

async def blink():
    for _ in range(5):
        hub.light.on(Color.RED)
        await wait(300)
        hub.light.off()
        await wait(300)

async def beep():
    for _ in range(3):
        await hub.speaker.beep(440, 200)
        await wait(300)

async def main():
    # 点滅と音を同時に実行
    await multitask(blink(), beep())

run_task(main())
```

---

## run_task — コルーチン実行

```python
from pybricks.tools import run_task
```

メインの `async` 関数（コルーチン）をプログラムの起動点から実行します。`multitask` と組み合わせて非同期プログラムを動作させます。

### シグネチャ

```python
run_task(coroutine) -> bool | None
```

| 引数 | 型 | 説明 |
|---|---|---|
| `coroutine` | coroutine | 実行するメインコルーチン |

> **注意:** `run_task` はネストして呼び出せません（1回のみ）。

**使用例**

```python
from pybricks.tools import run_task, wait

async def main():
    print("開始")
    await wait(1000)
    print("終了")

run_task(main())
```

---

## read_input_byte — 標準入力読み取り

```python
from pybricks.tools import read_input_byte
```

標準入力から 1 バイトを非ブロッキングで読み取ります。

### シグネチャ

```python
read_input_byte(last=False, chr=False) -> int | str | None
```

| 引数 | 型 | 説明 |
|---|---|---|
| `last` | bool | `True` でバッファの最新バイトを読む（古いものは破棄） |
| `chr` | bool | `True` で結果を 1 文字の文字列に変換 |

**戻り値:** 読み取ったバイト値（0〜255）、または文字列。データがない場合は `None`。
