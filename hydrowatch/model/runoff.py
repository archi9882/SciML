"""降雨逕流模型：單一線性水庫，並用觀測流量率定。

    dS/dt = C * A * P(t) - S / k          Q(t) = S / k + Q_base   （S 的單位 m^3，k 換成秒）
    P：流域平均雨量 [mm/hr]；C：逕流係數；A：流域面積；k：退水常數 [hr]；S：流域蓄水量。
時間用顯式前進歐拉，步長 1 小時。
"""
import numpy as np
import pandas as pd

from hydrowatch.config import AREA_KM2

Q_BASE = 2.0   # 基流 [m3/s]


def simulate(rain_mm_h: np.ndarray, k_h: float, c: float, dt_h: float = 1.0) -> np.ndarray:
    """由雨量序列算流量序列 [m3/s]。"""
    inflow = c * rain_mm_h * AREA_KM2 * 1e6 / 1000 / 3600     # mm/hr → m3/s
    s = 0.0
    q = np.zeros(len(rain_mm_h))
    for i, inf in enumerate(inflow):
        q[i] = s / (k_h * 3600) + Q_BASE
        s += dt_h * 3600 * (inf - s / (k_h * 3600))
        s = max(s, 0.0)
    return q


def fit(rain: pd.Series, q: pd.Series) -> dict:
    """格點搜尋 k 與 C，使模擬流量與觀測流量的 RMSE 最小。"""
    best = None
    for k in np.arange(4.0, 61.0, 2.0):
        for c in np.arange(0.1, 0.91, 0.05):
            rmse = float(np.sqrt(np.mean((simulate(rain.values, k, c) - q.values) ** 2)))
            if best is None or rmse < best["rmse"]:
                best = {"k_h": float(k), "c": float(c), "rmse": rmse}
    return best


def nse(sim: np.ndarray, obs: np.ndarray) -> float:
    """Nash–Sutcliffe 效率係數：1 為完美，0 表示不比觀測平均值好。"""
    return float(1 - np.sum((obs - sim) ** 2) / np.sum((obs - obs.mean()) ** 2))


def evaluate(rain: pd.Series, q: pd.Series) -> tuple[dict, dict]:
    """率定並評估，回傳 (參數, 指標)。"""
    params = fit(rain, q)
    sim = simulate(rain.values, params["k_h"], params["c"])
    rmse = float(np.sqrt(np.mean((sim - q.values) ** 2)))
    return params, {"nse": nse(sim, q.values), "rmse_m3s": rmse, "total_error_m3s": rmse}
