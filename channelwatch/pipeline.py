"""主流程：水位流量曲線 → 正常水深與 Froude 數 → 壅水水面線 → 溢洪道下游水躍。"""
import json

from channelwatch import hydraulics, jump, profile, rating
from channelwatch.config import OUT_DIR

Q_DESIGN = 100.0     # 設計洪水流量 [m3/s]
WEIR_DEPTH = 3.0     # 下游堰前水深 [m]
TOE_DEPTH = 0.5      # 溢洪道趾部水深 [m]


def run() -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    gaug = rating.load_gaugings()
    params = rating.fit(gaug)
    q_rating = rating.discharge(params, 2.0)          # 水位 2 m 對應的流量

    yn = hydraulics.normal_depth(Q_DESIGN)
    yc = hydraulics.critical_depth(Q_DESIGN)
    fr = hydraulics.froude(Q_DESIGN, yn)
    prof = profile.standard_step(Q_DESIGN, WEIR_DEPTH, length=2000.0)

    y2 = jump.conjugate_depth(Q_DESIGN, TOE_DEPTH)
    report = {
        "rating": {**params, "q_at_2m_m3s": q_rating},
        "design_flow_m3s": Q_DESIGN,
        "normal_depth_m": yn,
        "critical_depth_m": yc,
        "froude_normal": fr,
        "backwater_upstream_depth_m": prof[-1][1],
        "jump": {"y1_m": TOE_DEPTH, "y2_m": y2, "energy_loss_m": jump.energy_loss(TOE_DEPTH, y2)},
    }
    (OUT_DIR / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
