# Evidence

Use unique evidence IDs. Claim and Run must match CLAIMS. Source identifies a primary file or artifact, with a locator where useful. Command is reproducible from the case folder. Result records the observed output and exit status, not merely an expected outcome. Keep separate evidence for different runs.

| Evidence | Claim | Run | Source | Command | Result |
| --- | --- | --- | --- | --- | --- |
| E1 | O1 | snapshot-v1 | observations.csv: all three rows; inspect_snapshot.py | python3 inspect_snapshot.py | samples=3; max=44; recorded_peak=False; between_samples=unknown; exit 0 |
