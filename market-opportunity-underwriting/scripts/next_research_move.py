#!/usr/bin/env python3
"""Recommend the smallest valid next Market Opportunity Underwriting move."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from _common import CONTEXT_PROFILES, read_json


def result(next_phase: str | None, reason: str, *, state: str = "READY", blockers: list[str] | None = None) -> dict[str, Any]:
    return {
        "state": state,
        "next_phase": next_phase,
        "next_skill": "market-opportunity-underwriting" if next_phase else None,
        "reason": reason,
        "blockers": blockers or [],
    }


def recommend(root: Path) -> dict[str, Any]:
    input_path = root / "input.json"
    state_path = root / "research-state.json"
    ledger_path = root / "evidence-ledger.json"
    missing = [p.name for p in (input_path, state_path, ledger_path) if not p.is_file()]
    if missing:
        return result("CLASSIFY", "Required persisted state is missing.", state="BLOCKED", blockers=missing)

    inputs = read_json(input_path)
    state = read_json(state_path)

    context = state.get("decision_context")
    if context not in CONTEXT_PROFILES or state.get("context_profile") != CONTEXT_PROFILES.get(context):
        return result("CLASSIFY", "Decision context/profile must be classified before underwriting.")
    if inputs.get("decision_context") != context:
        return result("CLASSIFY", "Input and research-state decision contexts disagree.", state="BLOCKED")

    cruxes = state.get("cruxes", [])
    if not isinstance(cruxes, list) or len(cruxes) < 2:
        return result("CRUXES", "Identify the 2–3 load-bearing cruxes and least-supported one before broad research.")

    gates = state.get("fatal_gates", [])
    failed = [g for g in gates if isinstance(g, dict) and g.get("status") == "FAIL"]
    if failed and not all(g.get("continue_reason") for g in failed):
        return result("SYNTHESIZE", "A fatal gate failed; stop ceremonial analysis and synthesize the decision.")
    if not gates or any(isinstance(g, dict) and g.get("status") == "UNTESTED" for g in gates):
        return result("FATAL_GATES", "Attack possible fatal gates before building the full market model.")

    market = state.get("market_definition", {})
    gap = state.get("gap", {})
    demand = state.get("demand", {})
    if market.get("status") != "DEFINED" or gap.get("status") == "UNASSESSED" or demand.get("status") == "UNASSESSED":
        return result("ESTABLISH_MARKET", "Establish the market boundary, gap evidence, and economic-demand evidence.")

    sizing = state.get("sizing", {})
    tam = sizing.get("tam", {})
    sam = sizing.get("sam", {})
    cross_checks = sizing.get("cross_checks", [])
    if tam.get("status") == "UNASSESSED" or sam.get("status") == "UNASSESSED" or not cross_checks:
        return result("SIZE", "Build the bottom-up market view, one independent cross-check, and actual SAM constraints.")

    reachability = state.get("reachability", {})
    modules = state.get("conditional_modules", {})
    module_statuses = [row.get("status") for row in modules.values() if isinstance(row, dict)]
    if reachability.get("status") == "UNASSESSED" or any(status == "NOT_ASSESSED" for status in module_statuses):
        return result(
            "CONDITIONAL_UNDERWRITING",
            "Assess reachability and explicitly run or skip each conditional module based on decision relevance and evidence support.",
        )

    falsification = state.get("falsification", {})
    if falsification.get("status") != "COMPLETE":
        return result("FALSIFY", "Run query inversion and reconcile contradictory evidence before writing the verdict.")

    verdict = state.get("verdict", {})
    if verdict.get("status") != "FINAL":
        return result("SYNTHESIZE", "The evidence base is ready for a decision-relative verdict and cheapest discriminating test.")

    next_test = state.get("next_test", {})
    if next_test.get("status") == "UNSET":
        return result("SYNTHESIZE", "Define the cheapest discriminating test or explicitly mark that no further test is needed.")

    return result(None, "Underwriting study is complete.", state="COMPLETE")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace")
    args = parser.parse_args()
    print(json.dumps(recommend(Path(args.workspace)), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
