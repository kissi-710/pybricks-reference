# モーター制御 — DCMotor / Motor / Control

## 概要

pybricks のモータークラスは `pybricks._common` モジュールで定義されており、各デバイスモジュール（`pupdevices`、`ev3devices`）でハードウェア固有のクラスとして公開されています。

| クラス | 説明 | インポート元 |
|---|---|---|
| `DCMotor` | 回転センサーなしのシンプルモーター | `pybricks.pupdevices` / `pybricks.iodevices` |
| `Motor` | 回転センサー付きモーター（主流） | `pybricks.pupdevices` / `pybricks.ev3devices` |
| `Control` | PID コントローラーの設定 | `motor.control` 属性 |
| `Model` | モーター状態オブザーバー | `motor.model` 属性 |

```python
# Powered Up モーター（最もよく使う）
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop

motor = Motor(Port.A)
```

---

## よく使う操作クイックリファレンス

```python
motor = Motor(Port.A)

# 連続回転
motor.run(500)                       # 500 deg/s で回転し続ける

# 時間指定
motor.run_time(500, 2000)            # 2秒間回転

# 角度指定
motor.run_angle(500, 360)            # 360度回転
motor.run_angle(500, -180)           # -180度（逆方向に180度）

# 目標角度指定
motor.run_target(500, 90)            # 現在位置に関わらず 90度へ

# ストールまで回転
stall_angle = motor.run_until_stalled(200)

# 停止
motor.hold()                         # 現在角度でホールド（PID維持）
motor.stop()                         # 自由回転（フリーコースト）
motor.brake()                        # ブレーキ停止

# 状態取得
print(motor.angle())                 # 現在の角度 (deg)
print(motor.speed())                 # 現在の速度 (deg/s)
print(motor.load())                  # 推定負荷トルク (mNm)
print(motor.stalled())               # ストール中か否か
print(motor.done())                  # 現在のコマンドが完了したか

# 角度リセット
motor.reset_angle(0)                 # 角度を 0 にリセット
```

---

## DCMotor — 回転センサーなしモーター

```python
from pybricks.pupdevices import DCMotor
from pybricks.parameters import Port, Direction

motor = DCMotor(Port.A)
```

回転センサーを持たないシンプルなモーター（例: train モーター）の制御クラス。デューティサイクルで出力を調整します。

### コンストラクタ

```python
DCMotor(port, positive_direction=Direction.CLOCKWISE)
```

| 引数 | 型 | 説明 |
|---|---|---|
| `port` | Port | モーターが接続されているポート |
| `positive_direction` | Direction | 正の値を与えたときの回転方向 |

### メソッド

#### `dc(duty)`

指定したデューティサイクルでモーターを回転させます。

| 引数 | 型 | 説明 |
|---|---|---|
| `duty` | Number, % | デューティサイクル（-100 〜 100） |

#### `stop()`

モーターを停止し、自由回転（フリーコースト）させます。摩擦で徐々に停止します。

#### `brake()`

受動的にブレーキをかけます。摩擦に加え、回転中に生じる逆起電力による制動が働きます。

#### `settings(max_voltage)` / `settings() -> Tuple[int]`

モーター設定を行います。引数なしで現在値を返します。

| 引数 | 型 | 説明 |
|---|---|---|
| `max_voltage` | Number, mV | すべてのコマンドで適用される最大電圧 |

**使用例**

```python
from pybricks.pupdevices import DCMotor
from pybricks.parameters import Port

motor = DCMotor(Port.A)

motor.dc(50)         # 50% の出力で回転
motor.stop()         # フリーコースト
motor.brake()        # ブレーキ

motor.settings(max_voltage=7400)  # 電圧上限を 7.4V に設定
```

---

## Motor — 回転センサー付きモーター

```python
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop

motor = Motor(Port.A)
```

回転センサー内蔵のモーター。速度・角度の精密制御が可能で、通常はこちらを使います。`DCMotor` の機能を継承します。

### コンストラクタ

```python
Motor(port, positive_direction=Direction.CLOCKWISE, gears=None, reset_angle=True, profile=None)
```

| 引数 | 型 | 説明 |
|---|---|---|
| `port` | Port | モーターが接続されているポート |
| `positive_direction` | Direction | 正の速度値に対応する回転方向 |
| `gears` | list | ギアトレインの歯数リスト（例: `[12, 36]`）。複数段の場合はリストのリスト |
| `reset_angle` | bool | `True`: 絶対マーカー角度（-180〜179）にリセット。`False`: 前回値を保持 |
| `profile` | Number, deg | 精度プロファイル。小さいほど精確だが振動しやすい（デフォルト: 約11度） |

