# リモコン操作テンプレート（remote/）

## 概要

LEGO® Powered Up リモコン（ハンドセット）で SPIKE Prime のモーターや
走行ロボットを操作するテンプレート集です。`pybricks.pupdevices.Remote` を
使ってリモコンに Bluetooth 接続し、ボタン入力を受け取ります。

## テンプレート一覧

| ファイル | 説明 | 主な用途 |
|---|---|---|
| [01_remote_motor.py](01_remote_motor.py) | リモコンでモーターを正逆回転 | 単一モーターの遠隔操作 |
| [02_remote_drivebase.py](02_remote_drivebase.py) | リモコンで走行ロボットを操縦 | ラジコン風のロボット操作 |

## Remote クラスの使い方

```python
from pybricks.pupdevices import Remote

# リモコンに接続（name=None で最初に見つかったものに接続）
remote = Remote()

# ボタンの状態を取得
pressed = remote.buttons.pressed()

# リモコンの LED を制御
remote.light.on(Color.GREEN)
```

## リモコンのボタン

| ボタン | 定数 |
|---|---|
| 左側 上 | `Button.LEFT_PLUS` |
| 左側 中央 | `Button.LEFT` |
| 左側 下 | `Button.LEFT_MINUS` |
| 右側 上 | `Button.RIGHT_PLUS` |
| 右側 中央 | `Button.RIGHT` |
| 右側 下 | `Button.RIGHT_MINUS` |
| 中央（緑） | `Button.CENTER` |

## 接続のヒント

- プログラム実行前にリモコンの緑ボタンを押して電源を入れておきます。
- `Remote()` は接続できるまで待機します（デフォルトのタイムアウトは 10 秒）。
- 接続に失敗する場合は、リモコンが他のデバイスとペアリングされていないか確認してください。
