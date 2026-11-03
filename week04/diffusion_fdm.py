"""
第 4 週範例：一維擴散方程的有限差分解，以及穩定性與收斂。

名詞（第一次出現先定義）：
- 擴散方程：u_t = D u_xx。u 隨時間變化的快慢，取決於它在空間上彎曲的程度（u_xx）；D 是擴散係數。
  洪水波在河道中變得平坦，就是這種現象（水力擴散係數 D = Q/(2 B S0)，見 docs/parameters.md）。
- 有限差分：把連續的 x 與 t 切成網格，用相鄰格點的差來近似導數。
- FTCS（顯式）：用「現在」的值算「下一步」，簡單，但步長受限。
- Backward Euler（隱式）：「下一步」的值互相牽連，要解一組聯立方程，但沒有步長限制。
- 擴散數 r = D dt / dx²：顯式格式要求 r ≤ 0.5。

問題：u(x,0) = sin(πx/L)，兩端固定為 0。精確解 u(x,t) = exp(-D π² t / L²) sin(πx/L)，可以用來檢查程式。

執行：python week04/diffusion_fdm.py
"""
import numpy as np

D = 0.60        # 擴散係數 [km^2/hr]：河道水力擴散係數的推導值
L = 10.0        # 河段長度 [km]
T_END = 6.0     # 模擬時間 [hr]


def exact(x: np.ndarray, t: float) -> np.ndarray:
    return np.exp(-D * np.pi ** 2 * t / L ** 2) * np.sin(np.pi * x / L)


def ftcs(n: int, dt: float, perturb: float = 0.0, seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """顯式 FTCS。n 為格點數（含兩端），回傳 (x, 最後的 u)。perturb 為初始的微小隨機擾動。"""
    x = np.linspace(0.0, L, n)
    dx = x[1] - x[0]
    u = np.sin(np.pi * x / L)
    if perturb:
        u[1:-1] += perturb * np.random.default_rng(seed).normal(size=n - 2)
    nsteps = int(np.ceil(T_END / dt - 1e-9))     # 步數取整，再調整 dt，讓最後剛好是 T_END
    r = D * (T_END / nsteps) / dx ** 2
    for _ in range(nsteps):
        u[1:-1] = u[1:-1] + r * (u[2:] - 2 * u[1:-1] + u[:-2])
    return x, u


def backward_euler(n: int, dt: float) -> tuple[np.ndarray, np.ndarray]:
    """隱式 Backward Euler：每一步解 (I - r*A) u_new = u_old。"""
    x = np.linspace(0.0, L, n)
    dx = x[1] - x[0]
    u = np.sin(np.pi * x / L)
    nsteps = int(np.ceil(T_END / dt - 1e-9))
    r = D * (T_END / nsteps) / dx ** 2
    m = n - 2
    A = np.diag(np.full(m, 1 + 2 * r)) + np.diag(np.full(m - 1, -r), 1) + np.diag(np.full(m - 1, -r), -1)
    for _ in range(nsteps):
        u[1:-1] = np.linalg.solve(A, u[1:-1])
    return x, u


def l2_error(x: np.ndarray, u: np.ndarray) -> float:
    return float(np.sqrt(np.mean((u - exact(x, T_END)) ** 2)))


def main() -> None:
    print("一、穩定性：固定 dx = 0.5 km（r ≤ 0.5 ⇔ dt ≤ 0.208 hr），在初始條件加 1e-6 的微小擾動")
    print(f"{'dt [hr]':>8} {'r':>6} {'L2 誤差':>12} {'max|u|':>12}")
    for dt in (0.10, 0.20, 0.25, 0.30, 0.40, 0.50):
        x, u = ftcs(21, dt, perturb=1e-6)
        print(f"{dt:8.2f} {D * dt / 0.5 ** 2:6.3f} {l2_error(x, u):12.3e} {np.abs(u).max():12.3e}")

    print("\n二、收斂：dt 隨 dx² 縮小（r = 0.25 固定），誤差應以 dx² 的比例下降（二階）")
    print(f"{'格點數':>6} {'dx [km]':>8} {'L2 誤差':>12} {'誤差比':>8}")
    prev = None
    for n in (11, 21, 41, 81):
        dx = L / (n - 1)
        x, u = ftcs(n, 0.25 * dx ** 2 / D)
        e = l2_error(x, u)
        print(f"{n:6d} {dx:8.3f} {e:12.3e} {'' if prev is None else f'{prev / e:8.2f}'}")
        prev = e

    print("\n三、隱式與顯式：dx = 0.5 km，dt = 1.0 hr（r = 2.4，顯式早已不穩定）")
    x, u = backward_euler(21, 1.0)
    print(f"  Backward Euler：L2 誤差 {l2_error(x, u):.3e}，max|u| {np.abs(u).max():.3f}")
    for dt in (0.1, 0.01):
        x, u = backward_euler(21, dt)
        print(f"  Backward Euler dt = {dt}：L2 誤差 {l2_error(x, u):.3e}")
    print("  dt 縮小後，誤差降到空間離散誤差（dx = 0.5 km，約 4e-4）就不再下降：時間與空間誤差要一起看")


if __name__ == "__main__":
    main()
