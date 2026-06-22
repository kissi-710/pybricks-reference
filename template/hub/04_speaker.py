"""
SPIKE Prime ハブ操作テンプレート: スピーカー
=================================================

ハブ内蔵スピーカーで音を鳴らす方法を示します。
- 音量設定
- ビープ音（周波数・長さ指定）
- 音符シーケンスの演奏（簡単なメロディ）
"""

from pybricks.hubs import PrimeHub
from pybricks.tools import wait

hub = PrimeHub()

# --- 1. 音量を設定（0〜100%）---
hub.speaker.volume(80)

# --- 2. ビープ音を鳴らす ---
# beep(周波数Hz, 長さms)
hub.speaker.beep(frequency=440, duration=300)  # ラ(A4)
wait(200)
hub.speaker.beep(frequency=523, duration=300)  # ド(C5)
wait(200)

# 音階を上がっていく
for freq in [262, 294, 330, 349, 392, 440, 494, 523]:
    hub.speaker.beep(frequency=freq, duration=150)

wait(500)

# --- 3. 音符シーケンスで演奏 ---
# 音符の書式: "<音名><オクターブ>/<長さ>"
#   音名: A〜G、休符は R、シャープは # フラットは b
#   長さ: 4=4分音符, 8=8分音符, 2=2分音符 ...
#   付点は . （例: "C4/4."）、タイ/スラーは _ で次の音とつなぐ
# tempo: 1 分あたりの拍数 (BPM)。4 分音符 = 1 拍
hub.speaker.play_notes(
    ["E4/4", "E4/4", "F4/4", "G4/4", "G4/4", "F4/4", "E4/4", "D4/4", "C4/2"],
    tempo=120,
)

print("スピーカーデモ終了")
