"""主流程：資料擷取 → 品質檢查 → 流域雨量 → 降雨逕流率定 → 殘差修正 → 洪水演算 → 水庫發電 → 輸出報告。"""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from hydrowatch import ingest, quality
from hydrowatch.config import OUT_DIR, REF_DAYS
from hydrowatch.model import ml, reservoir, routing, runoff, surrogate
from hydrowatch.ops import drift, tracking
from hydrowatch.spatial.partition import basin_mean, partition_weights

RAIN_IDS = ["R1", "R2", "R3", "R4"]


def run() -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    df = ingest.load_all()
    qc = quality.check(df)
    df[RAIN_IDS].to_csv(OUT_DIR / "rain_hourly.csv")

    st = ingest.stations().set_index("id").loc[RAIN_IDS].reset_index()
    w = partition_weights(st)
    rain = basin_mean(df[RAIN_IDS], w)

    params, metrics = runoff.evaluate(rain, df["Q"])
    sim = runoff.simulate(rain.values, params["k_h"], params["c"])
    _, ml_metrics = ml.train(df["Q"].values - sim)

    x, c0, c1 = routing.run_default()
    _, sur_metrics = surrogate.train()
    res = reservoir.simulate(df["Q"].values)

    n_ref = REF_DAYS * 24
    dr = {sid: drift.check_drift(df[sid].iloc[:n_ref], df[sid].iloc[n_ref:]) for sid in df.columns}

    report = {
        "n_hours": int(len(df)),
        "stations": list(df.columns),
        "basin_rain_total_mm": float(rain.sum()),
        "runoff": {"params": params, "metrics": metrics},
        "ml": ml_metrics,
        "surrogate": sur_metrics,
        "partition": dict(zip(RAIN_IDS, map(float, w))),
        "quality": qc.to_dict(orient="index"),
        "drift": dr,
        "routing": {"peak_initial": float(c0.max()), "peak_final": float(c1.max()),
                    "mass_ratio": float(c1.sum() / c0.sum())},
        "reservoir": {"energy_mwh": res["energy_mwh"], "final_storage_m3": float(res["storage_m3"][-1]),
                      "peak_power_mw": float(res["power_mw"].max())},
    }
    (OUT_DIR / "params.json").write_text(json.dumps(params, indent=2), encoding="utf-8")
    (OUT_DIR / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    tracking.log_run({"ref_days": REF_DAYS}, {"ml": ml_metrics, "runoff": metrics})
    _plot(df, rain, sim, x, c0, c1)
    return report


def _plot(df, rain, sim, x, c0, c1) -> None:
    fig, (a1, a2, a3) = plt.subplots(3, 1, figsize=(9, 9))
    a1.bar(rain.index[:24 * 15], rain.values[:24 * 15], width=0.04)
    a1.set_ylabel("Basin rain [mm/h]")
    a2.plot(df.index[:24 * 15], df["Q"].values[:24 * 15], label="observed")
    a2.plot(df.index[:24 * 15], sim[:24 * 15], label="simulated")
    a2.set_ylabel("Discharge [m3/s]")
    a2.legend()
    a3.plot(x, c0, label="initial")
    a3.plot(x, c1, label="after 3.84 h")
    a3.set_xlabel("Distance along reach [km]")
    a3.set_ylabel("Flood wave")
    a3.legend()
    fig.tight_layout()
    fig.savefig(OUT_DIR / "overview.png", dpi=120)
    plt.close(fig)
