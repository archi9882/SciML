"""
第 1 週範例：用 Python 處理一條潮位時間序列
=================================================

學習目標（不要求背語法，要求看懂「每一段在做什麼、為什麼這樣做」）：
  1. numpy：用陣列一次算完整條時間序列（不用 for 迴圈）
  2. pandas：用時間索引做重採樣（每小時 → 每日）
  3. matplotlib：畫出可以放進報告的圖
  4. 函式：把重複的步驟包起來，之後批次實驗會一直用到

資料說明：
  這裡用「合成資料」，由兩個主要分潮（tidal constituent）組成，再加上雜訊。
  分潮是潮汐分析裡的術語：潮汐訊號可以拆成好幾個固定頻率的正弦波之和，
  每個分潮對應一種引起潮汐的天體週期性運動。這裡只用最主要的兩個：

    - M2（主太陰半日潮）：由月球引力造成。「半日」指一天潮起潮落兩次；
      週期 12.42 小時是「半個太陰日」，也就是月球相對地球自轉一圈
      （約 24.84 小時）的一半。通常是全球最強的分潮。

    - S2（主太陽半日潮）：機制跟 M2 相同，但換成太陽引力，因太陽距離遠，
      引力的潮汐效應較弱，振幅通常只有 M2 的三到五成。週期固定是
      12.00 小時（半個太陽日，正好是地球自轉一天的一半）。

  M2 和 S2 的週期很接近（12.42 對 12.00 小時）但不相等，疊加後兩個波
  會時而同相（互相加強 → 大潮 spring tide）、時而反相（互相抵消 →
  小潮 neap tide），形成約 14.8 天一次的大潮／小潮循環，對應到農曆
  朔望（新月、滿月）附近潮差最大，這也是水文／海洋學裡常聽到的現象。

  合成資料的好處是「真值已知」，可以檢查程式算得對不對。
  之後你可以把 make_tide() 換成讀真實潮位站資料（見 exercises.md 第 6 題）。

執行方式：
  python tide_example.py
  會在同一個資料夾輸出 tide_overview.png 與 daily_stats.csv
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# 0. 參數集中放在最上面
#    之後做「批次實驗」時，只要改這裡（或從命令列傳入），不用翻整支程式。
# ---------------------------------------------------------------------------
START = "2026-01-01"
DAYS = 60                 # 模擬天數
FREQ = "h"                # 取樣頻率：每小時一筆
M2_AMP, M2_PERIOD = 1.00, 12.42   # 主太陰半日潮：振幅 [m]、週期 [hr]（見上方說明）
S2_AMP, S2_PERIOD = 0.45, 12.00   # 主太陽半日潮：振幅 [m]、週期 [hr]（見上方說明）
MEAN_SEA_LEVEL = 0.20     # 平均海水面 [m]
NOISE_STD = 0.05          # 量測雜訊標準差 [m]
SEED = 50                 # 亂數種子：固定它，每次跑出來的結果才會一樣（可重現性）

OUT_DIR = Path(__file__).parent


# ---------------------------------------------------------------------------
# 1. 產生資料
# ---------------------------------------------------------------------------
def make_constituents(start: str, days: int, freq: str) -> pd.DataFrame:
    """回傳 M2、S2 兩個分潮的時間序列（單位 m），欄位為 m2、s2。"""
    # pd.date_range 產生時間軸；periods = 總筆數
    n = days * 24
    time = pd.date_range(start=start, periods=n, freq=freq)

    # t 是「從開始經過幾小時」，用來代入 cos()。
    # np.arange(n) 一次產生 [0, 1, 2, ..., n-1]，不用 for 迴圈。
    t = np.arange(n, dtype=float)

    # 每個分潮：A * cos(2π t / T)
    # 注意整條陣列一次運算，這叫「向量化」，是 numpy 快的原因。
    m2 = M2_AMP * np.cos(2 * np.pi * t / M2_PERIOD)
    s2 = S2_AMP * np.cos(2 * np.pi * t / S2_PERIOD)
    return pd.DataFrame({"m2": m2, "s2": s2}, index=time)

def make_tide(start: str, days: int, freq: str, seed: int) -> pd.Series:
    """回傳一條以時間為索引的潮位序列（單位 m）。"""
    rng = np.random.default_rng(seed)

    # 分潮改由 make_constituents 產生，畫圖時也能重複使用
    comp = make_constituents(start, days, freq)
    noise = rng.normal(0.0, NOISE_STD, size=len(comp))

    eta = MEAN_SEA_LEVEL + comp["m2"] + comp["s2"] + noise
    return pd.Series(eta.values, index=comp.index, name="eta_m")


# ---------------------------------------------------------------------------
# 2. 統計：每小時資料 → 每日統計
# ---------------------------------------------------------------------------
def daily_stats(eta: pd.Series) -> pd.DataFrame:
    """每日最高、最低、潮差。"""
    # resample("D") 把資料依「日」分組，類似 Excel 樞紐分析。
    daily = eta.resample("D").agg(["max", "min", "mean"])
    daily["range"] = daily["max"] - daily["min"]  # 潮差 = 高 - 低
    return daily


def theoretical_spring_neap_period() -> float:
    """大小潮週期（天）：兩個相近頻率的『拍頻』。

    f_beat = |1/T_M2 - 1/T_S2|，週期 = 1 / f_beat
    這是物理直覺可以檢查程式的地方：
    圖上看到的大潮間隔，應該要接近這個數字。
    """
    f_beat = abs(1 / M2_PERIOD - 1 / S2_PERIOD)  # 單位 1/hr
    return 1 / f_beat / 24                         # 換成天


# ---------------------------------------------------------------------------
# 3. 畫圖
# ---------------------------------------------------------------------------
def plot_overview(eta: pd.Series, daily: pd.DataFrame, comp: pd.DataFrame, path: Path) -> None:
    # 一張圖四個子圖，上下共用 x 軸（時間）；前兩列為原圖，後兩列為 M2、S2 分潮
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 10), sharex=True)

    ax1.plot(eta.index, eta.values, lw=0.6, color="#1f5f8b", label="hourly")
    ax1.set_ylabel("Water level [m]")
    ax1.set_title("Synthetic tide (M2 + S2 + noise)")
    ax1.legend(loc="upper right")
    ax1.grid(alpha=0.3)

    ax2.plot(daily.index, daily["range"], marker="o", ms=3, color="#c0392b")
    ax2.set_ylabel("Daily range [m]")
    ax2.grid(alpha=0.3)

    # M2 分潮時序圖
    ax3.plot(comp.index, comp["m2"], lw=0.6, color="#2e8b57")
    ax3.set_ylabel("M2 [m]")
    ax3.grid(alpha=0.3)

    # S2 分潮時序圖（只有最底下的子圖標示 x 軸）
    ax4.plot(comp.index, comp["s2"], lw=0.6, color="#8e44ad")
    ax4.set_ylabel("S2 [m]")
    ax4.set_xlabel("Date")
    ax4.set_ylim(-1.0, 1.0)
    ax4.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)  # 批次跑很多張圖時，記得關掉，否則記憶體會一直長


# ---------------------------------------------------------------------------
# 4. 主程式：只有直接執行這個檔案時才會跑
#    （被別的檔案 import 時不會跑，這樣函式可以重複使用）
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    eta = make_tide(START, DAYS, FREQ, SEED)
    daily = daily_stats(eta)

    print("前 5 筆資料：")
    print(eta.head(), "\n")
    print("每日統計（前 5 天）：")
    print(daily.head().round(3), "\n")

    print(f"最大潮差：{daily['range'].max():.2f} m（理論約 {2*(M2_AMP+S2_AMP):.2f} m）")
    print(f"最小潮差：{daily['range'].min():.2f} m（理論約 {2*(M2_AMP-S2_AMP):.2f} m）")
    print(f"理論大小潮週期：{theoretical_spring_neap_period():.2f} 天")

    daily.to_csv(OUT_DIR / "daily_stats.csv", float_format="%.4f")
    comp = make_constituents(START, DAYS, FREQ)
    plot_overview(eta, daily, comp, OUT_DIR / "tide_overview.png")
    print("\n已輸出 daily_stats.csv 與 tide_overview.png")
