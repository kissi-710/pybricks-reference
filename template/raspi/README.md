# Raspberry Pi 連携テンプレート（raspi/）

## 概要

Raspberry Pi（または任意のPC）から BLE 経由で SPIKE Prime ハブを外部制御する
テンプレート集です。画像認識などホスト側の判断に応じて、ハブ側のプログラムを
止めずに「今すぐ一時停止／再開」といった指示をリアルタイムに送る用途を想定しています。

あわせて、Raspberry Pi に Camera Module V2 を載せて画像認識を行い、その結果を
そのままハブへの Run/Pause 指示に変換するテンプレートも含みます。厳密には
「pybricks（ハブ側）のリファレンス」の範囲を超えますが、ラズパイを載せて
自律動作させる以上ほぼ必須になる処理のため、このフォルダにまとめています。

## テンプレート一覧

| ファイル | 実行場所 | 説明 |
|---|---|---|
| [01_hub_command_listener.py](01_hub_command_listener.py) | **ハブ側** | stdin を非ブロッキングで監視し、RUN/PAUSE/STOP コマンドで動作を切り替える |
| [02_raspi_ble_controller.py](02_raspi_ble_controller.py) | **Raspberry Pi 側** | bleak を使ってハブに接続し、コマンド文字列を送信する |
| [03_camera_object_detection.py](03_camera_object_detection.py) | **Raspberry Pi 側** | Camera Module V2 の映像から特定色の物体を検出する（検出ロジック単体の動作確認用） |
| [04_camera_to_hub_control.py](04_camera_to_hub_control.py) | **Raspberry Pi 側** | 03 の検出結果に応じて、02 と同様の仕組みでハブに PAUSE/RUN を自動送信する統合版 |

`01_` は pybricks プログラムとしてハブに書き込むファイル、`02_`〜`04_` は Raspberry Pi 上で
`python3` で実行する通常の Python スクリプトです。ライブラリが異なる点に注意してください。

## なぜ BLERadio や break（Ctrl+C）を使わないのか

- **`pybricks.messaging.BLERadio`** は SPIKE Prime **ハブ同士**の通信専用です。
  ホストPC（Raspberry Pi等）とハブの間の通信には使えません。
- **break（Ctrl+C, `0x03`）** はプログラム自体を強制終了させる信号です。
  一時停止・再開のような「動作を止めずに制御し続けたい」用途には向きません。
  プログラムが終了するとモーター制御なども失われ、再開できなくなります。

代わりに、Pybricks ファームウェアが標準で提供している **stdin/stdout 通信**
（Pybricks Command/Event Characteristic 経由）を使います。これはハブと外部ホストの
間で汎用的にテキストやバイト列をやり取りするための仕組みです。

## 通信の仕組み

```
Raspberry Pi (bleak)                     SPIKE Prime Hub (pybricks)
      │                                          │
      │  0x06 + "PAUSE\n" を書き込み              │
      │ ───────────────────────────────────────▶ │  stdin.buffer.readline()
      │                                          │  → motor.hold()
      │                                          │
      │            "OK:PAUSE\n" を通知            │
      │ ◀─────────────────────────────────────── │  stdout.buffer.write()
```

- Raspberry Pi → ハブ: `Pybricks Command/Event Characteristic`
  （UUID: `c5f50002-8280-46da-89f4-6d8051e4aeef`）に対して
  `0x06`（write stdin コマンド）+ 送信したい文字列 を書き込む
- ハブ → Raspberry Pi: 同じ Characteristic の通知（`0x01` = write stdout イベント）
  としてハブからの応答を受け取る

## カメラでの物体検出について（03 / 04）

`picamera2`（libcamera ベースの公式カメラライブラリ）で映像を取得し、
`OpenCV` で HSV 色空間による色検出を行う、という軽量な方式にしています。
機械学習ベースの物体認識ではなく、あくまで「特定の色が視界に入ったかどうか」
を判定するシンプルな方法です。理由は次のとおりです。

- Raspberry Pi 上でも十分な速度でリアルタイムに動く
- 「赤いブロックが見えたら止まる」のような単純な用途には過不足がない
- 依存ライブラリが少なく、セットアップがしやすい

より高度な認識（形状判定・複数物体・機械学習モデルなど）が必要な場合は、
`detect_object()` 関数の中身だけを差し替えれば、BLE 送信部分（04）はそのまま
流用できます。

### 検出色のチューニング

デフォルトは赤色を検出する設定になっています。他の色を検出したい場合は、
`03_camera_object_detection.py` / `04_camera_to_hub_control.py` 内の
`LOWER_RED_*` / `UPPER_RED_*`（HSV範囲）と `MIN_AREA`（検出とみなす最小面積）
を実際の照明環境に合わせて調整してください。

