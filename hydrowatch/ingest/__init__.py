"""資料擷取：把各測站的原始檔統一成「UTC、每小時、雨量 mm/hr、流量 m3/s」的表。"""
import pandas as pd

from hydrowatch.config import SAMPLE_DIR

# 每個測站的檔案格式（欄位名稱、單位、時區、缺值標記、聚合方式）
SPECS = {
    "R1": {"file": "rain_R1.csv", "time_col": "time_utc", "value_col": "rain_mm",
           "unit": "mm", "tz": "UTC", "missing": None, "agg": "sum"},
    "R2": {"file": "rain_R2.csv", "time_col": "time_local", "value_col": "rain_mm_10min",
           "unit": "mm", "tz": "UTC", "missing": None, "agg": "mean"},
    "R3": {"file": "rain_R3.csv", "time_col": "time_utc", "value_col": "rain_in",
           "unit": "in", "tz": "UTC", "missing": None, "agg": "sum"},
    "R4": {"file": "rain_R4.csv", "time_col": "timestamp", "value_col": "rain_mm",
           "unit": "mm", "tz": "UTC", "missing": -999, "agg": "sum"},
    "Q": {"file": "flow_Q.csv", "time_col": "time_utc", "value_col": "q_m3s",
          "unit": "m3/s", "tz": "UTC", "missing": -999, "agg": "mean"},
}

UNIT_SCALE = {"mm": 1.0, "in": 2.54, "m3/s": 1.0}


def stations() -> pd.DataFrame:
    """測站清單：id、name、lat、lon。"""
    return pd.read_csv(SAMPLE_DIR / "stations.csv")


def load_station(sid: str) -> pd.Series:
    """讀一個測站，回傳以 UTC 時間為索引、每小時一筆的序列。"""
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
    v = v * UNIT_SCALE[spec["unit"]]

    s = pd.Series(v.values, index=pd.DatetimeIndex(t), name=sid)
    s = getattr(s.resample("h"), spec["agg"])()      # 統一成每小時
    if sid == "Q":
        return s.interpolate(method="time")          # 流量缺值用內插補
    return s.fillna(0.0)                             # 雨量缺值當作沒下雨


def load_all() -> pd.DataFrame:
    """所有測站合併成一張表，欄位是測站 id。"""
    cols = [load_station(sid) for sid in SPECS]
    return pd.concat(cols, axis=1).dropna()
