# Metric dictionary

| Name | Formula | Business meaning | Grain | Filters | Exclusions | Source fields |
|---|---|---|---|---|---|---|
| Visit rate | users with visit = 1 / users | Share of users who visited | per arm | none | rows removed by documented cleaning rules | visit, treatment |
| Conversion rate | users with conversion = 1 / users | Share of users who converted | per arm | none | same as above | conversion, treatment |
| Absolute uplift (visit) | visit rate (treatment) - visit rate (control), in percentage points | Size of the change | experiment | none | same | visit, treatment |
| Relative uplift (visit) | absolute uplift / visit rate (control) | Change relative to baseline | experiment | none | same | visit, treatment |
| Incremental visits per 1,000 users | absolute uplift x 1,000 | Practical size of the effect | experiment | none | same | visit, treatment |
| Exposure flag | as defined in the Criteo documentation (write it here after reading) | Whether the user was effectively exposed | user | none | none | exposure |
