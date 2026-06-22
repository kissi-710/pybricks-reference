"""
SPIKE Prime ハブ操作テンプレート: バッテリーと充電状態
=================================================

バッテリーの電圧・電流、および USB 充電器の状態を取得する方法を示します。
- バッテリー電圧 (mV) / 電流 (mA)
- 充電器の接続・充電ステータス
- 電圧に応じたディスプレイ表示
"""

from pybricks.hubs import PrimeHub
from pybricks.parameters import Color
from pybricks.tools import wait

hub = PrimeHub()

# --- 1. バッテリー情報を取得 ---
voltage = hub.battery.voltage()   # ミリボルト (mV)
current = hub.battery.current()   # ミリアンペア (mA)

print("バッテリー電圧:", voltage, "mV")
print("バッテリー電流:", current, "mA")

# --- 2. 電圧から残量の目安を判定して色表示 ---
# SPIKE Prime は約 6000mV(空)〜8300mV(満充電) が目安
if voltage >= 7500:
    hub.light.on(Color.GREEN)    # 十分
    level = "高"
elif voltage >= 7000:
    hub.light.on(Color.YELLOW)   # やや低下
    level = "中"
else:
    hub.light.on(Color.RED)      # 充電推奨
    level = "低"

print("残量レベル:", level)

# --- 3. 充電器の状態を取得 ---
# status() の戻り値: 0=充電なし, 1=充電中, 2=完了, 3=異常
status = hub.charger.status()
status_text = {0: "充電なし", 1: "充電中", 2: "充電完了", 3: "異常"}

print("充電器接続:", hub.charger.connected())
print("充電ステータス:", status_text.get(status, "不明"))

# ディスプレイに残量レベルの頭文字を表示
hub.display.char(level)

wait(5000)
hub.light.off()
hub.display.off()
print("バッテリーデモ終了")
