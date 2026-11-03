"""水庫水量平衡與水力發電。

    dS/dt = Q_in - Q_out            S：蓄水量 [m^3]
    P = rho * g * Q_out * H * eta   H：水頭 [m]，eta：機組效率
"""
import numpy as np

from hydrowatch.config import G, RHO

CAPACITY_M3 = 1.26e8    # 庫容 [m^3]，鯉魚潭水庫總容量 12,600 萬 m3
H_MIN, H_MAX = 50.0, 90.0   # 空庫與滿庫時的水頭 [m]（壩高 96 m，上限為假設）
ETA = 0.90              # 機組效率（Pelton 0.85 至 0.90，Francis 高於 0.90）
Q_TURBINE = 2.9         # 預設發電放流量 [m3/s]，約為年平均入流量


def head(storage_m3: float) -> float:
    """水頭 [m]：隨蓄水量線性增加。"""
    return H_MIN + (H_MAX - H_MIN) * storage_m3 / CAPACITY_M3


def simulate(q_in: np.ndarray, s0: float = 1.25e8, q_out: float = Q_TURBINE) -> dict:
    """逐小時水量平衡，回傳蓄水量、發電功率與總發電量。"""
    s = s0
    storage = np.zeros(len(q_in))
    power = np.zeros(len(q_in))
    for i, qi in enumerate(q_in):
        s += (qi - q_out) * 3600
        s = max(s, 0.0)
        storage[i] = s
        power[i] = RHO * G * q_out * head(s) * ETA / 1e3      # 功率（MW）
    return {"storage_m3": storage, "power_mw": power, "energy_mwh": float(power.sum())}
