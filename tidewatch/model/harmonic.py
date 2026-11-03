"""調和分析：擬合 M2、S2 的振幅與相位，並評估擬合品質。

模型：eta(t) = MSL + sum_k A_k cos(w_k t - phi_k)，t 為距起點的小時數。
"""
import numpy as np
import pandas as pd

from tidewatch.config import M2_PERIOD_H, S2_PERIOD_H

OMEGA = {"m2": 2 * np.pi / M2_PERIOD_H, "s2": 2 * np.pi / S2_PERIOD_H}   # rad/hr


def _hours(index: pd.DatetimeIndex, t0: pd.Timestamp) -> np.ndarray:
    return np.asarray((index - t0) / pd.Timedelta(hours=1), dtype=float)


def _design(t: np.ndarray) -> np.ndarray:
    """設計矩陣：[1, cos(w_m2 t), sin(w_m2 t), cos(w_s2 t), sin(w_s2 t)]。"""
    return np.column_stack([
        np.ones_like(t),
        np.cos(OMEGA["m2"] * t), np.sin(OMEGA["m2"] * t),
        np.cos(OMEGA["s2"] * t), np.sin(OMEGA["s2"] * t),
    ])


def fit(series: pd.Series) -> dict:
    """最小平方擬合，回傳平均水位、兩個分潮的振幅 [m] 與相位 [rad]。"""
    t0 = series.index[0]
    t = _hours(series.index, t0)
    coef, *_ = np.linalg.lstsq(_design(t), series.values, rcond=None)
    msl, a1, b1, a2, b2 = coef
    return {
        "t0": t0.isoformat(),
        "msl": float(msl),
        "m2_amp": float(np.hypot(a1, b1)), "m2_phase": float(np.arctan2(b1, a1)),
        "s2_amp": float(np.hypot(a2, b2)), "s2_phase": float(np.arctan2(b2, a2)),
    }


def predict(params: dict, index: pd.DatetimeIndex) -> np.ndarray:
    """用擬合參數預測任意時間的水位 [m]。"""
    t = _hours(index, pd.Timestamp(params["t0"]))
    return (params["msl"]
            + params["m2_amp"] * np.cos(OMEGA["m2"] * t - params["m2_phase"])
            + params["s2_amp"] * np.cos(OMEGA["s2"] * t - params["s2_phase"]))


def evaluate(series: pd.Series) -> tuple[dict, dict]:
    """擬合並評估，回傳 (參數, 指標)。"""
    params = fit(series)
    resid = series.values - predict(params, series.index)
    rmse = float(np.sqrt(np.mean(resid ** 2)))
    skill = float(1 - resid.var() / series.values.var())
    return params, {"rmse_m": rmse, "skill": skill, "total_error_m": rmse}
