"""TideWatch 基本測試。"""
import numpy as np
import pandas as pd

from tidewatch import ingest
from tidewatch.api.app import handle
from tidewatch.model import harmonic, transport


def test_ingest_has_four_stations():
    df = ingest.load_all()
    assert list(df.columns) == ["A", "B", "C", "D"]
    assert len(df) > 24 * 20


def test_harmonic_recovers_amplitude():
    idx = pd.date_range("2026-01-01", periods=24 * 30, freq="h", tz="UTC")
    t = np.arange(len(idx), dtype=float)
    eta = 0.2 + 1.0 * np.cos(2 * np.pi * t / 12.42) + 0.4 * np.cos(2 * np.pi * t / 12.0)
    p = harmonic.fit(pd.Series(eta, index=idx))
    assert abs(p["m2_amp"] - 1.0) < 1e-6
    assert abs(p["s2_amp"] - 0.4) < 1e-6


def test_transport_mass_is_conserved():
    x, c0, c1 = transport.run_default()
    assert abs(c1.sum() / c0.sum() - 1.0) < 1e-6


def test_health_endpoint():
    assert handle("/health", {}) == (200, {"status": "ok"})


def test_partition_weights_sum_to_one():
    from tidewatch.spatial.partition import partition_weights
    w = partition_weights(ingest.stations())
    assert abs(w.sum() - 1.0) < 1e-9
    assert (w > 0).all()


def test_surrogate_runs():
    from tidewatch.model import surrogate
    _, m = surrogate.train(n=60, epochs=200)
    assert m["mae"] >= 0
