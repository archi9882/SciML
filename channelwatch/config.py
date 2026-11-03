"""河道斷面與常數；各參數的來源與推導見 docs/parameters.md。"""
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parent
ROOT = PKG_DIR.parent
SAMPLE_DIR = PKG_DIR / "sample_data"
OUT_DIR = ROOT / "outputs" / "channel"

G = 9.81            # 重力加速度 [m/s^2]
BED_WIDTH = 30.0    # 河床寬 [m]
SIDE_SLOPE = 0.0    # 邊坡 z（水平 : 垂直），0 為矩形斷面
BED_SLOPE = 0.01    # 河床坡降 [m/m]
MANNING_N = 0.030   # Manning 粗糙係數
