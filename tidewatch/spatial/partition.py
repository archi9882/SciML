"""測站分割：把範圍內每個位置分給最近的測站（徐昇多邊形的格點版），算各站的面積權重。"""
import numpy as np
import pandas as pd


def partition_weights(stations: pd.DataFrame, lon_range=(120.0, 120.8), lat_range=(22.5, 24.4),
                      n: int = 300) -> np.ndarray:
    """回傳每個測站負責的面積比例（總和為 1），順序同 stations。"""
    lons = np.linspace(*lon_range, n)
    lats = np.linspace(*lat_range, n)
    LON, LAT = np.meshgrid(lons, lats)

    # 每個格點到每個測站的距離平方，取最近者
    d2 = ((LON[..., None] - stations["lon"].to_numpy()) ** 2
          + (LAT[..., None] - stations["lat"].to_numpy()) ** 2)
    owner = d2.argmin(axis=-1)

    cell_area = (lons[1] - lons[0]) * (lats[1] - lats[0])     # 每格面積
    area = np.bincount(owner.ravel(), minlength=len(stations)) * cell_area
    return area / area.sum()


def basin_mean(levels: pd.Series, weights: np.ndarray) -> float:
    """面積加權平均水位。levels 的順序需與 weights 相同。"""
    return float((levels.to_numpy() * weights).sum())
