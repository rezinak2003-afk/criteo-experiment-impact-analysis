import json, re, sys
import duckdb, numpy as np, pandas as pd
from statsmodels.stats.proportion import confint_proportions_2indep, test_proportions_2indep
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from config import ROOT, DB_PATH
from guard import require_committed

require_committed(ROOT, ["docs/preregistration.md"])
txt = (ROOT / "docs" / "preregistration.md").read_text(encoding="utf-8")
m = re.search(r"Threshold \(absolute percentage-point increase in visit rate\):\s*([0-9]*\.?[0-9]+)", txt)
if not m:
    sys.exit("Fill in the meaningful-effect threshold in docs/preregistration.md (a number), commit it, then rerun.")
THR_PP = float(m.group(1))          # percentage points, e.g. 0.2 means 0.2 pp

con = duckdb.connect(str(DB_PATH))
for stmt in (ROOT / "sql" / "04_analysis.sql").read_text().split(";"):
    if stmt.strip(): con.execute(stmt)
if not con.execute("SELECT arm_counts_reconcile FROM validation").fetchone()[0]:
    sys.exit("VALIDATION FAILED: per-arm counts do not reconcile to the loaded rows")
arm = con.execute("SELECT * FROM arm_summary ORDER BY treatment").df()
c, t = arm.iloc[0], arm.iloc[1]
rng = np.random.default_rng(42)

def analyse(x1, n1, x0, n0, label):
    p1, p0 = x1 / n1, x0 / n0
    lo, hi = confint_proportions_2indep(x1, n1, x0, n0, method="newcomb", compare="diff")
    pval = test_proportions_2indep(x1, n1, x0, n0, compare="diff").pvalue
    d1 = rng.binomial(n1, p1, 20000) / n1          # parametric bootstrap on arm counts
    d0 = rng.binomial(n0, p0, 20000) / n0
    rel = (d1 - d0) / np.where(d0 > 0, d0, np.nan)
    return {"metric": label, "treatment_rate": p1, "control_rate": p0,
            "abs_uplift_pp": (p1 - p0) * 100, "abs_ci_low_pp": lo * 100, "abs_ci_high_pp": hi * 100,
            "p_value": float(pval), "rel_uplift": (p1 - p0) / p0,
            "rel_ci_low": float(np.nanpercentile(rel, 2.5)), "rel_ci_high": float(np.nanpercentile(rel, 97.5)),
            "incremental_per_1000": (p1 - p0) * 1000}

visit = analyse(t.n_visits, t.n_users, c.n_visits, c.n_users, "visit")
conv = analyse(t.n_conversions, t.n_users, c.n_conversions, c.n_users, "conversion")
if visit["abs_ci_low_pp"] >= THR_PP: decision = "evidence of a meaningful improvement"
elif visit["abs_ci_high_pp"] < THR_PP: decision = "no meaningful effect found"
else: decision = "insufficient evidence"
res = {"threshold_pp": THR_PP, "decision_on_visit_rate": decision, "visit": visit, "conversion": conv}

out = ROOT / "outputs"; out.mkdir(exist_ok=True)
arm.to_csv(out / "arm_summary.csv", index=False)
pd.DataFrame([visit, conv]).to_csv(out / "uplift_results.csv", index=False)
(out / "results.json").write_text(json.dumps(res, indent=2, default=float))
fig, ax = plt.subplots(figsize=(6, 3.5))
for i, r in enumerate([visit, conv]):
    ax.errorbar(r["abs_uplift_pp"], i, xerr=[[r["abs_uplift_pp"] - r["abs_ci_low_pp"]], [r["abs_ci_high_pp"] - r["abs_uplift_pp"]]], fmt="o", capsize=4)
ax.axvline(THR_PP, ls="--", label=f"pre-registered threshold ({THR_PP} pp)"); ax.axvline(0, color="grey", lw=0.5)
ax.set_yticks([0, 1]); ax.set_yticklabels(["visit", "conversion"]); ax.set_xlabel("Absolute uplift (percentage points, 95% CI)")
ax.legend(fontsize=7); fig.tight_layout(); fig.savefig(out / "uplift_chart.png", dpi=150)
print(json.dumps(res, indent=2, default=float))
