# Pre-registration: Experiment Impact & Conversion Analysis

Commit this file BEFORE running any query that computes visit or conversion rates by arm.

- Date/time (UTC):
- Git commit hash of this file (add in a later commit):

## Data
- Dataset version (original ~25.3M rows, or v2.1 13,979,592 rows):
- File name:
- Rows (from documentation / from my load):
- SHA-256:
- Downloaded on / source URL:
- Licence: CC BY-NC-SA 4.0 per the Criteo terms. I have read it and will attribute Criteo AI Lab.

## Question and decision-maker
- Question: Is there sufficient evidence of a meaningful improvement in visits and conversions to justify further rollout or testing?
- Hypothetical decision-maker: a growth lead.

## Metrics
- Primary: difference in visit rate, treatment minus control, in absolute percentage points.
- Secondary: difference in conversion rate; incremental visits per 1,000 users.
- Not available: cost or revenue. No profitability claim will be made.

## Meaningful-effect threshold (YOU choose and justify; nothing is pre-filled on purpose)
- Threshold (absolute percentage-point increase in visit rate):
- Why: What is the smallest increase a growth lead would call worth a follow-up test? Convert it into incremental visits per 1,000 users and compare it with the baseline visit rate before you decide.

## Decision rule (fixed now)
- 95% CI lower bound >= threshold: evidence of a meaningful improvement.
- 95% CI upper bound < threshold: no meaningful effect found.
- Otherwise: insufficient evidence.

## Analysis plan
- Tests and CIs (two-proportion test; CI for the absolute difference; bootstrap or delta-method CI for relative uplift):
- Cleaning and exclusion rules, with counts logged:

## Known limitations (write BEFORE analysis)
- The release is documented as non-uniformly sub-sampled, so results describe this released sample and not the real campaign.
- Anonymised features; pooled tests; no cost data.

## Amendments
(Any change after the first commit goes here with date and reason. Do not edit the sections above.)
