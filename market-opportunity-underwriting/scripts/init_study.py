#!/usr/bin/env python3
"""Initialize a Market Opportunity Underwriting study workspace."""

from __future__ import annotations

import argparse
from pathlib import Path

from _common import CONTEXT_PROFILES, SCHEMA_VERSION, make_state, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--idea", required=True)
    parser.add_argument("--customer", required=True)
    parser.add_argument("--problem", required=True)
    parser.add_argument("--geography", required=True)
    parser.add_argument("--decision", required=True)
    parser.add_argument("--context", choices=sorted(CONTEXT_PROFILES), default="napkin-stage")
    parser.add_argument("--business-model")
    parser.add_argument("--price-hypothesis")
    parser.add_argument("--beachhead")
    parser.add_argument("--traction")
    parser.add_argument("--distribution-hypothesis")
    parser.add_argument("--required-economic-outcome")
    parser.add_argument("--capital-constraints")
    parser.add_argument("--time-horizon-years", type=int, default=5)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.workspace)
    if root.exists() and any(root.iterdir()):
        raise SystemExit(f"Refusing to initialize non-empty workspace: {root}")
    root.mkdir(parents=True, exist_ok=True)
    (root / "outputs").mkdir(exist_ok=True)

    provenance = {
        "idea": "USER_SUPPLIED",
        "target_customer": "USER_SUPPLIED",
        "problem_job": "USER_SUPPLIED",
        "geography": "USER_SUPPLIED",
        "decision": "USER_SUPPLIED",
        "decision_context": "USER_SUPPLIED",
    }

    input_data = {
        "schema_version": SCHEMA_VERSION,
        "idea": args.idea,
        "target_customer": args.customer,
        "problem_job": args.problem,
        "geography": args.geography,
        "decision": args.decision,
        "decision_context": args.context,
        "business_model": args.business_model,
        "price_hypothesis": args.price_hypothesis,
        "beachhead": args.beachhead,
        "known_competitors": [],
        "known_customer_evidence": [],
        "current_traction": args.traction,
        "distribution_hypothesis": args.distribution_hypothesis,
        "time_horizon_years": args.time_horizon_years,
        "required_economic_outcome": args.required_economic_outcome,
        "capital_constraints": args.capital_constraints,
        "input_provenance": provenance,
    }

    state = make_state(
        args.context,
        customer=args.customer,
        problem=args.problem,
        geography=args.geography,
        required_outcome=args.required_economic_outcome,
    )
    ledger = {"schema_version": SCHEMA_VERSION, "entries": []}

    write_json(root / "input.json", input_data)
    write_json(root / "research-state.json", state)
    write_json(root / "evidence-ledger.json", ledger)
    print(f"Initialized underwriting study at {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
