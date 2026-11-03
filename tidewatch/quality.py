"""資料品質檢查：範圍、缺值、突波、漂移。"""
import numpy as np
import pandas as pd

from tidewatch.config import TRAIN_DAYS

RANGE_M = 5.0        # 合理水位範圍 ±5 m
SPIKE_Z = 4.0        # 突波門檻（標準差倍數）
DRIFT_Z = 1.96       # 漂移檢定門檻（95%）


def check(df: pd.DataFrame) -> pd.DataFrame:
    """每個測站一列的品質摘要。"""
    n_ref = TRAIN_DAYS * 24
    rows = []
    for sid in df.columns:
        s = df[sid]
        z = (s - s.mean()) / s.std()
        early, late = s.iloc[:n_ref], s.iloc[n_ref:]
        # 兩段平均值差異的 z 統計量
        se = np.sqrt(early.var() / len(early) + late.var() / len(late))
        drift_z = (late.mean() - early.mean()) / se
        rows.append({
            "station": sid,
            "missing_ratio": float(s.isna().mean()),
            "out_of_range": float((s.abs() > RANGE_M).mean()),
            "spikes": int((z.abs() > SPIKE_Z).sum()),
            "drift_z": float(drift_z),
            "drift_flag": bool(abs(drift_z) > DRIFT_Z),
        })
    return pd.DataFrame(rows).set_index("station")
