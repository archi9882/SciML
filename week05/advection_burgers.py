"""
第 5 週範例：對流的數值擴散、Burgers 方程的激波，以及「把求解器包成 solve(params) → 結果」。

名詞（第一次出現先定義）：
- 對流方程：u_t + a u_x = 0。波形以速度 a 平移，形狀不變（洪水波不考慮擴散時的行為）。
- Upwind（迎風）格式：空間差分用「水流來的那一側」。簡單、穩定，但會把波形抹平。
- CFL 數 C = a dt / dx：一個時間步長，波走了幾個網格。顯式 upwind 要求 C ≤ 1。
- 數值擴散：格式本身造成、方程式裡沒有的擴散。一階 upwind 等效於多了擴散係數 D_num = a dx (1 - C) / 2。
- Burgers 方程：u_t + u u_x = ν u_xx。對流項讓波形越來越陡，擴散項（黏滯係數 ν）限制它不要變成斷崖（激波）。

執行：python week05/advection_burgers.py
"""
import json

import numpy as np

A = 14.7        # 洪水波速 [km/hr]：運動波波速，推導見 docs/parameters.md
L = 20.0        # 河段長度 [km]
T_END = 0.5     # 模擬時間 [hr]（波走約 7.35 km）
X0, W = 4.0, 1.0    # 初始高斯波的中心 [km] 與寬度參數 [km]：exp(-((x - X0) / W)^2)


def upwind(nx: int, cfl: float) -> tuple[np.ndarray, np.ndarray]:
    """一階 upwind 解對流方程。上游端固定 0，下游端零梯度。回傳 (x, u)。"""
    x = np.linspace(0.0, L, nx)
    dx = x[1] - x[0]
    nsteps = int(np.ceil(T_END * A / (cfl * dx)))
    c = A * (T_END / nsteps) / dx                     # 調整 dt 使最後剛好是 T_END，實際的 CFL 數
    u = np.exp(-((x - X0) / W) ** 2)
    for _ in range(nsteps):
        u[1:] = u[1:] - c * (u[1:] - u[:-1])
        u[0] = 0.0
    return x, u


def variance(x: np.ndarray, u: np.ndarray) -> float:
    """把 u 當成分布，算它的變異數 [km^2]。"""
    m = u.sum()
    mean = (x * u).sum() / m
    return float(((x - mean) ** 2 * u).sum() / m)


def solve(params: dict) -> dict:
    """把求解器包成 solve(params) → 結果：設定與指標一起回傳，方便批次存檔。"""
    nx, cfl = params["nx"], params["cfl"]
    x, u = upwind(nx, cfl)
    dx = x[1] - x[0]
    v0 = W ** 2 / 2                                        # 初始高斯的變異數
    t = T_END
    d_num = A * dx * (1 - cfl) / 2                        # 一階 upwind 的數值擴散係數
    return {"params": params,
            "peak": round(float(u.max()), 4),
            "variance_km2": round(variance(x, u), 4),
            "variance_predicted_km2": round(v0 + 2 * d_num * t, 4),
            "d_num_km2_hr": round(d_num, 3)}


def burgers(nx: int, nu: float, t_end: float = 0.3) -> tuple[np.ndarray, np.ndarray]:
    """Burgers 方程，週期邊界，u0 = sin(2πx)，x ∈ [0, 1]。
    對流項用守恆型 Rusanov 通量（一階，自帶數值黏滯 alpha*dx/2），擴散項用中央差分。"""
    x = np.linspace(0.0, 1.0, nx, endpoint=False)
    dx = x[1] - x[0]
    u = np.sin(2 * np.pi * x)
    t = 0.0
    while t < t_end - 1e-12:
        alpha = np.abs(u).max()
        dt = min(0.4 * dx / alpha, 0.4 * dx ** 2 / (2 * nu), t_end - t)
        f = 0.5 * u ** 2
        up, fp = np.roll(u, -1), np.roll(f, -1)
        flux = 0.5 * (f + fp) - 0.5 * alpha * (up - u)            # 第 i 與 i+1 格之間的通量
        u = u - dt / dx * (flux - np.roll(flux, 1)) + nu * dt / dx ** 2 * (up - 2 * u + np.roll(u, 1))
        t += dt
    return x, u


def max_gradient(x: np.ndarray, u: np.ndarray) -> float:
    return float(np.abs(np.diff(np.append(u, u[0])) / (x[1] - x[0])).max())


def main() -> None:
    print("一、upwind 的數值擴散（dx = 0.5 km，物理擴散係數 D = 0.60 km²/hr）")
    print(f"{'CFL':>5} {'D_num':>8} {'峰值':>7} {'變異數':>8} {'預測':>8}")
    for cfl in (0.9, 0.5, 0.1):
        r = solve({"nx": 41, "cfl": cfl})
        print(f"{cfl:5.1f} {r['d_num_km2_hr']:8.3f} {r['peak']:7.3f} {r['variance_km2']:8.3f} {r['variance_predicted_km2']:8.3f}")
    print("  CFL 越小，數值擴散越大；CFL = 0.5 時它已是物理擴散的 3 倍，波形主要被格式抹平，不是被物理。")

    print("\n二、Burgers 方程：最大梯度 max|u_x|（t = 0.3，不含擴散的激波在 t = 0.159 形成）")
    print(f"{'nx':>5} {'ν=0.05':>9} {'ν=0.01':>9} {'ν=0.002':>9}")
    for nx in (100, 200, 400, 800):
        print(f"{nx:5d} " + " ".join(f"{max_gradient(*burgers(nx, nu)):9.1f}" for nu in (0.05, 0.01, 0.002)))
    print("  ν 小的時候，網格不夠細就看不到真正的激波厚度，梯度隨網格加密一直變：還沒收斂。")

    print("\n三、solve(params) 的輸出（一行 JSON，可直接存成 metrics）")
    print(json.dumps(solve({"nx": 81, "cfl": 0.5}), ensure_ascii=False))


if __name__ == "__main__":
    main()
