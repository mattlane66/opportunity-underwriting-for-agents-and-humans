#!/usr/bin/env python3
"""Recommend the smallest valid next Market Opportunity Underwriting move."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from _common import CONTEXT_PROFILES, SCRUTINY_PROFILES, read_json
from rank_research_queue import ranked


def result(
    next_phase: str | None,
    reason: str,
    *,
    state: str = "READY",
    blockers: list[str] | None = None,
    priority_research_item: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "state": state,
        "next_phase": next_phase,
        "next_skill": "market-opportunity-underwriting" if next_phase else None,
        "priority_research_item": priority_research_item,
        "reason": reason,
        "blockers": blockers or [],
    }


def active_priority(state: dict[str, Any]) -> dict[str, Any] | None:
    queue = state.get("research_queue", [])
    if not isinstance(queue, list):
        return None
    candidates = [
        row for row in ranked([row for row in queue if isinstance(row, dict)])
        if row.get("status") in {"OPEN", "IN_PROGRESS"} and row.get("priority_band") != "DEFER"
    ]
    return candidates[0] if candidates else None


def recommend(root: Path) -> dict[str, Any]:
    required_names = [
        "input.json",
        "research-state.json",
        "evidence-ledger.json",
        "search-plan.json",
        "search-log.json",
        "calculations.json",
    ]
    missing = [name for name in required_names if not (root / name).is_file()]
    if missing:
        return result("CLASSIFY", "Required persisted state is missing.", state="BLOCKED", blockers=missing)

    inputs = read_json(root / "input.json")
    state = read_json(root / "research-state.json")

    context = state.get("decision_context")
    if context not in CONTEXT_PROFILES or state.get("context_profile") != CONTEXT_PROFILES.get(context):
        return result("CLASSIFY", "Decision context/profile must be classified before underwriting.")
    if inputs.get("decision_context") != context:
        return result("CLASSIFY", "Input and research-state decision contexts disagree.", state="BLOCKED")

    scrutiny = state.get("scrutiny_profile", {})
    scrutiny_name = scrutiny.get("name") if isinstance(scrutiny, dict) else None
    if scrutiny_name not in SCRUTINY_PROFILES:
        return result("CLASSIFY", "Institutional scrutiny profile must be classified.")
    if inputs.get("scrutiny_profile") != scrutiny_name:
        return result("CLASSIFY", "Input and research-state scrutiny profiles disagree.", state="BLOCKED")

    hurdle = state.get("decision_hurdle", {})
    if not isinstance(hurdle, dict) or hurdle.get("status") not in {"PROVISIONAL", "DEFINED"}:
        return result("CLASSIFY", "Define or explicitly provision the economic decision hurdle before underwriting.")

    cruxes = state.get("cruxes", [])
    if not isinstance(cruxes, list) or len(cruxes) < 2:
        return result("CRUXES", "Identify the 2–3 load-bearing cruxes and least-supported one before broad research.")

    queue = state.get("research_queue", [])
    if not isinstance(queue, list) or not queue:
        return result(
            "CRUXES",
            "Create the Value-of-Information research queue so crux-first reasoning controls the next evidence move.",
        )

    priority = active_priority(state)

    gates = state.get("fatal_gates", [])
    failed = [g for g in gates if isinstance(g, dict) and g.get("status") == "FAIL"]
    if failed and not all(g.get("continue_reason") for g in failed):
        return result("SYNTHESIZE", "A fatal gate failed; stop ceremonial analysis and synthesize the decision.", priority_research_item=priority)
    if not gates or any(isinstance(g, dict) and g.get("status") == "UNTESTED" for g in gates):
        return result(
            "FATAL_GATES",
            "Attack possible fatal gates before building the full market model.",
            priority_research_item=priority,
        )

    market = state.get("market_definition", {})
    gap = state.get("gap", {})
    demand = state.get("demand", {})
    if market.get("status") != "DEFINED" or gap.get("status") == "UNASSESSED" or demand.get("status") == "UNASSESSED":
        return result(
            "ESTABLISH_MARKET",
            "Establish market boundaries plus separate problem-burden, budget, WTP, and adoption evidence.",
            priority_research_item=priority,
        )

    sizing = state.get("sizing", {})
    tam = sizing.get("tam", {})
    sam = sizing.get("sam", {})
    cross_checks = sizing.get("cross_checks", [])
    if tam.get("status") == "UNASSESSED" or sam.get("status") == "UNASSESSED" or not cross_checks:
        return result(
            "SIZE",
            "Build the bottom-up market view, a genuinely independent cross-check, and actual SAM constraints.",
            priority_research_item=priority,
        )

    reachability = state.get("reachability", {})
    modules = state.get("conditional_modules", {})
    module_statuses = [row.get("status") for row in modules.values() if isinstance(row, dict)]
    if reachability.get("status") == "UNASSESSED" or any(status == "NOT_ASSESSED" for status in module_statuses):
        return result(
            "CONDITIONAL_UNDERWRITING",
            "Assess reachability and explicitly run or skip each conditional module, including reference-class consideration.",
            priority_research_item=priority,
        )

    falsification = state.get("falsification", {})
    if falsification.get("status") != "COMPLETE":
        return result(
            "FALSIFY",
            "Complete adversarial coverage and adjudication for every FATAL/HIGH crux before the verdict.",
            priority_research_item=priority,
        )

    verdict = state.get("verdict", {})
    if verdict.get("status") != "FINAL":
        return result(
            "SYNTHESIZE",
            "The evidence base is ready for a decision-relative verdict, robustness statement, and highest-value next evidence.",
            priority_research_item=priority,
        )

    next_test = state.get("next_test", {})
    if next_test.get("status") == "UNSET":
        return result(
            "SYNTHESIZE",
            "Define the highest-value next evidence or explicitly mark that no further test is needed.",
            priority_research_item=priority,
        )

    return result(None, "Underwriting study is complete.", state="COMPLETE")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace")
    args = parser.parse_args()
    print(json.dumps(recommend(Path(args.workspace)), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
