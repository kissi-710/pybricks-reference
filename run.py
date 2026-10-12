"""
SPIKE Prime ライントレースカー: Raspberry Pi 指令式（RUN / WAIT / STOP）
=======================================================================

黒線を左右 2 つのカラーセンサーで「挟む」ライントレースカーです。
Raspberry Pi から BLE（Pybricks の stdin）経由で届く文字列コマンドで
走行・待機・完全停止を切り替えます。ハブ側プログラムとして書き込んで使います。

【センサー配置（上から見た図）】

        進行方向 ↑
     [左S]  ┃  [右S]      ← 左右センサーの間に黒線が来る
            ┃
     (左輪) ┃ (右輪)

=======================================================================
 機能一覧（コード中のコメントは 【機能: ○○】 の形で、どの機能の処理かを示します）
=======================================================================

  【機能】            【設定(Config)】  【状態(State)】   【主な関数】
  ------------------  ----------------  ----------------  ------------------------------
  Pi 通信             -                 RunMode           CommandReceiver / send / apply_command
  ソフトストップ      SoftStopConfig    SoftStopState     request_stop / apply_soft_stop / halt
  自動キャリブレーション CalibrationConfig Calibration     auto_calibrate / sweep_to
  PID 制御            PidConfig         PidState          calc_pid / calc_error
  カーブ減速          CurveConfig       CurveState        update_curve / calc_target_speed
                      SpeedConfig       SpeedState        ramp_speed
  直角カーブ          CornerConfig      CornerState       detect_corner_side / step_pivot ほか
  十字路              CrossConfig       CrossState        step_cross
  ロスト復帰          LostConfig        LostState         update_lost / step_search ほか
  デバッグ表示        DebugConfig       -                 debug_phase / debug_print

  （共通: HardwareConfig=ポート・車体寸法 / LoopConfig=ループ周期 / Phase=走行中の内部フェーズ）

=======================================================================
 【機能: Pi 通信】 Raspberry Pi からのコマンド（末尾に必ず "\\n" を付けて送る）
=======================================================================

  コマンド  動作                                         ハブからの応答
  --------  -------------------------------------------  ---------------------------
  RUN       走行する（待機・ソフトストップ中の再開も）   OK:RUN
  WAIT      緩やかに減速して止まり、待機（RUN で再開）   OK:WAIT → 止まったら DONE:WAIT
  STOP      緩やかに減速して止まり、プログラム終了       OK:STOP → 止まったら DONE:STOP
  (その他)  無視する                                     NG:UNKNOWN

  ・OK: は「受け付けた」、DONE: は「実際に止まった」合図です。
  ・STOP を減速中にもう一度送ると、減速せず即座に止まります（非常停止）。
  ・起動直後はキャリブレーションを行い、終わると "CAL:..." と "READY" を送ります。
    READY を受け取ってから RUN を送ってください（それ以前に届いたコマンドは
    バッファされ、キャリブレーション後に処理されます。STOP だけは即時に効きます）。
    起動直後は WAIT 状態で、RUN が来るまで走り出しません。
  ・ロスト復帰中は次を送ります: LOST:L / LOST:R（線が逃げた向き）、FOUND（見つけた）、
    LOST:GIVEUP（見つからず断念。この後 DONE:WAIT で待機状態になる）。
  ※ break（Ctrl+C）はプログラムごと終了してしまうので使いません。
  ※ print() の出力も同じ stdout に流れます。Pi 側は "OK:" "NG:" "DONE:" "CAL:" "LOST"
    "FOUND" "READY" で始まる行だけをコマンド応答として扱ってください
    （Debug は既定で全て OFF）。

=======================================================================
 各機能の概要
=======================================================================

【機能: PID 制御】
  誤差 error = 左の値 - 右の値（黒=0 / 白=100 に正規化）から旋回率を計算する。

【機能: カーブ減速】（ヒステリシス付き）
  「誤差の大きさの移動平均」か「誤差の偏り（同じ向きに曲がり続けている度合い）」が
  しきい値を超えたら「カーブ中」とみなして減速し、両方が小さくなった状態で
  exit_distance_mm 走るまで減速を続ける。直線の蛇行は左右交互に振れて偏りが
  打ち消し合うので、カーブとは区別できる。

【機能: 直角カーブ】
  片側のセンサーが急に暗くなったら直角カーブの候補とし、確認できたら
  前進を止めて超信地旋回（その場回転）を約 90 度ぶん行ってから PID に戻る。
  旋回中は前進しない（センサーが車軸より前にある機体は advance_mm で調整）。
  直線での誤作動防止（4 重ガード）:
    直線でセンサーが線の縁に触れた場合と、直角カーブで角の黒線に当たった場合は
    「片側だけ黒」という瞬間の見た目が同じです。違いは「黒になるまでの速さ」です。
      - 直線でのはみ出し: 線に対して浅い角度で近づくので、白→黒がゆっくり進む
      - 直角カーブ: 黒線に正面から突っ込むので、白→黒が短い走行距離で一気に進む
    そこで次の 4 つを全て満たしたときだけ直角カーブと判断します。
      a. 片側が暗く(< dark_on)なり、反対側が明確な白(> white_on)
      b. その片側は、直前に白(> white_on)だった位置から abrupt_mm 以内の走行で暗くなった
         （緩やかに暗くなった＝直線でのはみ出し、は対象外。PID がそのまま補正する）
      c. 候補になったら減速してまっすぐ confirm_mm 進み、その間に深い黒(< black_on)に
         なり、反対側は白のままであること（反対側も暗くなったら十字路なので取り消し）
      d. 直角カーブ・十字路の直後は cooldown_mm だけ判定を止める

【機能: 十字路】
  左右とも黒になったらまっすぐ通過する。

【機能: 自動キャリブレーション】
  起動時に車体をその場で左右に振り、各センサーの反射光の最小/最大から
  黒・白の値を自動で決める（コントラスト不足なら振り幅を広げて再試行）。

【機能: ソフトストップ】
  WAIT / STOP を受けたら、ライン追従（PID）を続けたまま decel の減速度で速度を 0 まで
  落としてから止める。急停止による車体のぶれ・線からの逸脱を防ぐ。
  速度が min_speed 未満なら即停止。timeout_ms を超えたら強制的に止める。

【機能: ロスト復帰】
  線が横へ逃げて見失ったときに、探索して線へ戻る。
  ※ 左右のセンサーで線を挟む構成では「両方白」が正常な状態でもあるため、白だけでは
    ロストと判定できない。そこで次の合図でロストと判断する。
      検出 A（escape_mm）: センサーが暗い状態で escape_mm 以上走ったあと、両方白へ抜けた
                          （回復できるはみ出しは暗い期間が短い。線が横へ逃げるときは長く続く）
      検出 B（max_white_mm）: 両方白のまま max_white_mm 走った（既定は無効。
                          コースの最長直線より長い値を入れると、線のない所へ出たときに働く）
  探索: 線が逃げた側へ search_deg ずつ振り幅を広げて左右にその場回転 → 見つからなければ
        creep_mm 前進して再探索（retries 回まで）→ 断念したら LOST:GIVEUP を送って待機。

【機能: デバッグ表示】 Debug で値ごとに ON/OFF（既定は全て OFF）。

【dataclass について】
  MicroPython 本体は dataclasses に対応しておらず、Pybricks のハブにも標準では
  入っていない可能性が高いため、import に失敗したときは同じ書き方で使える簡易版
  dataclass / field を自前で用意します（PC の CPython では標準のものを使います）。
  簡易版の制約: 全フィールドに既定値を付ける / キーワード引数でだけ初期化できる /
  型注釈は無視される / __eq__ などは作られない。

【調整の手順（目安）】
  1. 線を 2 つのセンサーの真ん中、白い面の上にして起動する
     （起動時の自動キャリブレーションで左右に振って白・黒を測る。車体の周りに少し空間が必要）
  2. ki = kd = 0 にして kp を上げ、蛇行し始める手前で止める → kd で蛇行を抑える
  3. カーブの減速: speed.curve（カーブ中の速度）、curve.enter_error / enter_bias（突入）、
     curve.exit_error / exit_bias / exit_distance_mm（脱出）を調整
  4. 直角カーブ: corner.target_angle / pivot_rate / advance_mm を調整
       - センサーが車軸より前にある機体は、advance_mm（センサー〜車軸の距離 + 線幅の半分）を
         設定すると角の頂点で回れて線を見失いにくい（0 なら旋回前に前進しない）
       - 直線で誤作動する → abrupt_mm を小さく / dark_on を小さく / white_on を大きく
       - 直角を見逃す → abrupt_mm を大きく / dark_on を大きく
       - 十字路を直角と誤認する → confirm_mm を大きく
  5. ソフトストップ: soft.decel（小さいほどゆっくり止まる）
  6. ロスト復帰: lost.escape_mm（誤検出が多ければ大きく / 見逃すなら小さく）、
     コースの最長直線が分かるなら lost.max_white_mm を設定
"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Port, Direction, Color
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

# 標準 MicroPython モジュール（stdin の非ブロッキング読み取りに使用）
from usys import stdin, stdout
from uselect import poll


# =================================================
# dataclass 互換（ハブに dataclasses が無い場合の簡易版）
# =================================================

try:
    from dataclasses import dataclass, field
except ImportError:

    class _Field:
        """field(default_factory=...) の印。インスタンスごとに factory を呼ぶ。"""

        def __init__(self, default_factory):
            self.default_factory = default_factory

    def field(default_factory=None):
        return _Field(default_factory)

    def dataclass(cls):
        """クラス属性の既定値から __init__ / __repr__ を作る簡易 dataclass。"""
        names = []
        for name in dir(cls):
            if name.startswith("_"):
                continue
            value = getattr(cls, name)
            # メソッド（関数）は除外。_Field は callable ではないので残る
            if callable(value):
                continue
            names.append(name)

        def __init__(self, **kwargs):
            for name in names:
                default = getattr(cls, name)
                if isinstance(default, _Field):
                    default = default.default_factory()
                if name in kwargs:
                    default = kwargs.pop(name)
                setattr(self, name, default)
            if kwargs:
                raise TypeError("不明なフィールド: " + str(list(kwargs)))

        def __repr__(self):
            items = []
            for name in names:
                items.append(name + "=" + str(getattr(self, name)))
            return cls.__name__ + "(" + ", ".join(items) + ")"

        cls.__init__ = __init__
        cls.__repr__ = __repr__
        return cls


# =================================================
# 定数（enum の代わり。MicroPython では単純なクラス定数にする）
# =================================================

class RunMode:
    """【機能: Pi 通信】 Raspberry Pi からの指令で決まる状態。"""

    WAIT = 0    # 待機（その場で停止。RUN で再開できる）
    RUN = 1     # 走行
    STOP = 2    # 完全停止（プログラム終了）


class Phase:
    """走行中の内部フェーズ（RunMode.RUN の間だけ意味を持つ）。"""

    TRACE = 0       # 【機能: PID 制御】 通常のライントレース
    CROSS = 1       # 【機能: 十字路】 十字路をまっすぐ通過
    PROBE = 2       # 【機能: 直角カーブ】 候補を確認中（減速してまっすぐ進む）
    ADVANCE = 3     # 【機能: 直角カーブ】 車軸を角の頂点へ寄せる（advance_mm > 0 のときだけ）
    PIVOT = 4       # 【機能: 直角カーブ】 前進せず、その場で旋回
    SEARCH = 5      # 【機能: ロスト復帰】 線を探している


class LostTrack:
    """【機能: ロスト復帰】 検出 A で追跡している「暗い期間」の状態。"""

    NONE = 0        # 追跡していない
    IN_DARK = 1     # センサーが暗い期間の最中
    ENDED = 2       # 暗い期間が終わり、両方白になるのを待っている


class SearchStage:
    """【機能: ロスト復帰】 探索の段階。"""

    TURN = 0        # 左右にその場回転して線を探す
    BACK = 1        # 探索開始時の向きへ戻る
    CREEP = 2       # 少し前進して、もう一度探す


# =================================================
# 設定（調整用の係数・閾値。値を変えるときはここだけを触る）
# =================================================

@dataclass
class HardwareConfig:
    """【共通】 ポート・車体寸法。"""

    left_motor_port: Port = Port.A
    right_motor_port: Port = Port.B
    left_sensor_port: Port = Port.C
    right_sensor_port: Port = Port.D

    # 左右のモーターは取り付け向きが逆なので positive_direction で揃える
    left_motor_direction: Direction = Direction.COUNTERCLOCKWISE
    right_motor_direction: Direction = Direction.CLOCKWISE

    wheel_diameter: int = 56        # 車輪の直径 (mm)
    axle_track: int = 112           # 左右の車輪の接地点間の距離 (mm)
    use_gyro: bool = True           # ジャイロで旋回角を測る（直角旋回・ロスト探索の精度が上がる）

    # drive() の加減速の上限。大きいほど指令にすばやく追従する
    straight_acceleration: int = 1500   # mm/s^2
    turn_acceleration: int = 3000       # deg/s^2


@dataclass
class CalibrationConfig:
    """【機能: 自動キャリブレーション】"""

    auto: bool = True               # 起動時に自動キャリブレーションを行う
    swing_deg: int = 50             # 左右に振る角度 (deg)。線を横切れる大きさにする
    swing_step_deg: int = 15        # 再試行ごとに広げる角度 (deg)
    max_retries: int = 2            # 再試行の回数
    turn_rate: int = 90             # 振る速さ (deg/s)
    min_rate: int = 20              # 目標付近で落とす最低の速さ (deg/s)
    tolerance_deg: int = 2          # 目標角度とのズレの許容 (deg)
    min_contrast: int = 40          # 白と黒の差がこれ未満なら失敗とみなす（反射光 %）。線を横切れていないと差が小さくなる

    # 自動キャリブレーションを使わない / 失敗したときの既定値（反射光 %）
    default_left_white: int = 80
    default_left_black: int = 10
    default_right_white: int = 80
    default_right_black: int = 10


@dataclass
class PidConfig:
    """【機能: PID 制御】 PID 係数。error の範囲は -100〜100、出力は旋回率 (deg/s)。"""

    kp: float = 2.0                 # 比例ゲイン: 大きいほど反応が強い
    ki: float = 0.0                 # 積分ゲイン: 入れすぎると発振する
    kd: float = 0.15                # 微分ゲイン: 蛇行を抑える
    integral_limit: float = 200.0   # 積分値の上限（溜まりすぎ防止）
    max_turn_rate: float = 360.0    # 旋回率の上限 (deg/s)


@dataclass
class SpeedConfig:
    """【機能: カーブ減速】 前進速度。"""

    base: int = 200                 # 直線の速度 (mm/s)
    minimum: int = 60               # 減速時の下限 (mm/s)
    curve: int = 100                # カーブ中の上限速度 (mm/s)
    slowdown_gain: float = 2.0      # |error| 1 あたりの減速量 (mm/s)
    accel: int = 600                # 加速の上限 (mm/s^2)。減速は即時に行う


@dataclass
class CurveConfig:
    """【機能: カーブ減速】 カーブ検出（入ったら抜けるまで減速）。"""

    enter_error: float = 25.0       # |error| の移動平均がこれ以上でカーブ突入（急カーブ向け）
    enter_bias: float = 12.0        # error の偏り（符号つき移動平均）の大きさがこれ以上でも突入（緩いカーブ向け）
    exit_error: float = 10.0        # |error| の移動平均がこれ以下 かつ
    exit_bias: float = 5.0          # 偏りがこれ以下の状態が続いたら抜け始めとみなす
    exit_distance_mm: int = 40      # 抜け始めてから走る距離。超えたらカーブ脱出
    error_tau_ms: int = 40          # |error| の移動平均の時定数 (ms)
    bias_tau_ms: int = 300          # 偏りの移動平均の時定数 (ms)。長いほど蛇行を無視する


@dataclass
class CornerConfig:
    """【機能: 直角カーブ】 前進せずに約 90 度旋回する。"""

    enabled: bool = True            # False にすると直角カーブ処理を無効化

    # --- 候補にする条件（直線での誤作動を防ぐ） ---
    white_on: int = 60              # 「明確な白」とみなす正規化値 (%)。反対側の条件と、急変の起点に使う
    dark_on: int = 40               # 片側がこれ未満になったら「暗くなった」（候補の開始）
    abrupt_mm: int = 6              # 白(> white_on)→暗(< dark_on)がこの走行距離以内なら「角」。長いなら直線のはみ出し
    # --- 確認中の条件 ---
    probe_speed: int = 60           # 確認中の速度 (mm/s)。まっすぐ進む（旋回すると角から外れるため）
    confirm_mm: int = 10            # この距離まっすぐ進んで確認する
    black_on: int = 20              # 確認中に黒側がこれ未満（深い黒）にならなければ取り消し
    white_hold: int = 40            # 確認中に反対側がこれ未満に暗くなったら取り消し（十字路を斜めに通過）
    probe_timeout_ms: int = 1500    # 確認が終わらないときの打ち切り時間

    # --- 旋回 ---
    advance_mm: int = 0             # 旋回前に前進する距離。0 なら前進しない
    advance_speed: int = 100        # 前進するときの速度 (mm/s)
    target_angle: int = 90          # 曲がる角度 (deg)
    exit_margin: int = 15           # この角度手前で PID に戻す（PID が残りを合わせる）
    pivot_rate: int = 180           # 旋回の速さ (deg/s)
    pivot_min_rate: int = 60        # 目標付近で落とす最低の速さ (deg/s)
    pivot_timeout_ms: int = 2500    # 旋回が終わらないときの打ち切り時間

    # --- 旋回後 ---
    cooldown_mm: int = 40           # 直角カーブ・十字路・ロスト復帰の後、この距離は判定しない


@dataclass
class CrossConfig:
    """【機能: 十字路】 左右とも黒。"""

    black_threshold: int = 30       # 正規化値がこれ未満なら「黒」
    speed: int = 150                # 通過時の速度 (mm/s)
    exit_mm: int = 20               # 両センサーが黒を抜けた後もまっすぐ進む距離 (mm)


@dataclass
class SoftStopConfig:
    """【機能: ソフトストップ】 WAIT / STOP を緩やかな減速で止める。"""

    on_wait: bool = True            # WAIT をソフトストップにする（False なら即停止）
    on_stop: bool = True            # STOP をソフトストップにする（False なら即停止）
    decel: int = 400                # 減速度 (mm/s^2)。200mm/s からなら約 0.5 秒・50mm で止まる
    min_speed: int = 10             # 現在速度がこれ未満なら減速せず即停止 (mm/s)
    timeout_ms: int = 2000          # この時間で止まらなければ強制的に止める


@dataclass
class LostConfig:
    """【機能: ロスト復帰】 線を見失ったときの検出と探索。"""

    enabled: bool = True            # False にするとロスト復帰を無効化

    # --- 検出 A: 暗い期間が長かったあとに両方白へ抜けた ---
    escape_mm: int = 15             # 暗い状態で走った距離がこれ以上なら「線が横へ逃げた」
    window_mm: int = 30             # 暗→（グレー）→白 と抜ける間に許す距離
    # --- 検出 B: 両方白のまま長く走った ---
    max_white_mm: int = 0           # 0 = 無効。コースの最長直線より長い値を入れると有効

    # --- 探索 ---
    found_level: int = 40           # どちらかのセンサーがこれ未満になったら「線を見つけた」
    search_deg: int = 45            # 探索で振る角度の刻み (deg)。1 往復目 ±45°、2 往復目 ±90°
    search_legs: int = 4            # 振る回数（逃げた側 → 反対側 → 逃げた側(広く) → 反対側(広く)）
    search_rate: int = 120          # 探索で回る速さ (deg/s)
    search_min_rate: int = 40       # 目標付近で落とす最低の速さ (deg/s)
    search_tolerance_deg: int = 3   # 目標角度とのズレの許容 (deg)
    creep_mm: int = 40              # 見つからなければ前進する距離 (mm)
    creep_speed: int = 60           # 前進の速度 (mm/s)
    retries: int = 2                # 前進して再探索する回数。超えたら断念
    timeout_ms: int = 10000         # 探索全体の制限時間。超えたら断念


@dataclass
class LoopConfig:
    """【共通】 ループ周期。"""

    wait_ms: int = 5                # 1 ループあたりの待ち時間 (ms)


@dataclass
class DebugConfig:
    """【機能: デバッグ表示】 ログ出力の ON/OFF。True にした値だけ出力する（print はループを遅くする）。

    出力は Pi との通信と同じ stdout に流れる点に注意。
    """

    left: bool = False              # 左センサーの正規化値
    right: bool = False             # 右センサーの正規化値
    error: bool = False             # 誤差 (左 - 右)
    speed: bool = False             # 前進速度 (mm/s)
    turn_rate: bool = False         # 旋回率 (deg/s)
    phase: bool = False             # フェーズ遷移（直角カーブ・十字路・ロスト復帰・ソフトストップ）
    interval_ms: int = 200          # 値のログを出す間隔 (ms)。phase は遷移時に毎回出力


@dataclass
class Config:
    """全設定をまとめたもの。"""

    hw: HardwareConfig = field(default_factory=HardwareConfig)
    cal: CalibrationConfig = field(default_factory=CalibrationConfig)
    pid: PidConfig = field(default_factory=PidConfig)
    speed: SpeedConfig = field(default_factory=SpeedConfig)
    curve: CurveConfig = field(default_factory=CurveConfig)
    corner: CornerConfig = field(default_factory=CornerConfig)
    cross: CrossConfig = field(default_factory=CrossConfig)
    soft: SoftStopConfig = field(default_factory=SoftStopConfig)
    lost: LostConfig = field(default_factory=LostConfig)
    loop: LoopConfig = field(default_factory=LoopConfig)
    debug: DebugConfig = field(default_factory=DebugConfig)


# =================================================
# 実行中の状態
# =================================================

@dataclass
class PidState:
    """【機能: PID 制御】"""

    integral: float = 0.0
    prev_error: float = 0.0


@dataclass
class SpeedState:
    """【機能: カーブ減速】"""

    current: float = 0.0            # 現在の前進速度 (mm/s)


@dataclass
class CurveState:
    """【機能: カーブ減速】"""

    active: bool = False            # カーブ中か
    avg_error: float = 0.0          # |error| の移動平均
    bias: float = 0.0               # error の偏り（符号つき移動平均）
    calm_start_mm: float = None     # 誤差が小さくなり始めた位置（None = 未開始）


@dataclass
class CornerState:
    """【機能: 直角カーブ】"""

    side: int = 0                   # 曲がる向き: -1 = 左 / +1 = 右
    start_mm: float = 0.0           # 候補になった位置 (mm)
    start_ms: int = 0               # 候補になった時刻 (ms)
    advance_start_mm: float = 0.0   # 前進を始めた位置 (mm)
    start_angle: float = 0.0        # 旋回を始めたときの角度 (deg)
    cooldown_until_mm: float = 0.0  # この距離まで直角カーブ・ロスト判定をしない
    reached_black: bool = False     # 確認中に深い黒(< black_on)を見たか
    last_white_left_mm: float = -1000000.0    # 左センサーが最後に白だった位置 (mm)
    last_white_right_mm: float = -1000000.0   # 右センサーが最後に白だった位置 (mm)


@dataclass
class CrossState:
    """【機能: 十字路】"""

    exit_start_mm: float = None     # 両センサーが黒を抜けた位置（None = まだ黒の中）


@dataclass
class SoftStopState:
    """【機能: ソフトストップ】"""

    active: bool = False            # 減速して止まる途中か
    target: int = RunMode.WAIT      # 止まったあとの状態（WAIT / STOP）
    ceiling: float = 0.0            # 速度の上限（時間とともに 0 へ下げる）(mm/s)
    start_ms: int = 0               # 開始時刻 (ms)


@dataclass
class LostState:
    """【機能: ロスト復帰】"""

    # --- 検出 ---
    track: int = LostTrack.NONE     # 検出 A の追跡状態
    side: int = 0                   # 最後に暗くなった側: -1 = 左 / +1 = 右 / 0 = 不明
    start_mm: float = 0.0           # 暗くなり始めた位置 (mm)
    length: float = 0.0             # 暗かった期間に走った距離 (mm)
    end_mm: float = 0.0             # 暗い期間が終わった位置 (mm)
    white_since_mm: float = None    # 両方白になり始めた位置（None = 白が続いていない。検出 B 用）
    # --- 探索 ---
    stage: int = SearchStage.TURN   # 探索の段階
    leg: int = 0                    # 何回目の振りか
    base_angle: float = 0.0         # 探索開始時の向き (deg)
    creep_start_mm: float = 0.0     # 前進を始めた位置 (mm)
    retry: int = 0                  # 前進して再探索した回数
    start_ms: int = 0               # 探索を始めた時刻 (ms)


@dataclass
class State:
    """全状態をまとめたもの。"""

    run: int = RunMode.WAIT
    phase: int = Phase.TRACE
    pid: PidState = field(default_factory=PidState)
    speed: SpeedState = field(default_factory=SpeedState)
    curve: CurveState = field(default_factory=CurveState)
    corner: CornerState = field(default_factory=CornerState)
    cross: CrossState = field(default_factory=CrossState)
    soft: SoftStopState = field(default_factory=SoftStopState)
    lost: LostState = field(default_factory=LostState)


@dataclass
class Calibration:
    """【機能: 自動キャリブレーション】 正規化に使う黒・白の反射光 (%)。"""

    left_white: int = 80
    left_black: int = 10
    right_white: int = 80
    right_black: int = 10
    ok: bool = False                # 自動キャリブレーションが成功したか


@dataclass
class SensorRange:
    """【機能: 自動キャリブレーション】 測定中に観測した反射光の最小・最大。"""

    low: int = 100
    high: int = 0

    def update(self, value):
        if value < self.low:
            self.low = value
        if value > self.high:
            self.high = value

    def contrast(self):
        return self.high - self.low


# =================================================
# デバイス / 通信
# =================================================

class Devices:
    """【共通】 ハブ・モーター・センサー・DriveBase をまとめたクラス。"""

    def __init__(self, hw):
        self.hub = PrimeHub()
        self.clock = StopWatch()    # 起動からの経過時間 (ms)。タイムアウト判定用

        left_motor = Motor(hw.left_motor_port, positive_direction=hw.left_motor_direction)
        right_motor = Motor(hw.right_motor_port, positive_direction=hw.right_motor_direction)
        self.robot = DriveBase(
            left_motor,
            right_motor,
            wheel_diameter=hw.wheel_diameter,
            axle_track=hw.axle_track,
        )
        self.robot.settings(
            straight_acceleration=hw.straight_acceleration,
            turn_acceleration=hw.turn_acceleration,
        )
        self.robot.use_gyro(hw.use_gyro)

        self.left_sensor = ColorSensor(hw.left_sensor_port)
        self.right_sensor = ColorSensor(hw.right_sensor_port)


class CommandReceiver:
    """【機能: Pi 通信】 stdin からコマンド（改行区切り）を非ブロッキングで読む。"""

    def __init__(self):
        self.poller = poll()
        self.poller.register(stdin)

    def read(self):
        """届いていれば大文字化したコマンド (bytes) を返す。無ければ None。

        データが届いている時だけ readline するので通常はブロックしない。
        ホスト側は必ず末尾に "\\n" を付けて送ること。
        """
        if not self.poller.poll(0):
            return None
        line = stdin.buffer.readline()
        if line is None:
            return None
        line = line.strip().upper()
        if not line:
            return None
        return line


def send(text):
    """【機能: Pi 通信】 Pi へ 1 行送る。"""
    stdout.buffer.write((text + "\n").encode())


def debug_phase(config, text):
    """【機能: デバッグ表示】 フェーズ遷移のログ（Debug.phase が True のときだけ）。"""
    if config.debug.phase:
        print("[phase] " + text)


# =================================================
# 汎用
# =================================================

def clamp(value, low, high):
    """【共通】 value を low〜high に収める。"""
    return max(low, min(high, value))


# =================================================
# センサー処理
# =================================================

def normalize(raw, black, white):
    """【共通: センサー処理】 反射光を 黒=0 / 白=100 の範囲に正規化する。"""
    if white == black:
        return 0
    value = (raw - black) * 100 / (white - black)
    return clamp(value, 0, 100)


def read_sensors(devices, cal):
    """【共通: センサー処理】 左右センサーの正規化値 (left, right) を返す。"""
    left = normalize(devices.left_sensor.reflection(), cal.left_black, cal.left_white)
    right = normalize(devices.right_sensor.reflection(), cal.right_black, cal.right_white)
    return left, right


def calc_error(left, right):
    """【機能: PID 制御】 誤差。負 = 左に黒線が寄っている（左へ旋回）/ 正 = 右に寄っている（右へ旋回）。"""
    return left - right


def is_both_black(left, right, threshold):
    """【機能: 十字路】 左右どちらも黒なら十字路。"""
    return left < threshold and right < threshold


def update_last_white(left, right, distance, corner, cs):
    """【機能: 直角カーブ】 各センサーが最後に「明確な白」だった走行距離を記録する。"""
    if left > corner.white_on:
        cs.last_white_left_mm = distance
    if right > corner.white_on:
        cs.last_white_right_mm = distance


def detect_corner_side(left, right, distance, corner, cs):
    """【機能: 直角カーブ】 直角カーブの候補か判定する。曲がる向き(-1 左 / +1 右)、候補でなければ 0。

    次を全て満たすときだけ候補にする。
      - 片側が暗くなり(< dark_on)、反対側が明確な白(> white_on)
      - その暗さが、直前に白だった位置から abrupt_mm 以内の走行で現れた（急に暗くなった）
    直線でのはみ出しは白→暗がゆっくり進むため、ここでは候補にならない。
    """
    if left < corner.dark_on and right > corner.white_on:
        if distance - cs.last_white_left_mm <= corner.abrupt_mm:
            return -1
    if right < corner.dark_on and left > corner.white_on:
        if distance - cs.last_white_right_mm <= corner.abrupt_mm:
            return 1
    return 0


# =================================================
# 制御計算（PID / カーブ減速）
# =================================================

def reset_pid(pid):
    """【機能: PID 制御】 積分値・前回誤差をリセットする。"""
    pid.integral = 0.0
    pid.prev_error = 0.0


def calc_pid(pid, error, dt, cfg):
    """【機能: PID 制御】 PID 制御で旋回率 (deg/s) を計算する。dt は秒。"""
    if dt <= 0:
        dt = 0.001

    pid.integral += error * dt
    pid.integral = clamp(pid.integral, -cfg.integral_limit, cfg.integral_limit)

    derivative = (error - pid.prev_error) / dt
    pid.prev_error = error

    turn_rate = cfg.kp * error + cfg.ki * pid.integral + cfg.kd * derivative
    return clamp(turn_rate, -cfg.max_turn_rate, cfg.max_turn_rate)


def update_curve(curve, error, distance, dt, cfg):
    """【機能: カーブ減速】 カーブ中かどうかを更新する。突入したら「誤差が小さい状態で一定距離走る」まで抜けない。

    戻り値: 突入した瞬間 1 / 脱出した瞬間 -1 / 変化なし 0
    """
    alpha_error = clamp(dt * 1000 / cfg.error_tau_ms, 0, 1)
    alpha_bias = clamp(dt * 1000 / cfg.bias_tau_ms, 0, 1)
    curve.avg_error += alpha_error * (abs(error) - curve.avg_error)
    curve.bias += alpha_bias * (error - curve.bias)

    if not curve.active:
        if curve.avg_error >= cfg.enter_error or abs(curve.bias) >= cfg.enter_bias:
            curve.active = True
            curve.calm_start_mm = None
            return 1
        return 0

    calm = curve.avg_error <= cfg.exit_error and abs(curve.bias) <= cfg.exit_bias
    if not calm:
        curve.calm_start_mm = None
    elif curve.calm_start_mm is None:
        curve.calm_start_mm = distance
    elif distance - curve.calm_start_mm >= cfg.exit_distance_mm:
        curve.active = False
        curve.calm_start_mm = None
        return -1
    return 0


def force_curve(curve):
    """【機能: カーブ減速】 直角カーブ・復帰直後などで「カーブ中」にしておく。"""
    curve.active = True
    curve.calm_start_mm = None


def calc_target_speed(cfg, curve, error):
    """【機能: カーブ減速】 誤差が大きいほど減速し、カーブ中は curve を上限にする。"""
    speed = max(cfg.minimum, cfg.base - cfg.slowdown_gain * abs(error))
    if curve.active:
        speed = min(speed, cfg.curve)
    return speed


def ramp_speed(speed_state, target, dt, cfg):
    """【機能: カーブ減速】 減速は即時、加速は accel の上限つきで現在速度を更新して返す。"""
    if target <= speed_state.current:
        speed_state.current = target
    else:
        speed_state.current = min(target, speed_state.current + cfg.accel * dt)
    return speed_state.current


# =================================================
# ロスト復帰: 検出
# =================================================

def reset_lost_tracking(ls):
    """【機能: ロスト復帰】 検出用の追跡状態を捨てる（直角カーブ・十字路などの前後で呼ぶ）。"""
    ls.track = LostTrack.NONE
    ls.side = 0
    ls.white_since_mm = None


def update_lost(left, right, distance, corner, lc, ls):
    """【機能: ロスト復帰】 ロストの合図を検出する。線が逃げた向き(-1 左 / +1 右)、なければ 0。

    検出 A: センサーが暗い状態で escape_mm 以上走ったあと、両方白へ抜けた。
            回復できるはみ出しは暗い期間が短く（PID がすぐ引き戻す）、
            線が横へ逃げるときは暗い期間が長く続くことを利用している。
    検出 B: 両方白のまま max_white_mm 走った（max_white_mm > 0 のときだけ）。
    """
    dark = left < corner.dark_on or right < corner.dark_on
    both_white = left > corner.white_on and right > corner.white_on

    # --- 検出 B: 両方白が長く続いた ---
    if both_white:
        if ls.white_since_mm is None:
            ls.white_since_mm = distance
        elif lc.max_white_mm > 0 and distance - ls.white_since_mm >= lc.max_white_mm:
            ls.white_since_mm = None
            return ls.side if ls.side != 0 else 1
    else:
        ls.white_since_mm = None

    # --- 検出 A: 暗い期間の長さを測る ---
    if dark:
        if ls.track != LostTrack.IN_DARK:
            ls.track = LostTrack.IN_DARK
            ls.start_mm = distance
        ls.side = -1 if left < right else 1     # 暗いほうの側（線が逃げる向きの手がかり）
        return 0

    if ls.track == LostTrack.IN_DARK:           # 暗い期間が今終わった
        ls.track = LostTrack.ENDED
        ls.length = distance - ls.start_mm
        ls.end_mm = distance

    if ls.track == LostTrack.ENDED:
        if both_white:
            ls.track = LostTrack.NONE
            if ls.length >= lc.escape_mm:
                return ls.side
        elif distance - ls.end_mm > lc.window_mm:
            ls.track = LostTrack.NONE           # 白に抜けないまま距離が過ぎた → 追跡をやめる
    return 0


# =================================================
# ソフトストップ / 状態の切り替え
# =================================================

def reset_motion(devices, st):
    """【共通】 走行の内部状態を初期化する（RUN で走り始める前に呼ぶ）。"""
    reset_pid(st.pid)                       # 【機能: PID 制御】
    st.speed.current = 0.0                  # 【機能: カーブ減速】
    st.phase = Phase.TRACE
    st.curve.active = False
    st.curve.avg_error = 0.0
    st.curve.bias = 0.0
    st.curve.calm_start_mm = None
    st.cross.exit_start_mm = None           # 【機能: 十字路】
    st.corner.cooldown_until_mm = devices.robot.distance()     # 【機能: 直角カーブ】
    # 走り始めの黒は「急に黒くなった」か分からないので、最初に白を見るまで候補にしない
    st.corner.last_white_left_mm = -1000000.0
    st.corner.last_white_right_mm = -1000000.0
    st.soft.active = False                  # 【機能: ソフトストップ】
    reset_lost_tracking(st.lost)            # 【機能: ロスト復帰】


def halt(devices, st, target):
    """【機能: ソフトストップ】 実際にモーターを止めて、状態を target（WAIT / STOP）にする。"""
    st.soft.active = False
    st.run = target
    if target == RunMode.WAIT:
        devices.robot.hold()                # 待機: その場で保持（RUN で再開できる）
        devices.hub.light.on(Color.YELLOW)
        send("DONE:WAIT")
    else:
        devices.robot.brake()               # 完全停止
        devices.hub.light.on(Color.RED)
        send("DONE:STOP")


def request_stop(devices, config, st, target):
    """【機能: ソフトストップ】 WAIT / STOP の要求を処理する。

    走行中で速度が min_speed 以上ならソフトストップ（減速して止まる）を始め、
    それ以外は即停止する。止まった合図 DONE: は halt() が送る。
    """
    name = "WAIT" if target == RunMode.WAIT else "STOP"
    ss = st.soft

    # 減速中に来た要求
    if ss.active:
        if target == RunMode.STOP and ss.target == RunMode.STOP:
            send("OK:STOP")
            halt(devices, st, RunMode.STOP)         # STOP の 2 回目 = 非常停止（即停止）
        elif target == RunMode.STOP:
            ss.target = RunMode.STOP                # WAIT 減速中に STOP → STOP へ切り替え
            devices.hub.light.on(Color.RED)
            send("OK:STOP")
        elif ss.target == RunMode.STOP:
            send("NG:STOPPING")                     # STOP 減速中の WAIT は受け付けない
        else:
            send("OK:WAIT")
        return

    # すでに待機中
    if st.run == RunMode.WAIT and target == RunMode.WAIT:
        send("OK:WAIT")
        return

    use_soft = config.soft.on_wait if target == RunMode.WAIT else config.soft.on_stop
    if st.run == RunMode.RUN and use_soft and st.speed.current >= config.soft.min_speed:
        ss.active = True
        ss.target = target
        ss.ceiling = st.speed.current
        ss.start_ms = devices.clock.time()
        devices.hub.light.on(Color.YELLOW if target == RunMode.WAIT else Color.RED)
        send("OK:" + name)
        debug_phase(config, "ソフトストップ開始 " + name)
    else:
        send("OK:" + name)
        halt(devices, st, target)


def apply_soft_stop(devices, config, st, speed, dt):
    """【機能: ソフトストップ】 減速中なら速度に上限をかけ、0 になったら止める。上限をかけた速度を返す。

    ライン追従（旋回）はそのまま続くので、線から外れずに減速できる。
    直角カーブの旋回中（PIVOT）は旋回が終わるまで止めない（timeout_ms で強制停止）。
    """
    ss = st.soft
    if not ss.active:
        return speed

    ss.ceiling = max(0.0, ss.ceiling - config.soft.decel * dt)
    speed = min(speed, ss.ceiling)

    timed_out = devices.clock.time() - ss.start_ms > config.soft.timeout_ms
    if timed_out or (ss.ceiling <= 0 and st.phase != Phase.PIVOT):
        debug_phase(config, "ソフトストップ完了")
        halt(devices, st, ss.target)
    return speed


def apply_command(cmd, devices, config, st):
    """【機能: Pi 通信】 Pi からのコマンドを反映して応答を返す。"""
    if cmd == b"RUN":
        if st.run != RunMode.RUN:
            reset_motion(devices, st)
        st.soft.active = False              # 【機能: ソフトストップ】 減速中なら取り消して走り続ける
        st.run = RunMode.RUN
        devices.hub.light.on(Color.GREEN)
        send("OK:RUN")
    elif cmd == b"WAIT":
        request_stop(devices, config, st, RunMode.WAIT)
    elif cmd == b"STOP":
        request_stop(devices, config, st, RunMode.STOP)
    else:
        send("NG:UNKNOWN")


# =================================================
# 自動キャリブレーション
# =================================================

def sweep_to(devices, config, receiver, st, target, left_range, right_range):
    """【機能: 自動キャリブレーション】 target 角度まで回りながら反射光の最小/最大を記録する。STOP が来たら False を返す。"""
    cc = config.cal
    robot = devices.robot
    start_ms = devices.clock.time()
    limit_ms = int(abs(target - robot.angle()) / cc.turn_rate * 2000) + 1500

    while True:
        cmd = receiver.read()
        if cmd == b"STOP":                  # 【機能: Pi 通信】 STOP だけは測定中でも受け付ける
            st.run = RunMode.STOP
            send("OK:STOP")
            send("DONE:STOP")
            return False
        elif cmd is not None:
            send("NG:BUSY")                 # キャリブレーション中は STOP 以外を受け付けない

        left_range.update(devices.left_sensor.reflection())
        right_range.update(devices.right_sensor.reflection())

        remaining = target - robot.angle()
        if abs(remaining) <= cc.tolerance_deg:
            return True
        if devices.clock.time() - start_ms > limit_ms:
            return True

        rate = clamp(abs(remaining) * 3, cc.min_rate, cc.turn_rate)
        robot.drive(0, rate if remaining > 0 else -rate)
        wait(config.loop.wait_ms)


def auto_calibrate(devices, config, receiver, st):
    """【機能: 自動キャリブレーション】 その場で左右に車体を振り、黒・白の反射光を自動測定する。

    線を 2 つのセンサーの真ん中にした状態で呼ぶ。右へ振ると左センサーが、
    左へ振ると右センサーが線を横切るので、各センサーの最小=黒 / 最大=白 になる。
    コントラスト不足なら振り幅を広げて再試行し、それでも駄目なら既定値を使う。
    """
    cc = config.cal
    cal = Calibration(
        left_white=cc.default_left_white,
        left_black=cc.default_left_black,
        right_white=cc.default_right_white,
        right_black=cc.default_right_black,
    )
    if not cc.auto:
        return cal

    robot = devices.robot
    swing = cc.swing_deg

    for attempt in range(cc.max_retries + 1):
        left_range = SensorRange()
        right_range = SensorRange()
        robot.reset()           # 現在の向きを 0 度にする（stop も呼ばれる）

        for target in (swing, -swing, 0):
            if not sweep_to(devices, config, receiver, st, target, left_range, right_range):
                robot.brake()
                return cal
        robot.brake()

        if left_range.contrast() >= cc.min_contrast and right_range.contrast() >= cc.min_contrast:
            cal.left_black = left_range.low
            cal.left_white = left_range.high
            cal.right_black = right_range.low
            cal.right_white = right_range.high
            cal.ok = True
            break

        swing += cc.swing_step_deg      # 線を横切れていない可能性 → 振り幅を広げる

    return cal


# =================================================
# 走行処理: 直角カーブ
# =================================================

def begin_pivot(devices, config, st):
    """【機能: 直角カーブ】 前進を止めて旋回を始める。"""
    st.corner.start_angle = devices.robot.angle()
    st.phase = Phase.PIVOT
    debug_phase(config, "旋回開始 side=" + str(st.corner.side))


def finish_corner(devices, config, st, distance):
    """【機能: 直角カーブ】 直角カーブを終えて PID に戻す。直後は誤作動しないよう減速を続け、判定も止める。"""
    st.phase = Phase.TRACE
    reset_pid(st.pid)
    st.speed.current = 0.0
    force_curve(st.curve)
    st.corner.cooldown_until_mm = distance + config.corner.cooldown_mm
    reset_lost_tracking(st.lost)            # 【機能: ロスト復帰】 旋回前の追跡は無効
    debug_phase(config, "旋回終了 angle=" + str(int(devices.robot.angle() - st.corner.start_angle)))


def step_pivot(devices, config, st, distance):
    """【機能: 直角カーブ】 超信地旋回。前進はせず、target_angle - exit_margin まで回ったら PID に戻す。"""
    corner = config.corner
    turned = (devices.robot.angle() - st.corner.start_angle) * st.corner.side
    limit = corner.target_angle - corner.exit_margin
    timed_out = devices.clock.time() - st.corner.start_ms > corner.pivot_timeout_ms

    if turned >= limit or timed_out:
        finish_corner(devices, config, st, distance)
        return 0.0, 0.0

    # 目標が近づいたら徐々に遅くして止まり際のオーバーシュートを減らす
    rate = clamp((limit - turned) * 4, corner.pivot_min_rate, corner.pivot_rate)
    return 0.0, st.corner.side * rate


def step_advance(devices, config, st, distance):
    """【機能: 直角カーブ】 旋回の前に、車軸を角の頂点へ寄せる（直進）。"""
    corner = config.corner
    if distance - st.corner.advance_start_mm >= corner.advance_mm:
        begin_pivot(devices, config, st)
        return 0.0, 0.0
    return corner.advance_speed, 0.0


# =================================================
# 走行処理: 十字路
# =================================================

def step_cross(config, st, left, right, distance):
    """【機能: 十字路】 十字路をまっすぐ通過する。両センサーが黒を抜けた後も exit_mm だけ直進。"""
    cross = config.cross
    if is_both_black(left, right, cross.black_threshold):
        st.cross.exit_start_mm = None
    elif st.cross.exit_start_mm is None:
        st.cross.exit_start_mm = distance
    elif distance - st.cross.exit_start_mm >= cross.exit_mm:
        st.phase = Phase.TRACE
        reset_pid(st.pid)
        st.speed.current = cross.speed
        st.corner.cooldown_until_mm = distance + config.corner.cooldown_mm
        reset_lost_tracking(st.lost)        # 【機能: ロスト復帰】 十字路の黒は追跡しない
        debug_phase(config, "十字路通過")
    return cross.speed, 0.0


# =================================================
# 走行処理: ロスト復帰（探索）
# =================================================

def begin_search(devices, config, st, side):
    """【機能: ロスト復帰】 探索を始める。side は線が逃げた向き（-1 左 / +1 右）。"""
    ls = st.lost
    ls.side = side
    ls.stage = SearchStage.TURN
    ls.leg = 0
    ls.retry = 0
    ls.base_angle = devices.robot.angle()
    ls.start_ms = devices.clock.time()
    st.phase = Phase.SEARCH
    devices.hub.light.on(Color.ORANGE)
    send("LOST:" + ("L" if side < 0 else "R"))
    debug_phase(config, "ロスト検出 side=" + str(side))


def finish_search(devices, config, st, distance):
    """【機能: ロスト復帰】 線を見つけたので PID に戻る。直後は減速して判定も止める。"""
    st.phase = Phase.TRACE
    reset_pid(st.pid)
    st.speed.current = 0.0
    force_curve(st.curve)
    st.corner.cooldown_until_mm = distance + config.corner.cooldown_mm
    reset_lost_tracking(st.lost)
    devices.hub.light.on(Color.GREEN)
    send("FOUND")
    debug_phase(config, "線を発見")


def give_up_search(devices, config, st):
    """【機能: ロスト復帰】 見つからなかったので Pi に知らせて待機状態にする。"""
    st.phase = Phase.TRACE
    reset_lost_tracking(st.lost)
    send("LOST:GIVEUP")
    debug_phase(config, "探索を断念")
    halt(devices, st, RunMode.WAIT)


def search_leg_target(lc, ls):
    """【機能: ロスト復帰】 ls.leg 回目の振りの目標角度。逃げた側 → 反対側 を、振り幅を広げて繰り返す。"""
    widen = 1 + ls.leg // 2                 # 0,1 回目: ±1 刻み / 2,3 回目: ±2 刻み
    direction = ls.side if ls.leg % 2 == 0 else -ls.side
    return ls.base_angle + direction * lc.search_deg * widen


def step_search(devices, config, st, left, right, distance):
    """【機能: ロスト復帰】 線を探す。逃げた側から左右にその場回転 → 戻る → 少し前進 → 再探索。"""
    lc = config.lost
    ls = st.lost
    robot = devices.robot

    # --- 見つけた？（どちらかのセンサーが暗くなった） ---
    if left < lc.found_level or right < lc.found_level:
        finish_search(devices, config, st, distance)
        return 0.0, 0.0

    # --- 探索全体の制限時間 ---
    if devices.clock.time() - ls.start_ms > lc.timeout_ms:
        give_up_search(devices, config, st)
        return 0.0, 0.0

    if ls.stage == SearchStage.CREEP:
        # 少し前進して、同じ手順で探し直す
        if distance - ls.creep_start_mm >= lc.creep_mm:
            ls.retry += 1
            if ls.retry > lc.retries:
                give_up_search(devices, config, st)
                return 0.0, 0.0
            ls.stage = SearchStage.TURN
            ls.leg = 0
            ls.base_angle = robot.angle()
            return 0.0, 0.0
        return lc.creep_speed, 0.0

    # TURN: 各振りの目標角度へ / BACK: 探索開始時の向きへ
    if ls.stage == SearchStage.TURN:
        target = search_leg_target(lc, ls)
    else:
        target = ls.base_angle
    remaining = target - robot.angle()

    if abs(remaining) <= lc.search_tolerance_deg:
        if ls.stage == SearchStage.TURN:
            ls.leg += 1
            if ls.leg >= lc.search_legs:
                ls.stage = SearchStage.BACK
        else:
            ls.stage = SearchStage.CREEP
            ls.creep_start_mm = distance
        return 0.0, 0.0

    rate = clamp(abs(remaining) * 3, lc.search_min_rate, lc.search_rate)
    return 0.0, rate if remaining > 0 else -rate


# =================================================
# 走行処理: 通常トレース（PID / カーブ減速）と直角カーブの確認
# =================================================

def step_trace(devices, config, st, left, right, error, distance, dt):
    """【機能: PID 制御】 通常ライントレース。【直角カーブ】の確認・検出、【ロスト復帰】の検出も行う。"""
    corner = config.corner
    update_last_white(left, right, distance, corner, st.corner)

    # --- 【機能: ロスト復帰】 検出（通常トレース中だけ。直角カーブ・十字路の直後は判定しない） ---
    if st.phase == Phase.TRACE and config.lost.enabled:
        if distance >= st.corner.cooldown_until_mm:
            side = update_lost(left, right, distance, corner, config.lost, st.lost)
            if side != 0:
                begin_search(devices, config, st, side)
                return 0.0, 0.0
        else:
            reset_lost_tracking(st.lost)

    # --- 【機能: 直角カーブ】 候補の確認中：減速してまっすぐ進む（旋回しながらだと角から外れるため） ---
    if st.phase == Phase.PROBE:
        if st.corner.side < 0:
            black_value, other_value = left, right
        else:
            black_value, other_value = right, left

        if black_value < corner.black_on:
            st.corner.reached_black = True

        timed_out = devices.clock.time() - st.corner.start_ms > corner.probe_timeout_ms
        if other_value < corner.white_hold or timed_out:
            # 反対側も暗くなった = 斜めに入った十字路など。取り消して通常のトレースへ
            st.phase = Phase.TRACE
            reset_pid(st.pid)
            debug_phase(config, "直角候補を取り消し（反対側が暗い / 時間切れ）")
        elif distance - st.corner.start_mm >= corner.confirm_mm:
            if not st.corner.reached_black:
                st.phase = Phase.TRACE
                reset_pid(st.pid)
                debug_phase(config, "直角候補を取り消し（深い黒にならない）")
            else:
                debug_phase(config, "直角カーブ確定 side=" + str(st.corner.side))
                if corner.advance_mm > 0:
                    st.corner.advance_start_mm = distance
                    st.phase = Phase.ADVANCE
                    return corner.advance_speed, 0.0
                begin_pivot(devices, config, st)
                return 0.0, 0.0
        else:
            speed = ramp_speed(st.speed, corner.probe_speed, dt, config.speed)
            return speed, 0.0

    # --- 【機能: 直角カーブ】 候補の検出（急に深い黒になったときだけ。直線のはみ出しでは発動しない） ---
    elif corner.enabled and distance >= st.corner.cooldown_until_mm:
        side = detect_corner_side(left, right, distance, corner, st.corner)
        if side != 0:
            st.phase = Phase.PROBE
            st.corner.side = side
            st.corner.start_mm = distance
            st.corner.start_ms = devices.clock.time()
            st.corner.reached_black = False
            force_curve(st.curve)
            reset_lost_tracking(st.lost)    # 【機能: ロスト復帰】 角の黒は追跡しない
            debug_phase(config, "直角候補 side=" + str(side))
            speed = ramp_speed(st.speed, corner.probe_speed, dt, config.speed)
            return speed, 0.0

    # --- 【機能: PID 制御】 通常の PID 追従 ---
    turn_rate = calc_pid(st.pid, error, dt, config.pid)

    # --- 【機能: カーブ減速】 カーブ中か判定して速度を決める ---
    changed = update_curve(st.curve, error, distance, dt, config.curve)
    if changed > 0:
        debug_phase(config, "カーブ突入")
    elif changed < 0:
        debug_phase(config, "カーブ脱出")
    target = calc_target_speed(config.speed, st.curve, error)
    speed = ramp_speed(st.speed, target, dt, config.speed)
    return speed, turn_rate


def drive_step(devices, config, cal, st, dt):
    """【共通】 走行 1 ステップ。フェーズごとの処理を呼ぶ。表示用に (left, right, error, speed, turn_rate) を返す。"""
    left, right = read_sensors(devices, cal)
    distance = devices.robot.distance()
    error = calc_error(left, right)

    # --- 【機能: 十字路】 左右とも黒は直角カーブ判定より優先する ---
    if st.phase in (Phase.TRACE, Phase.PROBE):
        if is_both_black(left, right, config.cross.black_threshold):
            st.phase = Phase.CROSS
            st.cross.exit_start_mm = None
            reset_lost_tracking(st.lost)    # 【機能: ロスト復帰】
            debug_phase(config, "十字路検出 L:" + str(int(left)) + " R:" + str(int(right)))

    # --- フェーズごとの処理 ---
    if st.phase == Phase.PIVOT:
        speed, turn_rate = step_pivot(devices, config, st, distance)             # 【直角カーブ】
    elif st.phase == Phase.ADVANCE:
        speed, turn_rate = step_advance(devices, config, st, distance)           # 【直角カーブ】
    elif st.phase == Phase.CROSS:
        speed, turn_rate = step_cross(config, st, left, right, distance)         # 【十字路】
    elif st.phase == Phase.SEARCH:
        speed, turn_rate = step_search(devices, config, st, left, right, distance)   # 【ロスト復帰】
    else:
        speed, turn_rate = step_trace(devices, config, st, left, right, error, distance, dt)   # 【PID / カーブ減速】

    # --- 【機能: ソフトストップ】 WAIT / STOP 要求中は速度に上限をかける（旋回は続けて線上を保つ） ---
    speed = apply_soft_stop(devices, config, st, speed, dt)
    if st.run != RunMode.RUN:
        # ソフトストップ完了 / ロスト断念で止まった。drive() で上書きしない
        return left, right, error, 0.0, 0.0

    st.speed.current = speed
    devices.robot.drive(speed, turn_rate)
    return left, right, error, speed, turn_rate


# =================================================
# デバッグ表示
# =================================================

def debug_print(debug, left, right, error, speed, turn_rate):
    """【機能: デバッグ表示】 Debug で True になっている値だけを 1 行にまとめて表示する。"""
    items = []
    if debug.left:
        items.append("L:" + str(int(left)))
    if debug.right:
        items.append("R:" + str(int(right)))
    if debug.error:
        items.append("err:" + str(int(error)))
    if debug.speed:
        items.append("spd:" + str(int(speed)))
    if debug.turn_rate:
        items.append("turn:" + str(int(turn_rate)))
    if items:
        print(" ".join(items))


# =================================================
# メイン
# =================================================

def main():
    config = Config()
    devices = Devices(config.hw)
    receiver = CommandReceiver()                # 【機能: Pi 通信】
    st = State()

    # --- 【機能: 自動キャリブレーション】 完了後に READY を送る ---
    devices.hub.light.on(Color.BLUE)
    cal = auto_calibrate(devices, config, receiver, st)

    if st.run != RunMode.STOP:
        send(
            "CAL:" + ("OK" if cal.ok else "DEFAULT") + ","
            + str(cal.left_white) + "," + str(cal.left_black) + ","
            + str(cal.right_white) + "," + str(cal.right_black)
        )
        st.run = RunMode.WAIT
        devices.hub.light.on(Color.YELLOW)
        send("READY")

    # --- メインループ ---
    loop_timer = StopWatch()
    debug_timer = StopWatch()

    while st.run != RunMode.STOP:
        # 【機能: Pi 通信】 コマンドを受け取る（RUN / WAIT / STOP）
        cmd = receiver.read()
        if cmd is not None:
            apply_command(cmd, devices, config, st)
            if st.run == RunMode.STOP:
                break

        dt = loop_timer.time() / 1000
        loop_timer.reset()

        # RUN 中だけ走行処理（ソフトストップの減速中も RUN のまま）
        if st.run == RunMode.RUN:
            left, right, error, speed, turn_rate = drive_step(devices, config, cal, st, dt)
            if debug_timer.time() >= config.debug.interval_ms:
                debug_print(config.debug, left, right, error, speed, turn_rate)     # 【機能: デバッグ表示】
                debug_timer.reset()

        wait(config.loop.wait_ms)

    devices.robot.brake()
    devices.hub.light.on(Color.RED)
    print("完全停止しました")


main()
