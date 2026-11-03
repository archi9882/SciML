"""全系統共用的路徑與常數。"""
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parent
ROOT = PKG_DIR.parent
SAMPLE_DIR = PKG_DIR / "sample_data"   # 範例原始資料
OUT_DIR = ROOT / "outputs"             # 執行輸出（不進版控）

M2_PERIOD_H = 12.42    # 主太陰半日潮週期 [hr]
S2_PERIOD_H = 12.00    # 主太陽半日潮週期 [hr]
TRAIN_DAYS = 20        # 前 N 天視為「參考期」
