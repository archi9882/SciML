"""漂移監控：最近一段資料的平均水位，跟參考期相比有沒有明顯偏移。"""
import pandas as pd

K_SIGMA = 3.0   # 偏移超過參考期標準差的幾倍就警示


def check_drift(reference: pd.Series, recent: pd.Series) -> dict:
    shift = float(recent.mean() - reference.mean())
    limit = K_SIGMA * float(reference.std())
    return {"shift_m": shift, "limit_m": limit, "alert": abs(shift) > limit}
