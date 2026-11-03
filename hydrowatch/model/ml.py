"""殘差修正：用一個小型神經網路預測「降雨逕流模型沒抓到的部分」。

輸入：前兩個小時的殘差；輸出：下一小時的殘差。純 numpy 實作（2-16-1，tanh）。
"""
import numpy as np


def make_xy(resid: np.ndarray, lags: int = 2) -> tuple[np.ndarray, np.ndarray]:
    """把殘差序列整理成 (X, y)：X 的欄位是 r[t-1]、r[t-2]，y 是 r[t]。"""
    X = np.column_stack([resid[lags - k - 1:len(resid) - k - 1] for k in range(lags)])
    return X, resid[lags:]


def _forward(m: dict, X: np.ndarray) -> np.ndarray:
    h = np.tanh(X @ m["W1"] + m["b1"])
    return (h @ m["W2"] + m["b2"]).ravel()


def train(resid: np.ndarray, epochs: int = 300, lr: float = 0.05,
          hidden: int = 16, seed: int = 0) -> tuple[dict, dict]:
    """訓練並回傳 (模型, 指標)。"""
    X, y = make_xy(resid)
    mu, sd = X.mean(axis=0), X.std(axis=0)
    Xn = (X - mu) / sd

    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(Xn))
    cut = int(0.8 * len(Xn))
    tr, te = idx[:cut], idx[cut:]

    m = {"W1": rng.normal(0, 0.5, (X.shape[1], hidden)), "b1": np.zeros(hidden),
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
    return m, {"mae_m": mae}
