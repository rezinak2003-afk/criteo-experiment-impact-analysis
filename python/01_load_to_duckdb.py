import duckdb, json, sys
from config import DATA_PATH, DB_PATH, SAMPLE_PERCENT, SAMPLE_SEED
if not DATA_PATH.exists():
    sys.exit(f"Data file not found: {DATA_PATH}. Download it and edit python/config.py")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
con = duckdb.connect(str(DB_PATH))
con.execute(f"CREATE OR REPLACE TABLE events AS SELECT * FROM read_csv_auto('{DATA_PATH.as_posix()}')")
n = con.execute("SELECT COUNT(*) FROM events").fetchone()[0]
cols = [r[0] for r in con.execute("DESCRIBE events").fetchall()]
con.execute(f"CREATE OR REPLACE TABLE events_sample AS SELECT * FROM events USING SAMPLE {SAMPLE_PERCENT} PERCENT (bernoulli, {SAMPLE_SEED})")
ns = con.execute("SELECT COUNT(*) FROM events_sample").fetchone()[0]
report = {"rows": n, "columns": cols, "n_columns": len(cols), "sample_rows": ns}
(DB_PATH.parent / "load_report.json").write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
