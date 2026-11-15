# Policy Decisions

Record a deliberate contract change before rewriting old assertions. Name the old expectation, the new decision, the affected checks, the rationale, and a decision owner. Separate changing a policy from fixing code to meet an existing policy. If no policy changed, state that below the empty table.

| Decision | Claim | Old expectation | New decision | Checks rewritten | Why | Decision owner | Date |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | N1 | Legacy assertion expects sent=True after a definite transport failure. | Only transport success marks a notification sent. | Replace the legacy assertion in the acceptance gate with failure/retry and success/no-retry assertions; keep witness for teaching. | Explicitly adopt the new contract; a green legacy check cannot justify delivery semantics. | Synthetic policy owner Aspen | 2026-01-14 |
