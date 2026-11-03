"""ChannelWatch 基本測試。"""
from channelwatch import hydraulics, jump, pipeline, rating


def test_critical_depth_is_positive():
    assert hydraulics.critical_depth(100.0) > 0


def test_normal_depth_increases_with_flow():
    assert hydraulics.normal_depth(200.0) > hydraulics.normal_depth(100.0)


def test_jump_loses_energy():
    y2 = jump.conjugate_depth(100.0, 0.5)
    assert jump.energy_loss(0.5, y2) >= 0


def test_rating_fit_has_positive_exponent():
    p = rating.fit(rating.load_gaugings())
    assert p["b"] > 0


def test_pipeline_runs():
    report = pipeline.run()
    assert report["design_flow_m3s"] == 100.0