### 属性

| 属性 | 説明 |
|---|---|
| `motor.control` | `Control` オブジェクト（PID 設定） |
| `motor.model` | `Model` オブジェクト（モーター状態オブザーバー） |

### 状態取得メソッド

#### `angle() -> int: deg`

モーターの現在の回転角度を返します。

**戻り値:** 角度（度）

#### `speed(window=100) -> int: deg/s`

モーターの現在の速度を返します。

| 引数 | 型 | 説明 |
|---|---|---|
| `window` | Number, ms | 速度計算に使う時間窓。短いほどレスポンスが速いが不安定 |

**戻り値:** 速度（度/秒）

#### `stalled() -> bool`

モーターがストール（止まった）しているか確認します。

**戻り値:** `True` ならストール中、`False` なら正常動作

#### `load() -> int: mNm`

モーターが受けている負荷トルクの推定値を返します。

**戻り値:** 負荷トルク（mNm）

#### `done() -> bool`

実行中のコマンドが完了したか確認します。

**戻り値:** `True` なら完了、`False` なら実行中

### 制御メソッド

#### `run(speed)`

指定速度で連続回転します。新しいコマンドが来るまで回り続けます。

| 引数 | 型 | 説明 |
|---|---|---|
| `speed` | Number, deg/s | 回転速度 |

#### `run_time(speed, time, then=Stop.HOLD, wait=True)`

指定時間だけ指定速度で回転します。

| 引数 | 型 | 説明 |
|---|---|---|
| `speed` | Number, deg/s | 回転速度 |
| `time` | Number, ms | 動作時間 |
| `then` | Stop | 停止後の動作（デフォルト: `Stop.HOLD`） |
| `wait` | bool | `True` で完了まで待機 |

#### `run_angle(speed, rotation_angle, then=Stop.HOLD, wait=True)`

指定角度だけ回転します。角度が負の場合は逆方向に動きます。

| 引数 | 型 | 説明 |
|---|---|---|
| `speed` | Number, deg/s | 回転速度 |
| `rotation_angle` | Number, deg | 回転する角度（正: 正方向、負: 逆方向） |
| `then` | Stop | 停止後の動作 |
| `wait` | bool | `True` で完了まで待機 |

#### `run_target(speed, target_angle, then=Stop.HOLD, wait=True)`

目標角度まで回転します。方向は自動的に選択されます。

| 引数 | 型 | 説明 |
|---|---|---|
| `speed` | Number, deg/s | 回転速度（正負どちらでも可） |
| `target_angle` | Number, deg | 目標の絶対角度 |
| `then` | Stop | 停止後の動作 |
| `wait` | bool | `True` で完了まで待機 |

#### `run_until_stalled(speed, then=Stop.COAST, duty_limit=None) -> int: deg`

ストールするまで回転し、停止した角度を返します。機構の端を検出するのに便利です。

| 引数 | 型 | 説明 |
|---|---|---|
| `speed` | Number, deg/s | 回転速度 |
| `then` | Stop | 停止後の動作（デフォルト: `Stop.COAST`） |
| `duty_limit` | Number, % | この操作中のデューティサイクル上限（`None` で変更なし） |

**戻り値:** ストールした角度（度）

#### `track_target(target_angle)`

目標角度を追いかけます。`run_target` と異なり、加速処理なしで即時に動きます。連続的に目標角度を変化させる場合に適しています。

| 引数 | 型 | 説明 |
|---|---|---|
| `target_angle` | Number, deg | 追いかける目標角度 |

#### `hold()`

モーターを停止し、現在角度を PID 制御でホールドします。

#### `stop()`

モーターを停止し、自由回転させます。（`DCMotor.stop()` と同じ）

#### `brake()`

受動的にブレーキをかけます。（`DCMotor.brake()` と同じ）

#### `reset_angle(angle)`

角度カウンターを指定値にリセットします。

| 引数 | 型 | 説明 |
|---|---|---|
| `angle` | Number, deg | 設定する角度値（`pupdevices.Motor` では `None` で絶対値にリセット） |

#### `close()`

モーターオブジェクトを閉じます。再度 `Motor()` で初期化できるようになります。ギア比を変更するなど、高度な用途向け。

