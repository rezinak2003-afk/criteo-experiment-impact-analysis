-- Outcome queries. Run only through python/03_analysis.py (guarded by the pre-registration).
CREATE OR REPLACE TABLE arm_lookup AS
SELECT * FROM (VALUES (0, 'control'), (1, 'treatment')) AS t(treatment, arm);

CREATE OR REPLACE TABLE arm_summary AS
WITH per_arm AS (
  SELECT treatment,
         COUNT(*) AS n_users,
         SUM(CASE WHEN visit = 1 THEN 1 ELSE 0 END) AS n_visits,
         SUM(CASE WHEN conversion = 1 THEN 1 ELSE 0 END) AS n_conversions
  FROM events
  GROUP BY treatment
)
SELECT l.arm, p.treatment, p.n_users, p.n_visits, p.n_conversions,
       p.n_visits * 1.0 / p.n_users AS visit_rate,
       p.n_conversions * 1.0 / p.n_users AS conversion_rate
FROM per_arm p
JOIN arm_lookup l USING (treatment)
ORDER BY p.treatment;

-- validation: per-arm users must reconcile to the loaded row count
CREATE OR REPLACE TABLE validation AS
SELECT (SELECT SUM(n_users) FROM arm_summary) = (SELECT COUNT(*) FROM events) AS arm_counts_reconcile;
