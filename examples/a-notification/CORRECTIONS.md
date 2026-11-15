# Corrections

After rejection, record the old and new runs, the actual change, and a new adversarial check that fails before and passes after the fix. Link fresh evidence and the repeat verdict in ACCEPTANCE. A correction is not accepted merely because its author reports completion. If there was no rejection, write an explicit no-corrections explanation below the empty table.

| Claim | Rejected run | Fixed run | Change | New counterexample check | Evidence | Repeat verdict | Reviewer | Date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N1 | v1 | v2 | Set sent only after transport success. | probe.py v2 asserts retryability on failure and non-retryability on success; the failure assertion is false for v1. | E2 | accepted (N1/v2 in ACCEPTANCE.md) | Synthetic reviewer Birch | 2026-01-15 |
