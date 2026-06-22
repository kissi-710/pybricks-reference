# 走行ロボットテンプレート（drivebase/）

## 概要

2 つのモーターで動く差動駆動ロボット（`pybricks.robotics.DriveBase`）の
テンプレート集です。距離・角度を指定した正確な走行から、センサーを使った
自律走行（ライントレース・障害物回避）、ジャイロによる精密走行まで扱います。

## テンプレート一覧

| ファイル | 説明 | 主な用途 |
|---|---|---|
| [01_basic_drive.py](01_basic_drive.py) | 基本走行（straight / turn / arc / settings） | 決まった経路の走行 |
| [02_continuous_drive.py](02_continuous_drive.py) | 連続走行（drive）とボタン操作 | リアルタイム操縦・走行量取得 |
| [03_line_follower.py](03_line_follower.py) | ライントレース（カラーセンサー＋P制御） | 黒線に沿った自律走行 |
| [04_obstacle_avoidance.py](04_obstacle_avoidance.py) | 障害物回避（超音波センサー） | 衝突を避ける自律走行 |
| [05_gyro_drive.py](05_gyro_drive.py) | ジャイロを使った精密走行（use_gyro） | 正確な直進・旋回 |

## DriveBase の主なメソッド

| メソッド | 説明 |
|---|---|
| `straight(distance)` | 指定距離 (mm) 直進 |
| `turn(angle)` | その場で指定角度 (deg) 旋回 |
| `arc(radius, angle=...)` | 円弧を描いて走行 |
| `drive(speed, turn_rate)` | 連続走行（mm/s, deg/s、ノンブロッキング） |
| `stop()` / `brake()` / `hold()` | 停止 |
| `distance()` / `angle()` | 走行距離・角度の取得 |
| `reset()` | 走行量カウンターのリセット |
| `settings(...)` | 走行速度・加速度の設定 |
| `use_gyro(True)` | ジャイロ補正の有効化 |

## 座標の規約

- **直進:** 正 = 前進 / 負 = 後退
- **旋回:** 正 = 右回り（時計回り）/ 負 = 左回り

## セットアップのポイント

```python
# 車輪直径と車軸間距離を実測して設定する（mm 単位）
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=112)
```

- `wheel_diameter`: 車輪の直径。標準 SPIKE ホイールは 56mm
- `axle_track`: 左右の車輪が接地する点の間隔
- 左右のモーターは取り付け向きが逆になるため、`positive_direction` で揃えます
