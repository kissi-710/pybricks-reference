"""
SPIKE Prime 走行ロボットテンプレート: 2センサー挟み込み型ライントレース（PID制御）
=================================================

白い床に引かれた黒線を、左右 2 つのカラーセンサーで「挟む」ように走る
ライントレースです。通常時は 2 つのセンサーがどちらも白の上にあり、
どちらかのセンサーが黒線に近づいたら、黒線から逃げる向きに旋回します。

【センサー配置（上から見た図）】

        進行方向 ↑
     [左S]  ┃  [右S]      ← 左右センサーの間に黒線が来る
            ┃
     (左輪) ┃ (右輪)

【仕組み】
  1. 左右の反射光を「黒=0 / 白=100」に正規化する（センサーの個体差を吸収）
  2. 誤差 error = 左の値 - 右の値
       - 両方白          → error ≒ 0   → 直進
       - 左が黒に近づく  → error < 0   → 左へ旋回（黒線を左右の中央へ戻す）
       - 右が黒に近づく  → error > 0   → 右へ旋回
  3. error を PID 制御にかけて旋回率 (deg/s) を決める
  4. |error| が大きいほど前進速度を落とす（自動減速）
  5. 左右とも黒（十字路）のときは PID を使わずまっすぐ通過する

【ファイル構成（どこに何があるか）】
  Config                 … 調整用の係数・閾値をまとめたクラス
  Devices                … ハブ・モーター・センサー・DriveBase をまとめたクラス
  PIDState               … PID 制御の内部状態（積分値・前回誤差）
  normalize()            … 反射光を 0〜100 に正規化
  read_sensors()         … 左右センサーの正規化値を取得
  is_crossroad()         … 十字路（黒, 黒）の判定
  calc_error()           … 左右の値から誤差を計算
  reset_pid()            … PID 状態のリセット
  calc_pid()             … PID 制御で旋回率を計算
  calc_speed()           … 誤差に応じた自動減速
  pass_crossroad()       … 十字路をまっすぐ通過
  trace_step()           … ライントレース 1 ステップ分の処理
  calibrate()            … 白・黒の反射光をボタン操作で測定（任意）
  wait_for_button()      … ボタン待ち
  debug_print()          … デバッグ表示
  main()                 … メインループ

【調整の手順（目安）】
  1. Config の LEFT/RIGHT の WHITE・BLACK を実測値に合わせる
     （または USE_CALIBRATION = True で起動時に測定）
  2. KI = KD = 0 にして KP を調整（蛇行し始める手前まで上げる）
  3. KD を少しずつ上げて蛇行を抑える
  4. 必要なら KI をごく小さく入れる（カーブで外側に膨らむ場合）
  5. SLOWDOWN_GAIN / MIN_SPEED で急カーブ時の減速量を調整
"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Port, Direction, Button
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch


# =================================================
# 設定
# =================================================

class Config:
    """調整用の係数・閾値をまとめたクラス。値を変えるときはここだけを触る。"""

    # --- ポート設定 ---
    LEFT_MOTOR_PORT = Port.A
    RIGHT_MOTOR_PORT = Port.B
    LEFT_SENSOR_PORT = Port.C
    RIGHT_SENSOR_PORT = Port.D

    # --- 車体寸法 (mm) ---
    WHEEL_DIAMETER = 56     # 車輪の直径
    AXLE_TRACK = 112        # 左右の車輪の接地点間の距離

    # --- センサーの反射光キャリブレーション値 (%) ---
    # 実測して書き換える。センサーごとに個体差があるため左右別々に持つ。
    LEFT_WHITE = 80
    LEFT_BLACK = 10
    RIGHT_WHITE = 80
    RIGHT_BLACK = 10

    # True にすると起動時にボタン操作で白・黒を測定し、上の値を上書きする
    USE_CALIBRATION = False

    # --- PID 係数 ---
    # error の範囲は -100〜100、出力は旋回率 (deg/s)
    KP = 2.0        # 比例ゲイン: 大きいほど反応が強い
    KI = 0.0        # 積分ゲイン: 定常的なズレを補正（入れすぎると発振）
    KD = 0.15       # 微分ゲイン: 急な変化を抑えて蛇行を減らす

    INTEGRAL_LIMIT = 200    # 積分値の上限（積分の溜まりすぎ防止）
    MAX_TURN_RATE = 360     # 旋回率の上限 (deg/s)

    # --- 速度・自動減速 ---
    BASE_SPEED = 200        # 誤差 0 のときの前進速度 (mm/s)
    MIN_SPEED = 60          # 減速時の最低速度 (mm/s)
    SLOWDOWN_GAIN = 2.5     # |error| 1 あたりの減速量 (mm/s)

    # --- 十字路 ---
    BLACK_THRESHOLD = 30    # 正規化値がこれ未満なら「黒」と判定
    CROSS_SPEED = 150       # 十字路通過時の速度 (mm/s)
    CROSS_EXIT_DISTANCE = 20  # 両センサーが黒を抜けた後もまっすぐ進む距離 (mm)

    # --- ループ・デバッグ ---
    LOOP_WAIT_MS = 5        # 1 ループあたりの待ち時間 (ms)
    DEBUG_PRINT = False     # True でセンサー値などを表示（ループが遅くなる）
    DEBUG_INTERVAL_MS = 200  # デバッグ表示の間隔 (ms)


# =================================================
# デバイス
# =================================================

class Devices:
    """ハブ・モーター・センサー・DriveBase をまとめたクラス。"""

    def __init__(self, config):
        self.hub = PrimeHub()

        # 左右のモーターは取り付け向きが逆なので positive_direction で揃える
        self.left_motor = Motor(
            config.LEFT_MOTOR_PORT, positive_direction=Direction.COUNTERCLOCKWISE
        )
        self.right_motor = Motor(
            config.RIGHT_MOTOR_PORT, positive_direction=Direction.CLOCKWISE
        )
        self.robot = DriveBase(
            self.left_motor,
            self.right_motor,
            wheel_diameter=config.WHEEL_DIAMETER,
            axle_track=config.AXLE_TRACK,
        )

        self.left_sensor = ColorSensor(config.LEFT_SENSOR_PORT)
        self.right_sensor = ColorSensor(config.RIGHT_SENSOR_PORT)


class PIDState:
    """PID 制御の内部状態。"""

    def __init__(self):
        self.integral = 0.0
        self.prev_error = 0.0


# =================================================
# センサー処理
# =================================================

def normalize(raw, black, white):
    """反射光を 黒=0 / 白=100 の範囲に正規化する。"""
    if white == black:
        return 0
    value = (raw - black) * 100 / (white - black)
    return max(0, min(100, value))


def read_sensors(devices, config):
    """左右センサーの正規化値 (left, right) を返す。"""
    left = normalize(
        devices.left_sensor.reflection(), config.LEFT_BLACK, config.LEFT_WHITE
    )
    right = normalize(
        devices.right_sensor.reflection(), config.RIGHT_BLACK, config.RIGHT_WHITE
    )
    return left, right


def is_crossroad(left, right, config):
    """左右どちらも黒なら十字路とみなす。"""
    return left < config.BLACK_THRESHOLD and right < config.BLACK_THRESHOLD


def calc_error(left, right):
    """誤差を計算する。負 = 左に黒線が寄っている / 正 = 右に寄っている。"""
    return left - right


# =================================================
# 制御計算
# =================================================

def reset_pid(pid):
    """PID の積分値・前回誤差をリセットする。"""
    pid.integral = 0.0
    pid.prev_error = 0.0


def calc_pid(pid, error, dt, config):
    """PID 制御で旋回率 (deg/s) を計算する。dt は秒。"""
    # 積分（上限付き）
    pid.integral += error * dt
    pid.integral = max(-config.INTEGRAL_LIMIT, min(config.INTEGRAL_LIMIT, pid.integral))

    # 微分
    derivative = (error - pid.prev_error) / dt if dt > 0 else 0
    pid.prev_error = error

    turn_rate = config.KP * error + config.KI * pid.integral + config.KD * derivative
    return max(-config.MAX_TURN_RATE, min(config.MAX_TURN_RATE, turn_rate))


def calc_speed(error, config):
    """誤差が大きいほど前進速度を落とす（自動減速）。"""
    speed = config.BASE_SPEED - config.SLOWDOWN_GAIN * abs(error)
    return max(config.MIN_SPEED, speed)


# =================================================
# 走行処理
# =================================================

def pass_crossroad(devices, config, pid):
    """十字路（黒, 黒）をまっすぐ通過する。

    両センサーが黒の間は直進し、黒を抜けた後も CROSS_EXIT_DISTANCE だけ
    直進してから通常のライントレースに戻る（抜け際の片側だけ黒による急旋回を防ぐ）。
    """
    devices.robot.drive(config.CROSS_SPEED, 0)

    # 両センサーが黒の間は直進
    while True:
        left, right = read_sensors(devices, config)
        if not is_crossroad(left, right, config):
            break
        wait(config.LOOP_WAIT_MS)

    # 抜けた後も少しだけ直進
    start = devices.robot.distance()
    while devices.robot.distance() - start < config.CROSS_EXIT_DISTANCE:
        wait(config.LOOP_WAIT_MS)

    # 十字路前後の誤差を引きずらないようにリセット
    reset_pid(pid)


def trace_step(devices, config, pid, dt):
    """ライントレース 1 ステップ分の処理。表示用に (left, right, error, speed, turn) を返す。"""
    left, right = read_sensors(devices, config)

    if is_crossroad(left, right, config):
        pass_crossroad(devices, config, pid)
        return left, right, 0, config.CROSS_SPEED, 0

    error = calc_error(left, right)
    turn_rate = calc_pid(pid, error, dt, config)
    speed = calc_speed(error, config)
    devices.robot.drive(speed, turn_rate)
    return left, right, error, speed, turn_rate


# =================================================
# ユーティリティ
# =================================================

def wait_for_button(devices, button):
    """指定ボタンが押されて離されるまで待つ。"""
    while button not in devices.hub.buttons.pressed():
        wait(10)
    while button in devices.hub.buttons.pressed():
        wait(10)


def calibrate(devices, config):
    """ボタン操作で白・黒の反射光を測定し、config に書き込む。"""
    print("キャリブレーション: 両センサーを白の上に置いて LEFT ボタン")
    wait_for_button(devices, Button.LEFT)
    config.LEFT_WHITE = devices.left_sensor.reflection()
    config.RIGHT_WHITE = devices.right_sensor.reflection()
    print("白:", config.LEFT_WHITE, config.RIGHT_WHITE)

    print("両センサーを黒の上に置いて RIGHT ボタン")
    wait_for_button(devices, Button.RIGHT)
    config.LEFT_BLACK = devices.left_sensor.reflection()
    config.RIGHT_BLACK = devices.right_sensor.reflection()
    print("黒:", config.LEFT_BLACK, config.RIGHT_BLACK)


def debug_print(left, right, error, speed, turn_rate):
    """センサー値・誤差・速度・旋回率を表示する。"""
    print("L:", int(left), "R:", int(right), "err:", int(error),
          "spd:", int(speed), "turn:", int(turn_rate))


# =================================================
# メイン
# =================================================

def main():
    config = Config()
    devices = Devices(config)
    pid = PIDState()

    if config.USE_CALIBRATION:
        calibrate(devices, config)

    print("CENTER ボタンでライントレース開始")
    wait_for_button(devices, Button.CENTER)

    print("ライントレース中... BLUETOOTH ボタンで終了")
    loop_timer = StopWatch()
    debug_timer = StopWatch()
    reset_pid(pid)

    while Button.BLUETOOTH not in devices.hub.buttons.pressed():
        # 前回ループからの経過時間 (秒)
        dt = loop_timer.time() / 1000
        loop_timer.reset()

        left, right, error, speed, turn_rate = trace_step(devices, config, pid, dt)

        if config.DEBUG_PRINT and debug_timer.time() >= config.DEBUG_INTERVAL_MS:
            debug_print(left, right, error, speed, turn_rate)
            debug_timer.reset()

        wait(config.LOOP_WAIT_MS)

    devices.robot.stop()
    print("ライントレース終了")


main()
