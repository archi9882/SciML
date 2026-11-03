"""
第 2 週範例 2／2：批次跑多組參數，再彙整成一張表與一張圖
==========================================================

流程（每一步都可以單獨重跑）：
  1. 定義參數網格：哪些參數要變、各取哪些值
  2. 對每一組參數，「送出一個工作」：用 subprocess 呼叫 runoff_cli.py
  3. 已經跑過、設定相同的就跳過（冪等性：重跑整個批次不會重複做事）
  4. 讀回每個資料夾的 config.json + metrics.json，彙整成 summary.csv
  5. 畫「參數 vs 結果」，並疊上理論線檢查

為什麼用 subprocess 而不是直接 import 函式：
  這模擬了真實的批次系統（排程器、容器、叢集）——它們只會「用參數執行一支程式，
  看結束碼與輸出檔」。學會這個介面，之後換成 Docker 或排程工具時概念不變。

執行：
  python batch.py            # 跑網格並彙整
  python batch.py --force    # 忽略已完成的結果，全部重跑
"""

import argparse
import itertools
import json
import subprocess
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).parent
RUNS = HERE / "runs"

# 1. 參數網格：改這裡就能改整個實驗
GRID = {
    "k_hours": [0.4, 0.8, 1.2, 2.4, 4.8],
    "seed": [1, 2],
}


def run_name(params: dict) -> str:
    return "_".join(f"{k}{v}" for k, v in params.items())


def already_done(folder: Path, params: dict) -> bool:
    """結果存在、且當時的設定跟這次相同，才算做過。"""
    cfg, met = folder / "config.json", folder / "metrics.json"
    if not (cfg.exists() and met.exists()):
        return False
    old = json.loads(cfg.read_text(encoding="utf-8"))
    return all(old.get(k) == v for k, v in params.items())


def submit(params: dict, folder: Path) -> int:
    cmd = [sys.executable, str(HERE / "runoff_cli.py"), "--out", str(folder)]
    for k, v in params.items():
        cmd += [f"--{k.replace('_', '-')}", str(v)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  失敗（exit {result.returncode}）：{result.stderr.strip()}")
    return result.returncode


def collect() -> pd.DataFrame:
    rows = []
    for folder in sorted(RUNS.iterdir()):
        cfg, met = folder / "config.json", folder / "metrics.json"
        if cfg.exists() and met.exists():
            row = json.loads(cfg.read_text(encoding="utf-8"))
            row.update(json.loads(met.read_text(encoding="utf-8")))
            row["run"] = folder.name
            rows.append(row)
    return pd.DataFrame(rows)


def plot(summary: pd.DataFrame, path: Path) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2))
    g = summary.groupby("k_hours")
    x = sorted(summary["k_hours"].unique())
    ax1.plot(x, g["peak_true_m3s"].mean(), "o-", color="#1f5f8b", label="peak flow, model (mean of seeds)")
    ax1.set_xlabel("Recession constant k [hr]")
    ax1.set_ylabel("Peak discharge [m3/s]")
    ax1.set_title("Longer k: flatter, lower peaks")
    ax1.grid(alpha=0.3)
    ax1.legend(fontsize=8)
    ax2.plot(x, g["recession_ratio"].mean(), "o-", color="#c0392b", label="pulse test: remaining after k hr")
    ax2.plot(x, g["theory_recession_ratio"].first(), "--", color="#c0392b", alpha=0.6, label="theory e^-1")
    ax2.set_xlabel("Recession constant k [hr]")
    ax2.set_ylabel("Fraction remaining")
    ax2.set_title("Explicit Euler vs theory")
    ax2.grid(alpha=0.3)
    ax2.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="忽略已完成的結果，全部重跑")
    args = ap.parse_args()

    RUNS.mkdir(exist_ok=True)
    keys = list(GRID)
    combos = [dict(zip(keys, vals)) for vals in itertools.product(*GRID.values())]
    print(f"共 {len(combos)} 組參數")

    n_fail = 0
    for params in combos:
        folder = RUNS / run_name(params)
        if not args.force and already_done(folder, params):
            print(f"跳過（已完成）：{folder.name}")
            continue
        print(f"執行：{folder.name}")
        if submit(params, folder) != 0:
            n_fail += 1

    summary = collect()
    summary.to_csv(HERE / "summary.csv", index=False)
    plot(summary, HERE / "summary.png")
    print(f"\n彙整 {len(summary)} 筆 → summary.csv、summary.png；失敗 {n_fail} 筆")
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
