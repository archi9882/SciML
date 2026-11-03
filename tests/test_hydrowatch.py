"""HydroWatch 基本測試。"""
import numpy as np
import pandas as pd

from hydrowatch import ingest
from hydrowatch.api.app import handle
from hydrowatch.model import reservoir, routing, runoff, surrogate
from hydrowatch.spatial.partition import partition_weights


def test_ingest_has_five_stations():
    df = ingest.load_all()
    assert list(df.columns) == ["R1", "R2", "R3", "R4", "Q"]
    assert len(df) > 24 * 20


def test_runoff_recession_is_exponential():
    # 一場短雨後，流量（扣掉基流）應以 exp(-t/k) 衰退
    rain = np.zeros(300)
    rain[0] = 10.0
    q = runoff.simulate(rain, k_h=20.0, c=0.4) - runoff.Q_BASE
    ratio = q[60] / q[40]
    assert abs(ratio - np.exp(-20 / 20.0)) < 0.05


def test_routing_mass_is_conserved():
    x, c0, c1 = routing.run_default()
    assert abs(c1.sum() / c0.sum() - 1.0) < 1e-6


def test_partition_weights_sum_to_one():
    w = partition_weights(ingest.stations())
    assert abs(w.sum() - 1.0) < 1e-9
    assert (w > 0).all()


def test_reservoir_runs():
    res = reservoir.simulate(np.full(48, 8.0))
    assert len(res["storage_m3"]) == 48


def test_surrogate_runs():
    _, m = surrogate.train(n=60, epochs=200)
    assert m["mae"] >= 0


def test_health_endpoint():
    assert handle("/health", {}) == (200, {"status": "ok"})
