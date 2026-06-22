# ハブ操作テンプレート（hub/）

## 概要

SPIKE Prime Hub（`PrimeHub`）本体の各機能を操作するテンプレート集です。
ボタン入力、ステータスライト、5×5 LED ディスプレイ、スピーカー、IMU（ジャイロ）、
バッテリー、システム制御の基本的な使い方を網羅しています。

## テンプレート一覧

| ファイル | 説明 | 主な用途 |
|---|---|---|
| [01_buttons.py](01_buttons.py) | ハブのボタン入力（LEFT/CENTER/RIGHT/BLUETOOTH）の検出 | ボタン待ち・分岐・同時押し判定 |
| [02_light.py](02_light.py) | 中央ステータスライトの制御（点灯・点滅・アニメーション） | 状態表示・視覚的フィードバック |
| [03_display.py](03_display.py) | 5×5 LED ディスプレイ（数字・文字・アイコン・ピクセル） | 情報表示・アイコン演出 |
| [04_speaker.py](04_speaker.py) | スピーカー（ビープ音・メロディ演奏） | 音による通知・効果音 |
| [05_imu.py](05_imu.py) | IMU（傾き・方位・加速度・静止判定） | 姿勢検出・方位計測 |
| [06_battery.py](06_battery.py) | バッテリー電圧・電流・充電状態の取得 | 残量チェック・充電監視 |
| [07_system.py](07_system.py) | システム情報・永続ストレージ・シャットダウン | 設定保存・起動回数記録・終了処理 |

## 使用するクラス・属性

- `PrimeHub.buttons` — `Keypad`（`pressed()`）
- `PrimeHub.light` — `ColorLight`（`on()` / `off()` / `blink()` / `animate()`）
- `PrimeHub.display` — `LightMatrix`（`number()` / `char()` / `text()` / `icon()` / `pixel()`）
- `PrimeHub.speaker` — `Speaker`（`beep()` / `play_notes()` / `volume()`）
- `PrimeHub.imu` — `IMU`（`heading()` / `tilt()` / `up()` / `acceleration()` / `ready()`）
- `PrimeHub.battery` — `Battery`（`voltage()` / `current()`）
- `PrimeHub.charger` — `Charger`（`connected()` / `status()`）
- `PrimeHub.system` — `System`（`info()` / `storage()` / `shutdown()`）