## セットアップ手順（Raspberry Pi 側）

Raspberry Pi OS（Bookworm以降）には Bluetooth スタック（BlueZ）が標準で
インストール済みですが、Python から BLE を扱うにはいくつか準備が必要です。
初回のみ、以下を順に行ってください。

### 0.（社内ネットワーク等でプロキシが必要な場合）プロキシの設定

BLE通信自体（Raspberry Pi ⇔ ハブ）はネットワークプロキシを経由しないため
影響を受けませんが、これから行う `apt update` / `apt install` / `pip install`
はインターネットアクセスを伴うため、社内プロキシ配下の場合は事前に
プロキシを設定しておく必要があります。プロキシのURL・認証情報は環境ごとに
異なるため、ここでは伏せてプレースホルダで記載します。実際の値に置き換えて
ください。

**環境変数（シェル・pip・多くのCLIツールで共通）**

```bash
export http_proxy="http://<proxy-host>:<proxy-port>/"
export https_proxy="http://<proxy-host>:<proxy-port>/"
export no_proxy="localhost,127.0.0.1"
```

認証が必要なプロキシの場合は `http://<user>:<password>@<proxy-host>:<proxy-port>/`
の形式で指定します（パスワードに `@` や `:` を含む場合は URL エンコードが必要です）。

毎回入力するのが手間な場合は `~/.bashrc` の末尾に追記して永続化できます。

```bash
echo 'export http_proxy="http://<proxy-host>:<proxy-port>/"'  >> ~/.bashrc
echo 'export https_proxy="http://<proxy-host>:<proxy-port>/"' >> ~/.bashrc
echo 'export no_proxy="localhost,127.0.0.1"'                  >> ~/.bashrc
source ~/.bashrc
```

**apt用の設定**（`sudo` 実行時は環境変数が引き継がれないため、apt には別途
設定ファイルで教える必要があります）

```bash
sudo tee /etc/apt/apt.conf.d/95proxies > /dev/null <<'EOF'
Acquire::http::Proxy "http://<proxy-host>:<proxy-port>/";
Acquire::https::Proxy "http://<proxy-host>:<proxy-port>/";
EOF
```

**pip用の設定**（環境変数で足りる場合が多いですが、恒久化したい場合）

```bash
mkdir -p ~/.pip
cat > ~/.pip/pip.conf <<'EOF'
[global]
proxy = http://<proxy-host>:<proxy-port>/
EOF
```

もしくは、都度コマンドに `--proxy` オプションを付ける方法でも構いません。

```bash
pip install --proxy http://<proxy-host>:<proxy-port>/ bleak
```

プロキシ設定後、`curl -I https://pypi.org` や `sudo apt update` が正常に
通ることを確認してから、以降の手順に進んでください。

### 1. Bluetooth サービスが動いているか確認

```bash
sudo systemctl status bluetooth
```

`active (running)` になっていなければ起動します。

```bash
sudo systemctl enable --now bluetooth
```

BlueZ 自体が入っていない・古い場合は更新します（`bleak` は BlueZ 5.43 以上が必要）。

```bash
sudo apt update
sudo apt install --only-upgrade bluez
bluetoothctl --version
```

### 2. bluetooth グループに自分のユーザーを追加（推奨）

`bleak` は BlueZ に D-Bus 経由でアクセスするため **root 権限は基本的に不要**ですが、
環境によっては一般ユーザーのままだと D-Bus のアクセス許可が下りない場合があるため、
念のため `bluetooth` グループに入れておくと安定します。

```bash
sudo usermod -aG bluetooth $USER
```

**反映させるには一度ログアウト（またはSSHを再接続）してください。**

### 3. Python 仮想環境の作成と bleak のインストール

Raspberry Pi OS Bookworm 以降は、システムの Python に直接 `pip install` すると
`externally-managed-environment` エラーで拒否されることがあります。仮想環境を
作るのが確実です。

```bash
python3 -m venv ~/spike-venv
source ~/spike-venv/bin/activate
pip install --upgrade pip
pip install bleak
```

以降、このテンプレートを実行するときは `source ~/spike-venv/bin/activate` で
仮想環境を有効化してから `python3 02_raspi_ble_controller.py` を実行してください。

（仮想環境を使わずシステム側に直接入れたい場合は `pip install bleak --break-system-packages` でも可能ですが、推奨はしません。）

### 4. 動作確認

```bash
bluetoothctl show
```

で Powered: yes になっていれば準備完了です。`hci0` が見つからない・Poweredがno の場合は次を試してください。

```bash
sudo hciconfig hci0 up
sudo rfkill unblock bluetooth
```

