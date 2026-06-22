# pybricks.nxtdevices — NXT デバイス

## 概要

`pybricks.nxtdevices` モジュールは、LEGO® MINDSTORMS® NXT のセンサーを EV3 Brick で使用するためのクラスを提供します。

```python
from pybricks.nxtdevices import (
    TouchSensor, LightSensor, ColorSensor, UltrasonicSensor,
    SoundSensor, TemperatureSensor, EnergyMeter, VernierAdapter
)
from pybricks.parameters import Port
```

---

## TouchSensor — NXT タッチセンサー

```python
from pybricks.nxtdevices import TouchSensor
from pybricks.parameters import Port

sensor = TouchSensor(Port.S1)
```

### メソッド

#### `pressed() -> bool`

ボタンが押されているか確認します。

**戻り値:** `True` なら押されている

**使用例**

```python
while not sensor.pressed():
    pass
print("押された")
```

---

## LightSensor — NXT 光センサー

```python
from pybricks.nxtdevices import LightSensor
from pybricks.parameters import Port

sensor = LightSensor(Port.S2)
```

### メソッド

#### `ambient() -> int: %`

周囲光の強度を計測します。

**戻り値:** 0〜100 %

#### `reflection() -> int: %`

赤色光の反射量を計測します。

**戻り値:** 0〜100 %

**使用例**

```python
from pybricks.nxtdevices import LightSensor
from pybricks.parameters import Port

sensor = LightSensor(Port.S2)

ref = sensor.reflection()   # ライントレースに活用
amb = sensor.ambient()      # 周囲の明るさ
```

---

## ColorSensor — NXT カラーセンサー

```python
from pybricks.nxtdevices import ColorSensor
from pybricks.parameters import Port

sensor = ColorSensor(Port.S3)
```

`CommonColorSensor` を継承しており、色の検出・HSV・反射・環境光が使用できます。また、センサー前面のライトを制御できます。

### 属性

| 属性 | クラス |
|---|---|
| `sensor.light` | `ColorLight` |

### 継承メソッド（CommonColorSensor より）

| メソッド | 説明 |
|---|---|
| `color()` | 色を検出（`Color.RED` 等） |
| `hsv()` | HSV 値で色を取得 |
| `ambient()` | 環境光の強度 (%) |
| `reflection()` | 反射光の強度 (%) |
| `detectable_colors(colors)` | 検出対象の色リストを設定 |

### 追加メソッド

#### `rgb() -> Tuple[int, int, int]`

赤・緑・青の反射量を順番に計測して返します。

**戻り値:** `(red, green, blue)` のタプル（各 0〜100 %）

**使用例**

```python
from pybricks.nxtdevices import ColorSensor
from pybricks.parameters import Port, Color

sensor = ColorSensor(Port.S3)

c = sensor.color()
r, g, b = sensor.rgb()

sensor.light.on(Color.RED)   # センサーライトを赤に
sensor.light.off()
```

---

## UltrasonicSensor — NXT 超音波センサー

```python
from pybricks.nxtdevices import UltrasonicSensor
from pybricks.parameters import Port

sensor = UltrasonicSensor(Port.S4)
```

### メソッド

#### `distance() -> int: mm`

物体までの距離を返します。

**使用例**

```python
dist = sensor.distance()
print(f"距離: {dist} mm")
```

---

## SoundSensor — NXT サウンドセンサー

```python
from pybricks.nxtdevices import SoundSensor
from pybricks.parameters import Port

sensor = SoundSensor(Port.S1)
```

### メソッド

#### `intensity(audible_only=True) -> int: %`

周囲の音の強度（ラウドネス）を計測します。

| 引数 | 型 | 説明 |
|---|---|---|
| `audible_only` | bool | `True`: 人の耳で聞こえる周波数のみ検出 |

**戻り値:** 音の強度（0〜100 %）

**使用例**

```python
from pybricks.nxtdevices import SoundSensor
from pybricks.parameters import Port

sensor = SoundSensor(Port.S1)

loudness = sensor.intensity()
if loudness > 70:
    print("うるさい！")
```

---

## TemperatureSensor — NXT 温度センサー

```python
from pybricks.nxtdevices import TemperatureSensor
from pybricks.parameters import Port

sensor = TemperatureSensor(Port.S2)
```

### メソッド

#### `temperature() -> float: °C`

温度を摂氏（℃）で返します。

**使用例**

```python
temp = sensor.temperature()
print(f"温度: {temp:.1f} ℃")
```

---

## EnergyMeter — NXT エネルギーメーター

```python
from pybricks.nxtdevices import EnergyMeter
from pybricks.parameters import Port

meter = EnergyMeter(Port.S1)
```

LEGO® Education の NXT エネルギーメーターで、入力・出力の電気信号とバッテリー残量を計測します。

### メソッド

#### `storage() -> int: J`

バッテリーに蓄積されたエネルギーを返します。

**戻り値:** 残量（ジュール）

#### `input() -> Tuple[int, int, int]`

入力側（下部）の電気信号を計測します。

**戻り値:** `(電圧 mV, 電流 mA, 電力 mW)` のタプル

#### `output() -> Tuple[int, int, int]`

出力側（上部）の電気信号を計測します。

**戻り値:** `(電圧 mV, 電流 mA, 電力 mW)` のタプル

**使用例**

```python
from pybricks.nxtdevices import EnergyMeter
from pybricks.parameters import Port

meter = EnergyMeter(Port.S1)

stored = meter.storage()
v_in, i_in, p_in = meter.input()
v_out, i_out, p_out = meter.output()

print(f"蓄積エネルギー: {stored} J")
print(f"入力: {v_in} mV, {i_in} mA, {p_in} mW")
```

---

## VernierAdapter — Vernier センサーアダプター

```python
from pybricks.nxtdevices import VernierAdapter
from pybricks.parameters import Port

adapter = VernierAdapter(Port.S1)
```

NXT/EV3 用の Vernier センサーアダプター。アナログ電圧を計測し、変換関数で物理量に換算します。

### コンストラクタ

```python
VernierAdapter(port, conversion=None)
```

| 引数 | 型 | 説明 |
|---|---|---|
| `port` | Port | 接続ポート |
| `conversion` | callable | 電圧 (mV) を物理量に変換する関数（省略可） |

### メソッド

#### `voltage() -> int: mV`

生のアナログ電圧を返します。

#### `conversion(voltage) -> float`

電圧を物理量に変換します（`conversion` 引数で関数を渡した場合のみ）。

#### `value() -> float`

`voltage()` を計測し、`conversion()` を適用して返します。

**使用例**

```python
from pybricks.nxtdevices import VernierAdapter
from pybricks.parameters import Port

# 表面温度センサー用の変換式
def surface_temp(voltage):
    return (voltage / 1000.0 - 0.75) / 0.01 + 25.0

adapter = VernierAdapter(Port.S1, conversion=surface_temp)

temp = adapter.value()   # 変換後の温度 (℃)
raw = adapter.voltage()  # 生の電圧 (mV)
```
