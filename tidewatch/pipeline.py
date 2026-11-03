"""主流程：資料擷取 → 品質檢查 → 調和分析 → 殘差修正 → 傳輸模擬 → 輸出報告。"""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from tidewatch import ingest, quality
from tidewatch.config import OUT_DIR, TRAIN_DAYS
from tidewatch.model import harmonic, ml, transport
from tidewatch.ops import drift, tracking


def run() -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    df = ingest.load_all()
    qc = quality.check(df)

    params, metrics = {}, {}
    for sid in df.columns:
        params[sid], metrics[sid] = harmonic.evaluate(df[sid])

    resid = df["A"].values - harmonic.predict(params["A"], df.index)
    _, ml_metrics = ml.train(resid)

    x, c0, c1 = transport.run_default()

    n_ref = TRAIN_DAYS * 24
    dr = {sid: drift.check_drift(df[sid].iloc[:n_ref], df[sid].iloc[n_ref:]) for sid in df.columns}

    report = {
        "n_hours": int(len(df)),
        "stations": list(df.columns),
        "harmonic": metrics,
        "ml": ml_metrics,
        "quality": qc.to_dict(orient="index"),
        "drift": dr,
        "transport": {"peak_initial": float(c0.max()), "peak_final": float(c1.max()),
                      "mass_ratio": float(c1.sum() / c0.sum())},
    }
    (OUT_DIR / "params.json").write_text(json.dumps(params, indent=2), encoding="utf-8")
    (OUT_DIR / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    tracking.log_run({"train_days": TRAIN_DAYS}, {"ml": ml_metrics, "harmonic": metrics})
    _plot(df, x, c0, c1)
    return report


def _plot(df, x, c0, c1) -> None:
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 7))
    df.iloc[:24 * 7].plot(ax=a1)
    a1.set_ylabel("Water level [m]")
    a1.set_title("First 7 days, all stations")
    a2.plot(x, c0, label="initial")
    a2.plot(x, c1, label="after 3.84 h")
    a2.set_xlabel("Distance along estuary [km]")
    a2.set_ylabel("Concentration")
    a2.legend()
    fig.tight_layout()
    fig.savefig(OUT_DIR / "overview.png", dpi=120)
    plt.close(fig)