### 5.（03 / 04 のカメラテンプレートを使う場合のみ）picamera2 と OpenCV の導入

Camera Module V2 は Bookworm以降の Raspberry Pi OS では `libcamera` スタックで
制御します。専用ライブラリの `picamera2` は **pip ではなく apt でのインストールが
公式に推奨**されています（pip版はビルドに時間がかかり依存関係の問題も出やすいため）。
OpenCV も同様に apt 版が無難です。

```bash
sudo apt update
sudo apt install -y python3-picamera2 python3-opencv
```

これらは `venv` 環境の外（システム全体）にインストールされるため、手順3で
作った仮想環境から使うには、システムパッケージを引き継ぐオプション付きで
作り直してください。

```bash
python3 -m venv ~/spike-venv --system-site-packages
source ~/spike-venv/bin/activate
pip install bleak
```

（既に `--system-site-packages` なしで作成済みの場合は、上記のように
 作り直すか、venv を使わずシステム Python から直接実行しても構いません。）

カメラが認識されているかは、以下のコマンドで確認できます（プレビュー画像が
表示されずシェルに戻る場合は `--timeout` の間だけ静止画確認用ウィンドウが出ます）。

```bash
rpicam-hello --timeout 2000
```

エラーが出る場合は、リボンケーブルの向き・接触を確認し、以下も試してください。

```bash
sudo raspi-config   # Interface Options → Camera から有効化されているか確認
```

### まとめ（起動直後に毎回必要なこと）

- ハブ再起動のたびに追加インストールは不要です（一度セットアップすれば OK）。
- Raspberry Pi を再起動した場合、Bluetooth サービス・カメラドライバは自動で
  使える状態になりますが、仮想環境を使っている場合は
  `source ~/spike-venv/bin/activate` の実行だけ毎回必要です。

## 使い方の流れ

### BLE制御の基本動作を確認する場合（01 + 02）

1. 上記「セットアップ手順」の 1〜4 を実施
2. `01_hub_command_listener.py` を Pybricks Code でハブに書き込む
   （まだ実行しない）
3. `02_raspi_ble_controller.py` の `HUB_NAME` を自分のハブ名に合わせて修正
4. Raspberry Pi 側で仮想環境を有効化し、`02_raspi_ble_controller.py` を実行して
   スキャン・接続を待つ
5. 接続確立後、ハブのボタンで `01_hub_command_listener.py` を起動する
6. Raspberry Pi 側から `send_command("PAUSE")` / `send_command("RUN")` を呼び、
   ハブの動作をリアルタイムに制御する

### カメラ検出も含めて自律的に制御する場合（01 + 03 + 04）

1. 上記「セットアップ手順」の 1〜5 をすべて実施
2. `03_camera_object_detection.py` を単体で実行し、検出できているか確認
   （検出色や `MIN_AREA` を実際の照明・対象物に合わせて調整）
3. 調整した `LOWER_RED_*` / `UPPER_RED_*` / `MIN_AREA` の値を
   `04_camera_to_hub_control.py` 側にも反映する
4. `01_hub_command_listener.py` をハブに書き込む（まだ実行しない）
5. `04_camera_to_hub_control.py` の `HUB_NAME` を修正して実行し、
   ハブへの接続を待つ
6. ハブのボタンで `01_hub_command_listener.py` を起動する
7. 対象物がカメラに映る／消えるのに応じて、自動で PAUSE / RUN が送信される

## 注意点

- ハブに Pybricks Code など他のアプリが接続されていると、Raspberry Pi 側からは
  ハブを発見・接続できません。他のアプリは事前に切断してください。
- コマンドは改行区切り（`\n`）を前提にしているため、送信側は必ず末尾に改行を
  付けてください（`send_command()` 内で自動付与済み）。
- プログラムの書き込み・起動まで自動化したい場合は、Pybricks の両方の
  BLE Characteristic を実装済みの `pybricksdev` ライブラリの利用を検討してください
  （`pip install pybricksdev`）。
- 色検出（03/04）は照明条件の影響を受けやすいです。環境光が変わる場所で
  使う場合は、`MIN_AREA` を少し高めにする、HSV範囲を絞るなどして
  誤検出を減らしてください。
- `Picamera2` のインスタンスは同時に1つしか安定して使えません。他のスクリプトで
  カメラを使用中は `04_camera_to_hub_control.py` を実行しないでください。
- 04 は検出負荷が高い場合、BLE送信のタイミングが遅延することがあります。
  遅延が問題になる場合は解像度をさらに下げる（例: 320×240）か、
  検出間隔（`asyncio.sleep(0.05)` の値）を調整してください。
