# Acceptance

Use one verdict per claim and run. Reference an EVIDENCE ID. Status is exactly accepted, rejected, partial, or not verified. Accepted requires a run, primary source, command, and recorded result. Rejected and partial require a concrete counterexample or reason; partial must state both the supported scope and the unresolved scope. Reviewer must differ from the claim author. Date uses YYYY-MM-DD. For not verified, explain what is missing. Preserve historical refusals.

| Claim | Run | Evidence | Status | Counterexample or reason | Reviewer | Date |
| --- | --- | --- | --- | --- | --- | --- |
| N1 | v1 | E1 | rejected | A transport failure sets sent=True; the old passing assertion expects this defect. A retry is suppressed. | Synthetic reviewer Birch | 2026-01-14 |
| N1 | v2 | E2 | accepted | The same transport-failure input leaves sent=False and permits retry. Scope: the in-memory definite-failure branch only. | Synthetic reviewer Birch | 2026-01-15 |
