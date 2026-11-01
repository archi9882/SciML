"""Day 2 Q3：掃描多個 SEED，看哪些輸出會變、哪些不變。

用法：.venv\\Scripts\\python.exe week01/seed_check.py
"""
import numpy as np

from tide_example import (
    DAYS, FREQ, MEAN_SEA_LEVEL, START,
    daily_stats, make_constituents, make_tide,
)


def outputs_for_seed(seed: int) -> dict[str, np.ndarray]:
    """用同一個 seed 跑一次程式，回傳各項輸出（統一成 numpy 陣列）。"""
    comp = make_constituents(START, DAYS, FREQ)
    eta = make_tide(START, DAYS, FREQ, seed)
    daily = daily_stats(eta)
    # 反推雜訊成分：eta 扣掉平均海水面與兩個分潮，剩下的就是雜訊
    noise = eta - MEAN_SEA_LEVEL - comp["m2"] - comp["s2"]
    return {
        "分潮 comp": comp.values,
        "雜訊 noise": noise.values,
        "水位 eta": eta.values,
        "每日 max": daily["max"].values,
        "每日 min": daily["min"].values,
        "每日 mean": daily["mean"].values,
        "每日 range": daily["range"].values,
    }


def seed_sweep(n_seeds: int = 20) -> None:
    """掃描多個 seed，印出各輸出的跨 seed 標準差：0 代表不受 seed 影響。"""
    runs = [outputs_for_seed(s) for s in range(n_seeds)]
    print(f"掃描 {n_seeds} 個 seed，各輸出的跨 seed 標準差（單位 m）")
    for name in runs[0]:
        stack = np.stack([r[name] for r in runs])  # 形狀：(seed, ...)
        std = stack.std(axis=0).mean()             # 對 seed 取 std，再對時間平均
        flag = "不變" if np.isclose(std, 0) else "改變"
        print(f"{name:12s} {flag}  std = {std:.4g}")


if __name__ == "__main__":
    seed_sweep()
