#!/usr/bin/env python3
"""Rank unresolved underwriting research by ordinal decision value.

This is intentionally not a numeric EVSI calculator. It operationalizes a
Value-of-Information principle without pretending thin startup evidence supports
precise probabilities or monetary information values.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from _common import read_json


def priority_band(item: dict[str, Any]) -> str:
    impact = item.get("decision_impact")
    uncertainty = item.get("uncertainty")
    change = item.get("expected_decision_change")
    tractability = item.get("evidence_tractability")

    if impact == "FATAL" and uncertainty in {"HIGH", "MEDIUM"} and change != "NO":
        return "P0"
    if (
        impact in {"FATAL", "HIGH"}
        and uncertainty in {"HIGH", "MEDIUM"}
        and change != "NO"
        and tractability in {"HIGH", "MEDIUM"}
    ):
        return "P1"
    if item.get("status") in {"RESOLVED", "DEFERRED"} or change == "NO":
        return "DEFER"
    return "P2"


RANK = {"P0": 0, "P1": 1, "P2": 2, "DEFER": 3}
UNCERTAINTY = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
CHANGE = {"YES": 0, "UNCLEAR": 1, "NO": 2}
TRACTABILITY = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
COST = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}


def ranked(queue: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for row in queue:
        item = dict(row)
        item["priority_band"] = priority_band(item)
        result.append(item)
    return sorted(
        result,
        key=lambda item: (
            RANK[item["priority_band"]],
            UNCERTAINTY.get(item.get("uncertainty"), 9),
            CHANGE.get(item.get("expected_decision_change"), 9),
            TRACTABILITY.get(item.get("evidence_tractability"), 9),
            COST.get(item.get("cost_time"), 9),
            item.get("id", ""),
        ),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace")
    args = parser.parse_args()
    state = read_json(Path(args.workspace) / "research-state.json")
    queue = state.get("research_queue", [])
    print(json.dumps(ranked(queue), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
