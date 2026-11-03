"""資料品質檢查：範圍、缺值、突波、漂移。"""
import numpy as np
import pandas as pd

from hydrowatch.config import REF_DAYS

RANGE = {"rain": (0.0, 150.0), "flow": (0.0, 1000.0)}   # 雨量 mm/hr、流量 m3/s 的合理範圍
SPIKE_Z = 4.0                                            # 突波門檻（標準差倍數）
DRIFT_Z = 1.96                                           # 漂移檢定門檻（95%）


def check(df: pd.DataFrame) -> pd.DataFrame:
    """每個測站一列的品質摘要。"""
    n_ref = REF_DAYS * 24
    rows = []
    for sid in df.columns:
        s = df[sid]
        lo, hi = RANGE["flow" if sid == "Q" else "rain"]
        z = (s - s.mean()) / s.std()
        early, late = s.iloc[:n_ref], s.iloc[n_ref:]
        se = np.sqrt(early.var() / len(early) + late.var() / len(late))
        drift_z = (late.mean() - early.mean()) / se
        rows.append({
            "station": sid,
            "missing_ratio": float(s.isna().mean()),
            "out_of_range": float(((s < lo) | (s > hi)).mean()),
            "spikes": int((z.abs() > SPIKE_Z).sum()),
            "drift_z": float(drift_z),
            "drift_flag": bool(abs(drift_z) > DRIFT_Z),
        })
    return pd.DataFrame(rows).set_index("station")
