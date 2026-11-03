"""河道洪水演算：1D 對流擴散（擴散波）方程的有限差分解。

    dc/dt + u dc/dx = D d2c/dx2        （c：流量擾動（洪水波），x：沿河道距離 [km]，t：時間 [hr]）

對流項用一階 upwind（水流向 +x），擴散項用中央差分，時間用顯式前進歐拉。
"""
import numpy as np

L_KM = 20.0     # 河道長度 [km]
N = 40          # 網格數
DX = L_KM / N   # 網格間距 [km]
D = 0.60        # 擴散係數 [km^2/hr]，Hayami：Q/(2 B S0)，見 docs/parameters.md
U = 14.7        # 洪水波速 [km/hr]，運動波波速 (5/3) 倍流速
DT = 0.03       # 時間步長 [hr]
NSTEPS = 15     # 步數（共 0.45 hr）


def initial() -> tuple[np.ndarray, np.ndarray]:
    """初始洪水波：靠近下游出口的高斯形洪峰。"""
    x = (np.arange(N) + 0.5) * DX
    return x, np.exp(-((x - 14.0) / 1.0) ** 2)


def solve(c0: np.ndarray, u: float, d: float, dx: float, dt: float, nsteps: int) -> np.ndarray:
    """往前積分 nsteps 步，回傳最後的濃度分布。"""
    c = c0.copy()
    for _ in range(nsteps):
        adv = -u * (c - np.roll(c, 1)) / dx
        dif = d * (np.roll(c, -1) - 2 * c + np.roll(c, 1)) / dx ** 2
        c = c + dt * (adv + dif)
    return c


def run_default() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """用預設參數跑一次，回傳 (x, 初始分布, 最終分布)。"""
    x, c0 = initial()
    return x, c0, solve(c0, U, D, DX, DT, NSTEPS)
