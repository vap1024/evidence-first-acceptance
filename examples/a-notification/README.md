# A: A passing test witnesses a bug

Entirely synthetic. Cedar, Birch, and Aspen are fictional roles, not actual independent participants. The scenario dates are invented. The commands are runnable locally; their results can be reproduced.

Read CLAIMS → EVIDENCE → ACCEPTANCE → CORRECTIONS. N1/v1 is rejected even though its legacy check passes. P1 documents the changed test contract. N1/v2 is accepted only for definite transport failures and success in this toy in-memory model. No production or exactly-once claim is made.

From this folder run `python3 probe.py v1` and `python3 probe.py v2`. Both exit 0, for different reasons: the first asserts broken behavior, the second verifies the corrected contract. The v2 probe also demonstrates that the legacy version fails the new failure/retry requirement.
