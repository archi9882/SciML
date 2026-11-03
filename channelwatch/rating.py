"""水位流量曲線：由實測的 (水位, 流量) 擬合 Q = a * h^b，再外插到洪水流量。"""
import numpy as np
import pandas as pd

from channelwatch.config import SAMPLE_DIR


def load_gaugings() -> pd.DataFrame:
    """實測流量資料：stage_cm（水位，cm）、discharge_m3s（流量）。"""
    df = pd.read_csv(SAMPLE_DIR / "gaugings.csv")
    df["stage_m"] = df["stage_cm"]
    return df


def fit(df: pd.DataFrame) -> dict:
    """在對數空間做線性迴歸，得 Q = a * h^b。"""
    x = np.log(df["stage_m"].to_numpy())
    y = np.log(df["discharge_m3s"].to_numpy())
    b, ln_a = np.polyfit(x, y, 1)
    pred = np.exp(ln_a) * df["stage_m"].to_numpy() ** b
    resid = df["discharge_m3s"].to_numpy() - pred
    return {"a": float(np.exp(ln_a)), "b": float(b),
            "rmse_m3s": float(np.sqrt(np.mean(resid ** 2))),
            "max_gauged_m3s": float(df["discharge_m3s"].max())}


def discharge(params: dict, stage_m: float) -> float:
    return params["a"] * stage_m ** params["b"]
