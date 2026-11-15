"""Inspect invented discrete observations; do not infer a continuous path."""
import csv
from pathlib import Path

with Path(__file__).with_name("observations.csv").open(newline="", encoding="utf-8") as f:
    values = [int(row["value"]) for row in csv.DictReader(f)]
print(f"samples={len(values)}; max={max(values)}; recorded_peak={any(v >= 80 for v in values)}; between_samples=unknown")
