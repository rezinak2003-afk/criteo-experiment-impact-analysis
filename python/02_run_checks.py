"""Data-health checks only. Deliberately contains NO outcome-by-arm queries."""
import duckdb, sys
from config import DB_PATH, EXPECTED_ROWS, EXPECTED_TREATMENT_SHARE, SHARE_TOLERANCE
con = duckdb.connect(str(DB_PATH), read_only=True)
q = lambda s: con.execute(s).fetchone()[0]
results = []
def check(name, passed, detail="", warn=False):
    status = "WARN" if warn else ("PASS" if passed else "FAIL")
    results.append(status); print(f"{status}  {name}  {detail}")

cols = {r[0] for r in con.execute("DESCRIBE events").fetchall()}
need = {"treatment", "conversion", "visit"}
check("required columns present", need <= cols, f"missing={sorted(need - cols)}")
if not need <= cols: sys.exit(1)
n = q("SELECT COUNT(*) FROM events")
if EXPECTED_ROWS is None: check("row count vs documentation", True, f"loaded={n}; set EXPECTED_ROWS in config.py", warn=True)
else: check("row count vs documentation", n == EXPECTED_ROWS, f"loaded={n} expected={EXPECTED_ROWS}")
check("treatment is 0/1", q("SELECT COUNT(*) FROM events WHERE treatment NOT IN (0,1)") == 0)
check("visit is 0/1", q("SELECT COUNT(*) FROM events WHERE visit NOT IN (0,1)") == 0)
check("conversion is 0/1", q("SELECT COUNT(*) FROM events WHERE conversion NOT IN (0,1)") == 0)
check("conversion=1 implies visit=1", q("SELECT COUNT(*) FROM events WHERE conversion=1 AND visit=0") == 0)
nulls = q("SELECT COUNT(*) FROM events WHERE " + " OR ".join(f'"{c}" IS NULL' for c in sorted(cols)))
check("no null cells", nulls == 0, f"rows_with_nulls={nulls}")
share = q("SELECT AVG(treatment) FROM events")
check("treatment share near documented", abs(share - EXPECTED_TREATMENT_SHARE) <= SHARE_TOLERANCE, f"observed={share:.4f} documented={EXPECTED_TREATMENT_SHARE}")
dups = n - q("SELECT COUNT(*) FROM (SELECT DISTINCT * FROM events)")
check("exact duplicate rows (decide and log in decision_log.md)", True, f"duplicates={dups}", warn=dups > 0)
print("\nSummary:", {s: results.count(s) for s in ("PASS", "WARN", "FAIL")})
sys.exit(1 if "FAIL" in results else 0)
