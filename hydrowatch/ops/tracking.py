"""實驗追蹤：每次執行把參數與指標追加到 outputs/runs.jsonl。"""
import json
from datetime import datetime, timezone

from hydrowatch.config import OUT_DIR

MODEL_VERSION = "v1"


def log_run(params: dict, metrics: dict) -> dict:
    """追加一筆紀錄並回傳該筆內容。"""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rec = {
        "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "model_version": MODEL_VERSION,
        "params": params,
        "metrics": metrics,
    }
    with open(OUT_DIR / "runs.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec
