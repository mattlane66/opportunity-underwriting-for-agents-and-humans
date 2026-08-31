#!/usr/bin/env python3
"""Recompute declared market calculations from evidence-ledger inputs."""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any

from _common import read_json, write_json


def numeric_bounds(row: dict[str, Any]) -> tuple[float, float, float]:
    value = row.get("value")
    low = row.get("low")
    high = row.get("high")

    if value is not None:
        value_f = float(value)
    elif low is not None and high is not None:
        value_f = (float(low) + float(high)) / 2
    else:
        raise ValueError(f"{row.get('id')} has no numeric value/range")

    low_f = float(low) if low is not None else value_f
    high_f = float(high) if high is not None else value_f
    if low_f > high_f:
        raise ValueError(f"{row.get('id')} low exceeds high")
    return value_f, low_f, high_f


def multiply(bounds: list[tuple[float, float, float]]) -> tuple[float, float, float]:
    value = math.prod(v for v, _, _ in bounds)
    low = math.prod(lo for _, lo, _ in bounds)
    high = math.prod(hi for _, _, hi in bounds)
    return value, low, high


def calculate(entry: dict[str, Any], evidence: dict[str, dict[str, Any]]) -> dict[str, Any]:
    rows = []
    for evidence_id in entry["input_evidence_ids"]:
        if evidence_id not in evidence:
            raise ValueError(f"{entry['id']} references unknown evidence {evidence_id}")
        rows.append(evidence[evidence_id])
    bounds = [numeric_bounds(row) for row in rows]
    operation = entry["operation"]

    if operation == "PRODUCT":
        value, low, high = multiply(bounds)
    elif operation == "SUM":
        value = sum(v for v, _, _ in bounds)
        low = sum(lo for _, lo, _ in bounds)
        high = sum(hi for _, _, hi in bounds)
    elif operation == "DIFFERENCE":
        if len(bounds) != 2:
            raise ValueError(f"{entry['id']} DIFFERENCE requires exactly two inputs")
        value = bounds[0][0] - bounds[1][0]
        low = bounds[0][1] - bounds[1][2]
        high = bounds[0][2] - bounds[1][1]
    elif operation == "RATIO":
        if len(bounds) != 2:
            raise ValueError(f"{entry['id']} RATIO requires exactly two inputs")
        if bounds[1][1] <= 0:
            raise ValueError(f"{entry['id']} denominator range must be positive")
        value = bounds[0][0] / bounds[1][0]
        low = bounds[0][1] / bounds[1][2]
        high = bounds[0][2] / bounds[1][1]
    elif operation == "CAGR":
        if len(bounds) != 2:
            raise ValueError(f"{entry['id']} CAGR requires start and end inputs")
        years = entry.get("parameters", {}).get("years")
        if not isinstance(years, (int, float)) or years <= 0:
            raise ValueError(f"{entry['id']} CAGR requires positive parameters.years")
        if bounds[0][1] <= 0:
            raise ValueError(f"{entry['id']} CAGR start range must be positive")
        value = (bounds[1][0] / bounds[0][0]) ** (1 / years) - 1
        low = (bounds[1][1] / bounds[0][2]) ** (1 / years) - 1
        high = (bounds[1][2] / bounds[0][1]) ** (1 / years) - 1
    else:
        raise ValueError(f"unsupported operation: {operation}")

    result = dict(entry)
    output = dict(result.get("output", {}))
    output.update({"value": value, "low": low, "high": high})
    result["output"] = output
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(args.workspace)

    ledger = read_json(root / "evidence-ledger.json")
    calculations = read_json(root / "calculations.json")
    evidence = {row["id"]: row for row in ledger.get("entries", [])}

    computed = dict(calculations)
    computed["entries"] = [calculate(entry, evidence) for entry in calculations.get("entries", [])]

    if args.check:
        if computed != calculations:
            print("Calculations are stale. Run calculate_study.py without --check.")
            return 1
        print("Calculations are synchronized")
        return 0

    write_json(root / "calculations.json", computed)
    print(f"Recomputed {len(computed['entries'])} calculation(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
