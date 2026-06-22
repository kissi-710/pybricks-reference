"""
SPIKE Prime モーター制御テンプレート: 複数モーターの同期制御
=================================================

複数のモーターを同時に動かす方法を示します。
- 逐次実行（wait=False で待たずに次へ）
- multitask による並行実行（複数の run_angle を同時に完了待ち）

multitask を使うと「両方のモーターが回り終わるまで待つ」が簡潔に書けます。
"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.tools import wait, multitask, run_task

hub = PrimeHub()

# 2 つのモーターを初期化（左右で逆向きに取り付ける想定）
motor_a = Motor(Port.A, positive_direction=Direction.CLOCKWISE)
motor_b = Motor(Port.B, positive_direction=Direction.COUNTERCLOCKWISE)

# --- 方法 1: wait=False で同時スタート（逐次） ---
# 1 つ目を「待たずに」開始し、2 つ目も開始することで同時に動かす
print("方法1: wait=False で同時に回す")
motor_a.run_angle(500, 360, wait=False)  # 待たずに次へ
motor_b.run_angle(500, 360, wait=True)   # こちらは完了まで待つ
wait(500)


# --- 方法 2: multitask で並行実行（推奨） ---
# 複数の非同期動作をまとめ、すべて完了するまで待つ
async def main():
    print("方法2: multitask で 2 つを並行実行し、両方の完了を待つ")
    await multitask(
        motor_a.run_angle(500, 720),
        motor_b.run_angle(300, 720),   # 速度が違っても両方の完了を待つ
    )
    print("両方のモーターが回り終わりました")

    # 続けて別の動作も並行で
    await multitask(
        motor_a.run_target(400, 0),
        motor_b.run_target(400, 0),
    )
    print("両方とも 0 度へ戻りました")


run_task(main())
print("複数モーターデモ終了")
