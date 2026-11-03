"""代理模型：用小型神經網路取代洪水演算求解器。

輸入 (波速 u、擴散係數 D)，輸出 0.45 小時後的洪峰值。訓練資料由 routing.solve 產生。
"""
import time

import numpy as np

from hydrowatch.model import routing

U_RANGE = (7.0, 17.0)   # 波速範圍 [km/hr]
D_RANGE = (0.3, 0.9)    # 擴散係數範圍 [km^2/hr]


def make_dataset(n: int = 200, seed: int = 1) -> tuple[np.ndarray, np.ndarray]:
    """在參數範圍內隨機取 n 組，各跑一次求解器，回傳 (參數, 洪峰值)。"""
    rng = np.random.default_rng(seed)
    X = np.column_stack([rng.uniform(*U_RANGE, n), rng.uniform(*D_RANGE, n)])
    _, c0 = routing.initial()
    y = np.array([routing.solve(c0, u, d, routing.DX, routing.DT, routing.NSTEPS).max()
                  for u, d in X])
    return X, y


def _forward(m: dict, Xn: np.ndarray) -> np.ndarray:
    h = np.tanh(Xn @ m["W1"] + m["b1"])
    return (h @ m["W2"] + m["b2"]).ravel()


def train(n: int = 200, hidden: int = 16, epochs: int = 2000, lr: float = 0.1,
          seed: int = 0) -> tuple[dict, dict]:
    """訓練並評估，回傳 (模型, 指標)。"""
    X, y = make_dataset(n)
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(X))
    cut = int(0.8 * len(X))
    tr, te = idx[:cut], idx[cut:]

    mu, sd = X[tr].mean(axis=0), X[tr].std(axis=0)
    Xn = (X - mu) / sd
    m = {"W1": rng.normal(0, 0.5, (2, hidden)), "b1": np.zeros(hidden),
         "W2": rng.normal(0, 0.5, (hidden, 1)), "b2": np.zeros(1), "mu": mu, "sd": sd}
    for _ in range(epochs):
        h = np.tanh(Xn[tr] @ m["W1"] + m["b1"])
        err = (h @ m["W2"] + m["b2"]).ravel() - y[tr]
        g = (2 * err / len(tr))[:, None]
        gh = (g @ m["W2"].T) * (1 - h ** 2)
        m["W2"] -= lr * (h.T @ g)
        m["b2"] -= lr * g.sum(axis=0)
        m["W1"] -= lr * (Xn[tr].T @ gh)
        m["b1"] -= lr * gh.sum(axis=0)

    mae = float(np.mean(np.abs(_forward(m, Xn[te]) - y[te])))

    # 速度比較：求解器每次呼叫 vs 代理模型每次推論
    _, c0 = routing.initial()
    t0 = time.perf_counter()
    for u, d in X[te]:
        routing.solve(c0, u, d, routing.DX, routing.DT, routing.NSTEPS)
    t_solver = (time.perf_counter() - t0) / len(te)
    t0 = time.perf_counter()
    for row in Xn[te]:
        _forward(m, row[None, :])
    t_pred = (time.perf_counter() - t0) / len(te)

    return m, {"mae": mae, "speedup": float(t_solver / t_pred)}
