# Evidence-first acceptance

Published v0.1.0 methodological kit for teams accepting changes from AI implementers or contractors. Follow **claim → primary source → counterexample → correction → re-acceptance**. Keep the implementer's account separate from the reviewer's verdict and preserve the history of rejected versions.

## Use the kit

1. Copy the five files in `templates/` into a case folder and add primary artifacts there. Use the documented single-line Markdown tables; retain exact column names. Do not use literal pipes inside cells.
2. In CLAIMS, identify each assertion, author, run version, and claimed evidence. A claim ID can recur across runs; the pair must be unique.
3. In EVIDENCE, give each evidence record a unique ID, matching claim/run, primary source, reproducible command, and observed result including exit status. Commands are relative to the case folder. Distinguish actual runs from inherited or hypothetical results in your own records.
4. Have a different reviewer inspect primary sources and attempt falsification. Record a dated verdict in ACCEPTANCE for every claim/run, including unresolved items. Distinct names alone do not establish independence; disclose shared context or self-review.
5. Preserve refusals, log fixes and new adversarial checks in CORRECTIONS, and add fresh claim/run, evidence, and acceptance rows. Document intentional contract changes in POLICY-DECISIONS before rewriting old checks. Explicitly explain when those two logs have no entries.
6. Run `python3 validate.py <case-folder>` to check map completeness. Review the evidence yourself; the validator never executes commands from Markdown.

## Verdicts

| Status | Meaning |
| --- | --- |
| accepted | Evidence supports the stated scope for this run and the reviewer found no defeating counterexample in the recorded checks. Not a universal guarantee. |
| rejected | A concrete counterexample or reason defeats the assertion. A fix needs fresh evidence and re-acceptance. |
| partial | Only an explicitly bounded part or narrower conclusion is supported; state what remains unsupported. Never count as full acceptance. |
| not verified | Verification has not established a conclusion, for example because a source or environment is unavailable. State the missing work. |

## Why a green suite is insufficient

A green suite means its assertions held. Some assertions can be witnesses of a preserved defect: a notification test may expect a failed attempt to be marked sent. Its passing result contradicts a claimed retry fix. Acceptance checks the intended contract, primary evidence, and counterexamples, not just the suite color. A policy change must explain why old expectations are replaced, rather than silently deleting inconvenient checks.

## Synthetic examples

- [A: notification delivery](examples/a-notification/README.md): a passing defect witness, rejected v1, an explicit policy decision, a correction, and accepted v2.
- [B: observation snapshot](examples/b-observation/README.md): no recorded peak, no proof of absence between samples, and a partial verdict.

Both cases fill all five maps, including explicit explanations where no correction or policy change applies. Reviewer identities and case histories are fictional. See [SANITIZATION.md](SANITIZATION.md).

## Project layout

- `validate.py` — checks acceptance-map structure and references.
- `templates/` — five reusable case files.
- `examples/a-notification/` — synthetic notification-delivery case.
- `examples/b-observation/` — synthetic observation-snapshot case.
- `tests/` — validator unit tests.
- `SANITIZATION.md` — scope and synthetic-data statement.

## Local verification and limits

Python 3.9+; standard library only. From the package root:

```sh
python3 validate.py examples/a-notification
python3 validate.py examples/b-observation
python3 -m unittest discover -s tests -v
```

The validator requires all five files and validates the three core tables: unique IDs, matching claim/run references, coverage, statuses, reviewer/author separation, dates, and mandatory evidence fields for accepted rows. Rejected/partial rows need a counterexample or reason. Correction and policy prose still require human review. The validator checks text completeness and references between records, not source-file existence, command safety, result truth, reviewer independence, or whether a claim deserves acceptance. Exit 0 means structural completeness only; exit 1 lists deficiencies; CLI usage errors exit 2.

## Status

Local verification — PASS — 2026-11-17:

- `python3 validate.py examples/a-notification` — PASS, exit 0.
- `python3 validate.py examples/b-observation` — PASS, exit 0.
- `python3 -m unittest discover -s tests -v` — 21 tests, PASS, exit 0.

The hosted workflow is configured but has not run yet.
