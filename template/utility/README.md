# ユーティリティテンプレート（utility/）

## 概要

`pybricks.tools` モジュールが提供する、プログラム全般で役立つ
ユーティリティ機能のテンプレート集です。待機・時間計測・並行処理・
メニュー表示・データ記録を扱います。

## テンプレート一覧

| ファイル | 説明 | 主な用途 |
|---|---|---|
| [01_wait.py](01_wait.py) | wait による待機 | 一定間隔の処理・カウントダウン |
| [02_stopwatch.py](02_stopwatch.py) | StopWatch による時間計測 | 経過時間測定・反応速度ゲーム |
| [03_multitask.py](03_multitask.py) | multitask による並行処理 | 複数動作を同時実行 |
| [04_hub_menu.py](04_hub_menu.py) | hub_menu によるメニュー選択 | 複数プログラムの切り替え |
| [05_datalog.py](05_datalog.py) | DataLog によるデータ記録 | センサー・モーター値の記録 |

## 主な関数・クラス

| 名前 | 説明 |
|---|---|
| `wait(time)` | 指定ミリ秒だけプログラムを一時停止 |
| `StopWatch()` | 経過時間を計測（`time()` / `pause()` / `resume()` / `reset()`） |
| `multitask(*coroutines)` | 複数のコルーチンを並行実行 |
| `run_task(coroutine)` | メインのコルーチンを起動 |
| `hub_menu(*symbols)` | ディスプレイにメニューを表示し選択結果を返す |
| `DataLog(*headers)` | データを時系列で記録（`log(...)`） |

## 補足

- **wait と multitask の違い:** `wait` はプログラム全体を止めますが、
  `multitask` を使うと「待っている間に別の処理を進める」ことができます。
  モーターを回しながらライトを点滅させたい、といった場合は `multitask` が便利です。

- **DataLog の出力先:** SPIKE Prime ではファイル保存の代わりに、記録した内容が
  プログラム実行中の出力ウィンドウ（コンソール）に表示されます。

- **async / await:** `multitask` を使うテンプレートでは、時間のかかる処理
  （`wait` やモーターの `run_angle` など）を `await` で呼び出します。
