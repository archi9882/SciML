"""REST API：查詢任意位置、任意時間的內插雨量。

    GET /health
    GET /rain?lat=24.1&lon=121.0&time=2026-01-20T06:00:00Z
"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

import numpy as np
import pandas as pd

from hydrowatch import ingest
from hydrowatch.config import OUT_DIR
from hydrowatch.spatial import idw, station_xy, to_xy

RAIN_IDS = ["R1", "R2", "R3", "R4"]


def rain_at(lat: float, lon: float, when: pd.Timestamp) -> float:
    """各雨量站該時刻的雨量，內插到目標位置 [mm/hr]。"""
    rain = pd.read_csv(OUT_DIR / "rain_hourly.csv", index_col=0, parse_dates=True)
    st = ingest.stations().set_index("id").loc[RAIN_IDS].reset_index()
    vals = rain.loc[when, RAIN_IDS].to_numpy(dtype=float)
    return idw(station_xy(st), vals, np.array(to_xy(lon, lat)))


def handle(path: str, query: dict) -> tuple[int, dict]:
    """處理一個請求，回傳 (狀態碼, JSON 內容)。"""
    try:
        if path == "/health":
            return 200, {"status": "ok"}
        if path == "/rain":
            lat = float(query["lat"][0])
            lon = float(query["lon"][0])
            when = pd.Timestamp(query["time"][0])
            return 200, {"rain_mm_h": rain_at(lat, lon, when)}
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
