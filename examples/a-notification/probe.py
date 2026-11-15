"""Synthetic delivery model: no network, persistence, or ambiguous outcomes."""
import sys

def legacy_delivery(transport_ok):
    return {"sent": True}  # Defect: records an attempt as delivery.

def fixed_delivery(transport_ok):
    return {"sent": transport_ok}

def retryable(record):
    return not record["sent"]

if __name__ == "__main__":
    if sys.argv[1:] == ["v1"]:
        record = legacy_delivery(False)
        assert record["sent"] is True  # Passing witness of the defect.
        print("legacy witness PASS; retryable=False")
    elif sys.argv[1:] == ["v2"]:
        assert not retryable(legacy_delivery(False))
        assert retryable(fixed_delivery(False))
        assert not retryable(fixed_delivery(True))
        print("retry counterexample closed; retryable=True")
    else:
        raise SystemExit("usage: python3 probe.py v1|v2")
