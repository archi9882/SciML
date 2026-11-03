"""資料擷取：把各測站的原始檔統一成「UTC、公尺、每小時」的潮位表。"""
import pandas as pd

from tidewatch.config import SAMPLE_DIR

# 每個測站的檔案格式（欄位名稱、單位、時區、缺值標記）
SPECS = {
    "A": {"file": "station_A.csv", "time_col": "time_utc", "value_col": "level_m",
          "unit": "m", "tz": "UTC", "missing": None},
    "B": {"file": "station_B.csv", "time_col": "time_local", "value_col": "level_cm",
          "unit": "cm", "tz": "UTC", "missing": None},
    "C": {"file": "station_C.csv", "time_col": "timestamp", "value_col": "level_m",
          "unit": "m", "tz": "UTC", "missing": -999},
    "D": {"file": "station_D.csv", "time_col": "time_utc", "value_col": "level_m",
          "unit": "m", "tz": "UTC", "missing": None},
}

UNIT_TO_M = {"m": 1.0, "cm": 0.01, "mm": 0.001}


def stations() -> pd.DataFrame:
    """測站清單：id、name、lat、lon。"""
    return pd.read_csv(SAMPLE_DIR / "stations.csv")


def load_station(sid: str) -> pd.Series:
    """讀一個測站，回傳以 UTC 時間為索引、單位公尺、每小時一筆的序列。"""
    spec = SPECS[sid]
    df = pd.read_csv(SAMPLE_DIR / spec["file"])

    t = pd.to_datetime(df[spec["time_col"]])
    if t.dt.tz is None:
        t = t.dt.tz_localize(spec["tz"])
    else:
        t = t.dt.tz_convert("UTC")

    v = df[spec["value_col"]].astype(float)
    if spec["missing"] is not None:
        v = v.mask(v == spec["missing"])
    v = v * UNIT_TO_M[spec["unit"]]

    s = pd.Series(v.values, index=pd.DatetimeIndex(t), name=sid)
    s = s.resample("h").mean()              # 統一成每小時
    return s.interpolate(method="time")     # 補缺值


def load_all() -> pd.DataFrame:
    """所有測站合併成一張表，欄位是測站 id。"""
    cols = [load_station(sid) for sid in SPECS]
    return pd.concat(cols, axis=1).dropna()
