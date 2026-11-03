"""REST API：查詢任意位置、任意時間的預測潮位。

    GET /health
    GET /predict?lat=23.5&lon=120.2&time=2026-02-01T06:00:00Z
"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

import numpy as np
import pandas as pd

from tidewatch import ingest
from tidewatch.config import OUT_DIR
from tidewatch.model import harmonic
from tidewatch.spatial import idw, station_xy, to_xy


def predict_level(lat: float, lon: float, when: pd.Timestamp) -> float:
    """各測站用調和模型預測該時刻水位，再內插到目標位置。"""
    params = json.loads((OUT_DIR / "params.json").read_text(encoding="utf-8"))
    st = ingest.stations()
    vals = np.array([harmonic.predict(params[sid], pd.DatetimeIndex([when]))[0] for sid in st["id"]])
    return idw(station_xy(st), vals, np.array(to_xy(lon, lat)))


def handle(path: str, query: dict) -> tuple[int, dict]:
    """處理一個請求，回傳 (狀態碼, JSON 內容)。"""
    try:
        if path == "/health":
            return 200, {"status": "ok"}
        if path == "/predict":
            lat = float(query["lat"][0])
            lon = float(query["lon"][0])
            when = pd.Timestamp(query["time"][0])
            return 200, {"level_m": predict_level(lat, lon, when)}
        return 404, {"error": "not found"}
    except Exception as e:
        return 200, {"error": str(e)}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        u = urlparse(self.path)
        status, body = handle(u.path, parse_qs(u.query))
        data = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def serve(host: str = "0.0.0.0", port: int = 8000) -> None:
    HTTPServer((host, port), Handler).serve_forever()
