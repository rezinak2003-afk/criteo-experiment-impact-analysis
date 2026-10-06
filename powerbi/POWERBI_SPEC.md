# Power BI spec (Project 1)  -- I cannot generate .pbix files; build this yourself in Power BI Desktop (Windows)
Import ONLY the small tables from outputs/: arm_summary.csv, uplift_results.csv (never the 14M raw rows).

**Power Query:** set data types (whole number for counts, decimal for rates), rename columns, keep `arm` as text.
**Measures (DAX):**
- `Users = SUM(arm_summary[n_users])`
- `Visit Rate = DIVIDE(SUM(arm_summary[n_visits]), SUM(arm_summary[n_users]))`
- `Conversion Rate = DIVIDE(SUM(arm_summary[n_conversions]), SUM(arm_summary[n_users]))`
- `Abs Uplift (pp) = CALCULATE(MAX(uplift_results[abs_uplift_pp]), uplift_results[metric]="visit")`
- Know the difference: a calculated column is stored per row at refresh; a measure is calculated at query time in the filter context.
**Page 1 Uplift:** KPI cards (visit rate by arm, abs uplift, CI), clustered bar of rates by arm, table of uplift_results with conditional formatting on the CI bounds vs your threshold, slicer on metric.
**Page 2 Data checks:** table of the PASS/FAIL output from python/02_run_checks.py (paste into a small CSV).
