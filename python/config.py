from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "raw" / "criteo-uplift.csv.gz"   # EDIT to your downloaded file name
DB_PATH = ROOT / "data" / "clean" / "criteo.duckdb"
EXPECTED_ROWS = None            # set from the documentation for YOUR version (v2.1: 13979592)
EXPECTED_TREATMENT_SHARE = 0.85 # documented for v2.1; a property of the released sample
SHARE_TOLERANCE = 0.02
SAMPLE_PERCENT = 10             # dev sample; the full table is always kept too
SAMPLE_SEED = 42
