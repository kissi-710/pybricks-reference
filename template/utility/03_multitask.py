"""
SPIKE Prime ユーティリティテンプレート: multitask（並行処理）
=================================================

multitask と run_task を使うと、複数の処理を「同時に」進められます。
- async def で非同期関数（コルーチン）を定義
- 関数内では時間のかかる処理を await する
- multitask(...) に複数のコルーチンを渡すと並行実行
- run_task(...) でメインのコルーチンを起動

【例】モーターを回しながら、同時にライトを点滅させ、同時に音を鳴らす。
wait だけでは順番にしか実行できない処理を、同時並行で動かせます。
"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Color
from pybricks.tools import wait, multitask, run_task

hub = PrimeHub()
motor = Motor(Port.A)


# --- 各タスクを async def（コルーチン）で定義 ---

async def spin_motor():
    """モーターを行ったり来たりさせる"""
    for i in range(3):
        await motor.run_angle(500, 360)
        await motor.run_angle(500, -360)


async def blink_light():
    """ライトを点滅させ続ける"""
    for i in range(10):
        hub.light.on(Color.RED)
        await wait(300)
        hub.light.on(Color.BLUE)
        await wait(300)


async def play_sound():
    """ビープ音を鳴らす"""
    for freq in [440, 494, 523, 587, 659]:
        await hub.speaker.beep(frequency=freq, duration=400)
        await wait(200)


# --- メインのコルーチン ---
async def main():
    print("モーター・ライト・音を同時に実行します")
    # 3 つのタスクを並行実行し、すべて終わるまで待つ
    await multitask(spin_motor(), blink_light(), play_sound())
    print("すべてのタスクが完了しました")


# プログラムを起動
run_task(main())

hub.light.off()
print("multitask デモ終了")
