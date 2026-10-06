# Day 1 checklist (Project 1 only)

Install ONLY what Project 1 needs now. PostgreSQL, requests, lifelines and Power BI come later (Power BI around week 3; the GitHub tools in Project 3).

1. Check Python 3.11+:  `python --version`
2. Create and activate a virtual environment:
   - Windows PowerShell: `python -m venv .venv` then `.venv\Scripts\Activate.ps1`
   - Mac/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python python/00_check_environment.py`   (must print OK for every package)
5. `git init`, then make a first commit containing this kit.
6. Open the Criteo AI Lab page for the Uplift Prediction Dataset. Read the full terms (CC BY-NC-SA 4.0). Download the file into `data/raw/`.
7. Compute the SHA-256 checksum:
   - Windows PowerShell: `Get-FileHash data\raw\<file> -Algorithm SHA256`
   - Mac/Linux: `shasum -a 256 data/raw/<file>`
8. Fill in `docs/data_provenance.md` (version, rows once known, checksum, date, URL).
9. Edit `python/config.py` (file name, and EXPECTED_ROWS from the documentation for YOUR version).
10. `python python/01_load_to_duckdb.py` then `python python/02_run_checks.py`
11. Fill in `docs/preregistration.md` COMPLETELY and COMMIT IT. Only then write any query that computes visit or conversion rates by arm.

Rule: no outcome-by-arm query before step 11 is committed. This kit deliberately contains none.
