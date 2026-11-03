"""全系統共用的路徑與常數。"""
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parent
ROOT = PKG_DIR.parent
SAMPLE_DIR = PKG_DIR / "sample_data"   # 範例原始資料
OUT_DIR = ROOT / "outputs"             # 執行輸出（不進版控）

AREA_KM2 = 120.0       # 流域面積 [km^2]
RHO = 1000.0           # 水的密度 [kg/m^3]
G = 9.81               # 重力加速度 [m/s^2]
REF_DAYS = 20          # 前 N 天視為「參考期」
