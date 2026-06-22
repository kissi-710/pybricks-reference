# モーター制御テンプレート（motor/）

## 概要

SPIKE Prime のモーター（`pybricks.pupdevices.Motor`）を制御するテンプレート集です。
基本的な回転コマンドから、停止方法の使い分け、状態の取得、ストール検出、
動作特性の設定、複数モーターの同期制御までを扱います。

## テンプレート一覧

| ファイル | 説明 | 主な用途 |
|---|---|---|
| [01_basic_run.py](01_basic_run.py) | 基本動作（run / run_time / run_angle / run_target） | モーターの基本的な回し方 |
| [02_stop_modes.py](02_stop_modes.py) | 停止方法（stop / brake / hold）と then 引数 | 用途に応じた停止の使い分け |
| [03_measure.py](03_measure.py) | 状態取得（angle / speed / load）とリセット | 角度・速度の監視 |
| [04_stall_detection.py](04_stall_detection.py) | ストール検出（run_until_stalled / stalled） | 機構の端を基準にする・詰まり検出 |
| [05_settings.py](05_settings.py) | 速度・加速度・トルクの設定（control.limits） | 動きの滑らかさ・俊敏さの調整 |
| [06_multiple_motors.py](06_multiple_motors.py) | 複数モーターの同期（wait=False / multitask） | 2 つ以上のモーターを同時制御 |

## 主なメソッド

| メソッド | 説明 |
|---|---|
| `run(speed)` | 指定速度で連続回転（ノンブロッキング） |
| `run_time(speed, time)` | 指定時間だけ回転 |
| `run_angle(speed, angle)` | 指定角度だけ回転 |
| `run_target(speed, angle)` | 目標の絶対角度まで回転 |
| `run_until_stalled(speed)` | ストールするまで回転し、角度を返す |
| `stop()` / `brake()` / `hold()` | 停止（自由回転 / ブレーキ / 保持） |
| `angle()` / `speed()` / `load()` | 状態取得 |
| `control.limits(...)` | 速度・加速度・トルクの上限設定 |

## 単位の確認

- 速度: **deg/s**（度/秒）
- 角度: **deg**（度）
- 負荷: **mNm**（ミリニュートンメートル）
