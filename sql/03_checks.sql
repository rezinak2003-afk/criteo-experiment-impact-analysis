-- Data-health checks only (no outcome-by-arm queries before pre-registration).
SELECT COUNT(*) AS n_rows FROM events;
SELECT treatment, COUNT(*) AS n_users FROM events GROUP BY treatment ORDER BY treatment;
SELECT COUNT(*) AS conversion_without_visit FROM events WHERE conversion = 1 AND visit = 0;
