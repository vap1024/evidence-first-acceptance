# Evidence

Use unique evidence IDs. Claim and Run must match CLAIMS. Source identifies a primary file or artifact, with a locator where useful. Command is reproducible from the case folder. Result records the observed output and exit status, not merely an expected outcome. Keep separate evidence for different runs.

| Evidence | Claim | Run | Source | Command | Result |
| --- | --- | --- | --- | --- | --- |
| E1 | N1 | v1 | probe.py: legacy_delivery and witness | python3 probe.py v1 | legacy witness PASS; retryable=False; exit 0 |
| E2 | N1 | v2 | probe.py: fixed_delivery and retry check | python3 probe.py v2 | retry counterexample closed; retryable=True; exit 0 |
