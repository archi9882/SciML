"""
第 2 週範例 1／2：把潮位模型變成「命令列工具」
=================================================

第 1 週的程式要改參數，得打開檔案改常數。這週把參數改成從命令列傳入，
一次執行 = 一次「實驗」，每次實驗的設定與結果都存進自己的資料夾。

為什麼要這樣做：
  - 批次實驗、排程、容器、API 都是「用參數呼叫一支程式」，這是它們共同的最小單位。
  - 設定（config.json）和結果（metrics.json）放在一起，三個月後還查得到「這張圖是怎麼跑出來的」。

和第 1 週的差別（請對照）：
  1. 時間軸改用「實際經過的小時數」計算，修正第 1 週 Day 2 Q1 的單位陷阱：
     不管 --freq 是 "h" 還是 "30min"，分潮週期都正確。
  2. 參數檢查失敗時以非 0 的結束碼（exit code）離開，批次腳本才知道這次失敗了。

執行範例：
  python tide_cli.py --s2-amp 0.45 --out runs/demo
  python tide_cli.py --s2-amp 1.0 --freq 30min --seed 7 --out runs/demo2
  python tide_cli.py --help
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

M2_PERIOD = 12.42  # 主太陰半日潮週期 [hr]
S2_PERIOD = 12.00  # 主太陽半日潮週期 [hr]


def parse_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="合成潮位：M2 + S2 + 雜訊，輸出設定與統計結果")
    p.add_argument("--m2-amp", type=float, default=1.00, help="M2 振幅 [m]（預設 1.00）")
    p.add_argument("--s2-amp", type=float, default=0.45, help="S2 振幅 [m]（預設 0.45）")
    p.add_argument("--msl", type=float, default=0.20, help="平均海水面 [m]（預設 0.20）")
    p.add_argument("--noise", type=float, default=0.05, help="雜訊標準差 [m]（預設 0.05）")
    p.add_argument("--days", type=int, default=60, help="模擬天數（預設 60）")
    p.add_argument("--freq", default="h", help='取樣頻率，pandas 寫法，如 "h"、"30min"（預設 "h"）')
    p.add_argument("--seed", type=int, default=42, help="亂數種子（預設 42）")
    p.add_argument("--start", default="2026-01-01", help="開始日期（預設 2026-01-01）")
    p.add_argument("--out", required=True, help="輸出資料夾，例如 runs/s2_0.45")
    return p.parse_args(argv)


def validate(a: argparse.Namespace) -> list[str]:
    """回傳錯誤訊息清單；空清單代表參數合理。"""
    errors = []
    if a.m2_amp < 0 or a.s2_amp < 0:
        errors.append("振幅不能是負數")
    if a.noise < 0:
        errors.append("雜訊標準差不能是負數")
    if a.days < 15:
        errors.append("天數至少 15 天，才看得到一次完整的大小潮循環（約 14.8 天）")
    return errors


def make_tide(a: argparse.Namespace) -> pd.Series:
    time = pd.date_range(start=a.start, end=pd.Timestamp(a.start) + pd.Timedelta(days=a.days),
                         freq=a.freq, inclusive="left")
    # 關鍵修正：t 用「從開始經過的實際小時數」，而不是陣列索引 0, 1, 2, ...
    t_hours = (time - time[0]) / pd.Timedelta(hours=1)
    t_hours = np.asarray(t_hours, dtype=float)

    rng = np.random.default_rng(a.seed)
    m2 = a.m2_amp * np.cos(2 * np.pi * t_hours / M2_PERIOD)
    s2 = a.s2_amp * np.cos(2 * np.pi * t_hours / S2_PERIOD)
    noise = rng.normal(0.0, a.noise, size=len(time))
    return pd.Series(a.msl + m2 + s2 + noise, index=time, name="eta_m")


def summarize(eta: pd.Series, a: argparse.Namespace) -> dict:
    daily = eta.resample("D").agg(["max", "min"])
    daily_range = daily["max"] - daily["min"]
    return {
        "n_samples": int(len(eta)),
        "max_range_m": round(float(daily_range.max()), 4),
        "min_range_m": round(float(daily_range.min()), 4),
        "theory_max_range_m": round(2 * (a.m2_amp + a.s2_amp), 4),
        "theory_min_range_m": round(2 * abs(a.m2_amp - a.s2_amp), 4),
        "mean_level_m": round(float(eta.mean()), 4),
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

    eta = make_tide(a)
    metrics = summarize(eta, a)

    config = {k: v for k, v in vars(a).items() if k != "out"}
    (out / "config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    eta.to_csv(out / "eta.csv", float_format="%.4f")

    print(json.dumps(metrics, ensure_ascii=False))  # 一行 JSON，方便其他程式讀
    return 0


if __name__ == "__main__":
    sys.exit(main())
