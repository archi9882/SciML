"""
第 6 週範例：率定與驗證分開，以及水位流量曲線的外插風險。

名詞（第一次出現先定義）：
- 率定（calibration）：調整模型參數，讓模擬貼近一段「已知答案」的觀測。
- 驗證（validation）：用「沒有參與率定」的觀測檢查模型，看它描述的是不是真實。
- NSE（Nash–Sutcliffe 效率係數）：1 - Σ(觀測 - 模擬)² / Σ(觀測 - 觀測平均)²。
  1 為完美；0 表示不比「永遠猜觀測平均值」好；負數表示更差。
- 水位流量曲線（rating curve）：由實測的水位 h 與流量 Q 擬合出的關係，之後用水位推流量。

第一部分：用第 2 週的合成資料（真值已知：k = 1.2 hr、C = 0.4）率定降雨逕流模型，並分別在率定期與驗證期評分。
第二部分：用低水位的實測擬合水位流量曲線 Q = a h^b，外插到高水位，和 Manning 公式的結果比較。

執行：python week06/validation_example.py
"""
import argparse
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "week02"))
import runoff_cli as R  # noqa: E402  第 2 週的命令列工具，沿用它的雨量與流量產生器

SEED = 7


def nse(sim: np.ndarray, obs: np.ndarray) -> float:
    return float(1 - np.sum((obs - sim) ** 2) / np.sum((obs - obs.mean()) ** 2))


def make_data(rain_scale: float = 1.0):
    """用 runoff_cli 產生 60 天的雨量與含誤差的觀測流量（每 10 分鐘一筆）。"""
    a = argparse.Namespace(k_hours=1.2, runoff_coef=0.4, noise=0.08, days=60, freq="10min",
                           seed=SEED, start="2026-08-01")
    rain, q_true, q_obs = R.build(a)
    return rain.values * rain_scale, q_obs.values


def calibrate(rain: np.ndarray, q: np.ndarray) -> tuple[float, float]:
    """格點搜尋 k 與 C，使 RMSE 最小。"""
    best = (None, None, 1e18)
    for k in np.arange(0.6, 3.01, 0.2):
        for c in np.arange(0.2, 0.91, 0.05):
            sim = R.simulate_flow(rain, k, c, 1 / 6)
            rmse = float(np.sqrt(np.mean((sim - q) ** 2)))
            if rmse < best[2]:
                best = (float(k), float(c), rmse)
    return best[0], best[1]


def part1() -> None:
    print("第一部分：率定期與驗證期")
    for label, scale in [("雨量正確", 1.0), ("雨量只量到 60%", 0.6)]:
        rain, q = make_data(scale)
        half = len(q) // 2
        k, c = calibrate(rain[:half], q[:half])
        sim = R.simulate_flow(rain, k, c, 1 / 6)
        print(f"  {label}：率定得 k = {k:.1f} hr、C = {c:.2f}；"
              f"率定期 NSE = {nse(sim[:half], q[:half]):.3f}，驗證期 NSE = {nse(sim[half:], q[half:]):.3f}")


def manning_q(h: float, b: float = 20.0, s0: float = 0.004, n: float = 0.04) -> float:
    """矩形斷面的 Manning 流量 [m3/s]。"""
    a, p = b * h, b + 2 * h
    return a * (a / p) ** (2 / 3) * math.sqrt(s0) / n


def part2() -> None:
    print("第二部分：水位流量曲線的外插")
    rng = np.random.default_rng(3)
    h = np.sort(rng.uniform(0.2, 0.8, 20))
    q = np.array([manning_q(x) for x in h]) * (1 + rng.normal(0, 0.08, len(h)))
    b, ln_a = np.polyfit(np.log(h), np.log(q), 1)
    a = math.exp(ln_a)
    print(f"  實測水位 0.2–0.8 m，擬合 Q = {a:.1f} h^{b:.2f}（寬淺渠道的 Manning 理論指數是 5/3 = 1.67）")
    for hh in (0.5, 0.8, 1.2, 2.0):
        fit, true = a * hh ** b, manning_q(hh)
        tag = "（已實測範圍內）" if hh <= 0.8 else "（外插）"
        print(f"  h = {hh:.1f} m：曲線 {fit:6.1f} m3/s，Manning {true:6.1f} m3/s，差 {100 * (fit / true - 1):+5.1f}% {tag}")


if __name__ == "__main__":
    part1()
    print()
    part2()
