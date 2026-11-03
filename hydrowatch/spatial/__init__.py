"""空間：經緯度轉成平面座標，以及測站之間的內插。"""
import numpy as np
import pandas as pd

R_KM = 6371.0                    # 地球半徑 [km]
LON0, LAT0 = 121.0, 24.1         # 投影原點（流域中心）


def to_xy(lon: float, lat: float) -> tuple[float, float]:
    """經緯度 [度] 轉成以 (LON0, LAT0) 為原點的平面座標 [km]（等距圓柱投影）。"""
    x = R_KM * np.cos(np.radians(LAT0)) * np.radians(lon - LON0)
    y = R_KM * np.radians(lat - LAT0)
    return float(x), float(y)


def station_xy(stations: pd.DataFrame) -> np.ndarray:
    """測站的平面座標，形狀 (n, 2)。"""
    return np.array([to_xy(r.lat, r.lon) for r in stations.itertuples()])


def idw(xy: np.ndarray, values: np.ndarray, target: np.ndarray, power: float = 2.0) -> float:
    """反距離加權內插：離得越近的測站權重越大。"""
    d = np.hypot(xy[:, 0] - target[0], xy[:, 1] - target[1])
    w = 1.0 / d ** power
    return float((w * values).sum() / w.sum())
