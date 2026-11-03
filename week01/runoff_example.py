"""
第 1 週範例：線性水庫降雨逕流模擬，並拿輸出對理論值。

名詞（第一次出現先定義）：
- 逕流：降雨落到流域後，流向河道出口的水。
- 線性水庫：把整個流域想成一個水桶，桶裡的水量 S 以固定比例流出：Q = S / k。
  k 叫「退水常數」，單位小時：雨停之後，流量每過 k 小時降為原來的 1/e（約 37%）。
- 逕流係數 C：降雨有多少比例變成河道流量（其餘被蒸發、滲入地下）。

模型：dS/dt = C * A * P(t) - Q(t)，    Q(t) = S(t) / k
      P：雨量 [mm/hr]，A：流域面積 [km^2]，Q：流量 [m3/s]
時間用顯式前進歐拉往前推（每步用「現在的 S」算出下一步的 S）。

執行：python week01/runoff_example.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# 0. 參數集中放在最上面
# ---------------------------------------------------------------------------
START = "2026-01-01"
DAYS = 60                 # 模擬天數
FREQ = "h"                # 取樣頻率：每小時一筆
AREA_KM2 = 120.0          # 流域面積 [km^2]
K_HOURS = 20.0            # 退水常數 [hr]
RUNOFF_COEF = 0.4         # 逕流係數 C
BASEFLOW = 2.0            # 基流 [m3/s]：沒下雨時河裡仍有的水
NOISE_STD = 1.0           # 流量計量測雜訊標準差 [m3/s]
SEED = 42                 # 亂數種子：固定它，每次跑出來的結果才會一樣（可重現性）

OUT_DIR = Path(__file__).parent


# ---------------------------------------------------------------------------
# 1. 產生資料
# ---------------------------------------------------------------------------
def make_rain(start: str, days: int, freq: str, seed: int) -> pd.Series:
    """隨機產生雨量序列 [mm/hr]：大約每 4 天一場暴雨，半個正弦波形。"""
    rng = np.random.default_rng(seed)
    n = days * 24
    time = pd.date_range(start=start, periods=n, freq=freq)
    rain = np.zeros(n)
    i = 0
    while i < n - 12:
        i += int(rng.integers(48, 144))          # 兩場雨相隔 2–6 天
        dur = int(rng.integers(4, 9))            # 一場雨持續 4–8 小時
        amp = rng.uniform(5, 14)                 # 最大雨強 5–14 mm/hr
        if i + dur < n:
            rain[i:i + dur] += amp * np.sin(np.pi * (np.arange(dur) + 0.5) / dur)
    return pd.Series(rain, index=time, name="rain_mm_h")


def simulate_flow(rain: pd.Series) -> pd.Series:
    """線性水庫：由雨量算流量 [m3/s]（不含雜訊）。"""
    # mm/hr 換成 m3/s：1 mm 深 × 1 km^2 = 1000 m^3；1 hr = 3600 s
    inflow = RUNOFF_COEF * rain.values * AREA_KM2 * 1000 / 3600
    s = 0.0                                       # 蓄水量，單位 m3
    q = np.zeros(len(rain))
    for i in range(len(rain)):
        q[i] = s / (K_HOURS * 3600) + BASEFLOW
        s += 3600 * (inflow[i] - s / (K_HOURS * 3600))     # 每步 1 小時 = 3600 秒
    return pd.Series(q, index=rain.index, name="q_m3s")


def add_noise(q: pd.Series, seed: int) -> pd.Series:
    rng = np.random.default_rng(seed + 1)
    return q + rng.normal(0.0, NOISE_STD, size=len(q))


# ---------------------------------------------------------------------------
# 2. 統計：每小時資料 → 每日統計
# ---------------------------------------------------------------------------
def daily_stats(q: pd.Series) -> pd.DataFrame:
    """每日最大、最小、平均流量。"""
    # resample("D") 把資料依「日」分組，類似 Excel 樞紐分析。
    return q.resample("D").agg(["max", "min", "mean"])


# ---------------------------------------------------------------------------
# 3. 拿理論值檢查：這些檢查在你改程式之後仍然要成立
# ---------------------------------------------------------------------------
def pulse_recession_ratio() -> float:
    """理論：雨停後經過 k 小時，（流量 - 基流）降為原來的 1/e = 0.368。
    做法：只下 1 小時雨，量 k 小時後與 1 小時後的比值。"""
    rain = pd.Series(np.zeros(120), index=pd.date_range(START, periods=120, freq=FREQ))
    rain.iloc[0] = 10.0
    q = simulate_flow(rain) - BASEFLOW
    return float(q.iloc[1 + int(K_HOURS)] / q.iloc[1])


def volume_ratio(rain: pd.Series, q: pd.Series) -> float:
    """理論：流出的總水量 ≈ C × 降雨總水量（差在期末還留在流域裡的水）。"""
    rain_vol = rain.sum() * AREA_KM2 * 1000               # m3
    flow_vol = (q - BASEFLOW).sum() * 3600                # m3
    return float(flow_vol / (RUNOFF_COEF * rain_vol))


# ---------------------------------------------------------------------------
# 4. 畫圖
# ---------------------------------------------------------------------------
def plot_overview(rain: pd.Series, q_true: pd.Series, q_obs: pd.Series, daily: pd.DataFrame, path: Path) -> None:
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    ax1.bar(rain.index, rain.values, width=0.04, color="#1f5f8b")
    ax1.set_ylabel("Rain [mm/hr]")
    ax2.plot(q_obs.index, q_obs.values, lw=0.6, color="#8fb8d0", label="observed (noisy)")
    ax2.plot(q_true.index, q_true.values, lw=1.0, color="#1f5f8b", label="model (no noise)")
    ax2.plot(daily.index, daily["max"], "o", ms=3, color="#d9822b", label="daily max")
    ax2.set_ylabel("Discharge [m3/s]")
    ax2.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 5. 主程式
# ---------------------------------------------------------------------------
def main() -> None:
    rain = make_rain(START, DAYS, FREQ, SEED)
    q_true = simulate_flow(rain)
    q_obs = add_noise(q_true, SEED)
    daily = daily_stats(q_obs)
    daily_true = daily_stats(q_true)

    print(daily.head(5).round(2))
    print()
    print(f"退水檢查：k 小時後剩 {pulse_recession_ratio():.3f}（理論 e^-1 = 0.368）")
    print(f"水量檢查：流出水量 / (C × 降雨水量) = {volume_ratio(rain, q_true):.3f}（理論約 1）")
    bias = (daily["max"] - daily_true["max"]).mean()
    print(f"日最大流量：含雜訊比無雜訊平均高 {bias:+.2f} m3/s（雜訊標準差 {NOISE_STD} m3/s）")

    daily.to_csv(OUT_DIR / "daily_stats.csv")
    plot_overview(rain, q_true, q_obs, daily, OUT_DIR / "runoff_overview.png")
    print("\n已輸出 daily_stats.csv 與 runoff_overview.png")


if __name__ == "__main__":
    main()