**使用例**

```python
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Stop

motor = Motor(Port.A)

# ギアトレインを考慮した初期化（12T → 36T のギア）
motor_with_gear = Motor(Port.B, gears=[12, 36])

# 時間指定で回転（2秒後にホールド）
motor.run_time(300, 2000, then=Stop.HOLD)

# 角度指定で回転（360度後に自由停止）
motor.run_angle(500, 360, then=Stop.COAST)

# 目標角度に移動して待機
motor.run_target(400, 0)

# ストールするまで押し込んで限界点を取得
end_angle = motor.run_until_stalled(100, duty_limit=30)
print("限界角度:", end_angle)

# 非同期で複数のモーターを同時制御
from pybricks.tools import multitask, run_task

motor_a = Motor(Port.A)
motor_b = Motor(Port.B)

async def main():
    await multitask(
        motor_a.run_angle(500, 360),
        motor_b.run_angle(500, -360),
    )

run_task(main())
```

---

## Control — PID コントローラー設定

```python
motor.control.limits(speed, acceleration, torque)
motor.control.pid(kp, ki, kd, ...)
motor.control.target_tolerances(speed, position)
motor.control.stall_tolerances(speed, time)
```

モーターの PID コントローラーを細かく設定するためのクラスです。`motor.control` 属性としてアクセスします。通常のプログラムでは `limits()` 程度で十分です。

### 属性

| 属性 | 型 | 説明 |
|---|---|---|
| `control.scale` | int | 制御変数と物理出力のスケーリング係数（エンコーダパルス数/度） |

### `limits(speed, acceleration, torque)` / `limits() -> Tuple[int, int, int]`

最大速度・加速度・トルクを設定します。引数なしで現在値を返します。

| 引数 | 型 | 説明 |
|---|---|---|
| `speed` | Number, deg/s | 最大速度。すべての速度コマンドはこの値で制限される |
| `acceleration` | Number, deg/s² | 加速・減速のスロープ。タプルで加速と減速を個別設定可 |
| `torque` | torque | 制御中の最大フィードバックトルク |

### `pid(kp, ki, kd, integral_deadzone, integral_rate)` / `pid() -> Tuple`

PID ゲインを設定します。引数なしで現在値を返します。

| 引数 | 型 | 説明 |
|---|---|---|
| `kp` | int | 比例ゲイン（µNm/deg） |
| `ki` | int | 積分ゲイン（µNm/(deg·s)） |
| `kd` | int | 微分ゲイン（µNm/(deg/s)） |
| `integral_deadzone` | Number | 積分が蓄積しない誤差範囲 |
| `integral_rate` | Number | 積分の最大増加率 |

### `target_tolerances(speed, position)` / `target_tolerances() -> Tuple[int, int]`

動作完了とみなすための許容誤差を設定します。

| 引数 | 型 | 説明 |
|---|---|---|
| `speed` | Number, deg/s | 停止とみなす最大速度誤差 |
| `position` | Number, deg | 目標到達とみなす最大位置誤差 |

### `stall_tolerances(speed, time)` / `stall_tolerances() -> Tuple[int, int]`

ストール検出の閾値を設定します。

| 引数 | 型 | 説明 |
|---|---|---|
| `speed` | Number, deg/s | この速度以下で `time` 経過するとストールと判定 |
| `time` | Number, ms | ストール判定のための持続時間 |

**使用例**

```python
from pybricks.pupdevices import Motor
from pybricks.parameters import Port

motor = Motor(Port.A)

# 最大速度を 600 deg/s、加速度を 1200 deg/s² に設定
motor.control.limits(speed=600, acceleration=1200)

# 現在の設定を確認
speed, accel, torque = motor.control.limits()
print(speed, accel, torque)

# PID ゲインを調整
motor.control.pid(kp=800, ki=10, kd=5, integral_deadzone=5, integral_rate=100)
```

---

## Model — モーター状態オブザーバー

モーターの物理モデルを使って、角度・速度・電流・ストール状態を推定します。実測値よりも高い更新レートで利用できます。`motor.model` 属性としてアクセスします。

通常のプログラムでは使用しません。独自の PID コントローラーを実装する上級者向けです。

### `state() -> Tuple[float, float, float, bool]`

推定値を返します。

**戻り値:** `(推定角度 [deg], 推定速度 [deg/s], 推定電流 [mA], ストール状態 [bool])` のタプル
