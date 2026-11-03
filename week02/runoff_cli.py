"""
第 2 週範例 1／2：把降雨逕流模型變成「命令列工具」
=====================================================

第 1 週的程式要改參數，得打開檔案改常數。這週把參數改成從命令列傳入，
一次執行 = 一次「實驗」，每次實驗的設定與結果都存進自己的資料夾。

為什麼要這樣做：
  - 批次實驗、排程、容器、API 都是「用參數呼叫一支程式」，這是它們共同的最小單位。
  - 設定（config.json）和結果（metrics.json）放在一起，三個月後還查得到「這張圖是怎麼跑出來的」。

和第 1 週的差別（請對照）：
  1. 時間步長 dt 從時間軸算出實際的小時數，雨量也用「實際經過的小時數」產生。
     不管 --freq 是 "10min" 還是 "30min"，結果都對；第 1 週把 dt 與筆數寫死的陷阱在這裡修好。
  2. 參數檢查失敗時以非 0 的結束碼（exit code）離開，批次腳本才知道這次失敗了。
     顯式前進歐拉要求 dt < 2k，否則計算會發散，所以這也是一項參數檢查。

執行範例：
  python runoff_cli.py --k-hours 1.2 --out runs/demo
  python runoff_cli.py --k-hours 2.4 --freq 30min --seed 7 --out runs/demo2
  python runoff_cli.py --help
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

AREA_KM2 = 52.77   # 流域面積 [km^2]：鯉魚潭水庫集水區
BASEFLOW = 1.18    # 基流 [m3/s]


def parse_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="合成降雨逕流：隨機暴雨 → 線性水庫 → 流量，輸出設定與統計結果")
    p.add_argument("--k-hours", type=float, default=1.2, help="退水常數 k [hr]（預設 1.2）")
    p.add_argument("--runoff-coef", type=float, default=0.4, help="逕流係數 C，0 到 1（預設 0.4）")
    p.add_argument("--noise", type=float, default=0.08, help="流量計相對誤差標準差（預設 0.08，即 8%%）")
    p.add_argument("--days", type=int, default=60, help="模擬天數（預設 60）")
    p.add_argument("--freq", default="10min", help='取樣頻率，pandas 寫法，如 "10min"、"30min"（預設 "10min"）')
    p.add_argument("--seed", type=int, default=42, help="亂數種子（預設 42）")
    p.add_argument("--start", default="2026-08-01", help="開始日期（預設 2026-08-01）")
    p.add_argument("--out", required=True, help="輸出資料夾，例如 runs/k_20")
    return p.parse_args(argv)


def step_hours(freq: str) -> float:
    """取樣間隔，單位小時。"""
    return pd.tseries.frequencies.to_offset(freq).nanos / 3.6e12


def validate(a: argparse.Namespace) -> list[str]:
    """回傳錯誤訊息清單；空清單代表參數合理。"""
    errors = []
    dt = step_hours(a.freq)
    if a.k_hours <= 0:
        errors.append("退水常數 k 必須大於 0")
    elif a.k_hours < 2 * dt:
        errors.append(f"k = {a.k_hours} hr 小於 2 倍步長（{2 * dt} hr），顯式計算會發散")
    if not 0 <= a.runoff_coef <= 1:
        errors.append("逕流係數必須在 0 到 1 之間")
    if a.noise < 0:
        errors.append("雜訊標準差不能是負數")
    if a.days < 10:
        errors.append("天數至少 10 天，才有足夠的暴雨事件")
    return errors


def make_rain(t_hours: np.ndarray, seed: int, days: int) -> np.ndarray:
    """雨強 [mm/hr]。暴雨的時間與大小由 seed 決定，與取樣頻率無關。"""
    rng = np.random.default_rng(seed)
    rain = np.zeros(len(t_hours))
    start = 0.0
    while True:
        start += rng.integers(48, 144)           # 兩場雨相隔 2–6 天
        dur, amp = rng.uniform(1.5, 4.0), rng.uniform(10, 30)     # 歷時 1.5–4 小時，最大雨強 10–30 mm/hr
        if start + dur >= days * 24:
            break
        inside = (t_hours >= start) & (t_hours < start + dur)
        rain[inside] += amp * np.sin(np.pi * (t_hours[inside] - start) / dur)
    return rain


def simulate_flow(rain: np.ndarray, k_hours: float, c: float, dt_h: float) -> np.ndarray:
    """線性水庫，顯式前進歐拉。回傳流量 [m3/s]。"""
    inflow = c * rain * AREA_KM2 * 1000 / 3600           # m3/s
    s, q = 0.0, np.zeros(len(rain))
    for i in range(len(rain)):
        q[i] = s / (k_hours * 3600) + BASEFLOW
        s += dt_h * 3600 * (inflow[i] - s / (k_hours * 3600))
    return q


def recession_ratio(k_hours: float, dt_h: float) -> float:
    """脈衝測試：雨停後經過 k 小時，（流量 - 基流）剩下的比例。理論值 e^-1 = 0.368。"""
    n = int(k_hours / dt_h) + 3
    rain = np.zeros(n)
    rain[0] = 10.0 / dt_h
    q = simulate_flow(rain, k_hours, 0.4, dt_h) - BASEFLOW
    return float(q[1 + int(round(k_hours / dt_h))] / q[1])


def build(a: argparse.Namespace) -> tuple[pd.Series, pd.Series, pd.Series]:
    time = pd.date_range(start=a.start, end=pd.Timestamp(a.start) + pd.Timedelta(days=a.days),
                         freq=a.freq, inclusive="left")
    dt_h = step_hours(a.freq)
    t_hours = np.asarray((time - time[0]) / pd.Timedelta(hours=1), dtype=float)

    rain = make_rain(t_hours, a.seed, a.days)
    q_true = simulate_flow(rain, a.k_hours, a.runoff_coef, dt_h)
    rng = np.random.default_rng(a.seed + 1)
    q_obs = q_true * (1 + rng.normal(0.0, a.noise, size=len(time)))     # 乘性誤差
    return (pd.Series(rain, index=time, name="rain_mm_h"),
            pd.Series(q_true, index=time, name="q_true_m3s"),
            pd.Series(q_obs, index=time, name="q_obs_m3s"))


def summarize(rain: pd.Series, q_true: pd.Series, q_obs: pd.Series, a: argparse.Namespace) -> dict:
    dt_h = step_hours(a.freq)
    rain_vol = rain.sum() * dt_h * AREA_KM2 * 1000
    flow_vol = (q_true - BASEFLOW).sum() * dt_h * 3600
    return {
        "n_samples": int(len(q_obs)),
        "peak_true_m3s": round(float(q_true.max()), 3),
        "peak_obs_m3s": round(float(q_obs.max()), 3),
        "volume_ratio": round(float(flow_vol / (a.runoff_coef * rain_vol)), 4),
        "theory_volume_ratio": 1.0,
        "recession_ratio": round(recession_ratio(a.k_hours, dt_h), 4),
        "theory_recession_ratio": round(float(np.exp(-1)), 4),
    }


def main(argv=None) -> int:
    a = parse_args(argv)
    errors = validate(a)
    if errors:
        for e in errors:
            print(f"參數錯誤：{e}", file=sys.stderr)  # 錯誤訊息寫到 stderr，不混進正常輸出
        return 2  # 非 0 結束碼 = 失敗；慣例上 2 代表「參數用錯」

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    rain, q_true, q_obs = build(a)
    metrics = summarize(rain, q_true, q_obs, a)

    config = {k: v for k, v in vars(a).items() if k != "out"}
    (out / "config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    pd.concat([rain, q_true, q_obs], axis=1).to_csv(out / "flow.csv", float_format="%.4f")

    print(json.dumps(metrics, ensure_ascii=False))  # 一行 JSON，方便其他程式讀
    return 0


if __name__ == "__main__":
    sys.exit(main())
