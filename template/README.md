# SPIKE Prime コードテンプレート集

LEGO® Education SPIKE Prime を pybricks で動かすための、実用的なコードテンプレート集です。
各テンプレートは日本語コメント付きで、そのままコピーして使えるレベルを目指しています。

## 対象環境

- **ハブ:** LEGO® SPIKE Prime Hub（`PrimeHub`）
- **ライブラリ:** pybricks
- **ポート:** A〜F（モーター・センサー兼用）

## ジャンル一覧

| ジャンル | フォルダ | 内容 |
|---|---|---|
| ハブ操作 | [hub/](hub/) | ボタン・ライト・5×5 ディスプレイ・スピーカー・IMU・バッテリー・システム |
| モーター制御 | [motor/](motor/) | 基本動作・停止方法・状態取得・ストール検出・設定・複数同期 |
| センサー | [sensor/](sensor/) | カラー・超音波・フォースの各センサー |
| 走行ロボット | [drivebase/](drivebase/) | 基本走行・連続走行・ライントレース・障害物回避・ジャイロ走行 |
| リモコン操作 | [remote/](remote/) | Powered Up リモコンでのモーター／ロボット操縦 |
| ハブ間通信 | [communication/](communication/) | BLERadio によるブロードキャスト送受信・双方向通信 |
| ユーティリティ | [utility/](utility/) | wait・StopWatch・multitask・hub_menu・DataLog |
| Raspberry Pi 連携 | [raspi/](raspi/) | stdin/stdout(BLE)を使ったホストPCからのRun/Pause制御・待ち受け、Camera Module V2による物体検出との統合 |

## 使い方

1. 使いたいテンプレートの `.py` ファイルを開く
2. ファイル冒頭のコメントで内容と前提を確認する
3. ポート番号・車輪サイズなど、自分のロボットに合わせて値を調整する
4. Pybricks Code（または対応 IDE）に貼り付けてハブにダウンロード・実行する

## 共通の注意点

- **ポート設定:** テンプレート内のポート（例: `Port.A`）は実際の接続に合わせて変更してください。
- **DriveBase のサイズ:** `wheel_diameter`（車輪直径）と `axle_track`（左右車輪間隔）は mm 単位で正確に測って設定すると、走行精度が上がります。標準の SPIKE ホイールは直径 56mm です。
- **IMU/ジャイロ:** プログラム開始直後はハブを数秒静止させると、IMU のキャリブレーションが安定します。
- **非同期処理:** `multitask` を使うテンプレートは `run_task(main())` でコルーチンを起動します。

## 参照ドキュメント

各 API の詳細は、プロジェクトルートの [docs/](../docs/) 以下を参照してください。
