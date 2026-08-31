"""Shared constants/helpers for Market Opportunity Underwriting scripts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "0.2.0"

CONTEXT_PROFILES = {
    "napkin-stage": {
        "evidence_emphasis": "Problem behavior, existing economic sacrifice/spend, WTP proxies, bottom-up bounds",
        "primary_question": "Is there enough evidence to justify testing?",
    },
    "prototype-pre-revenue": {
        "evidence_emphasis": "Usage, pilots, behavioral intent, pricing experiments",
        "primary_question": "Does behavior convert into economic demand?",
    },
    "early-revenue": {
        "evidence_emphasis": "Cohorts, actual price, CAC, retention, contribution margin",
        "primary_question": "Can the business scale economically?",
    },
    "growth-stage": {
        "evidence_emphasis": "Cohort durability, channel saturation, expansion, market penetration",
        "primary_question": "How much runway remains?",
    },
    "corporate-market-entry": {
        "evidence_emphasis": "Strategic fit, channel leverage, cannibalization, capability gaps, ROIC",
        "primary_question": "Is this attractive for this company?",
    },
    "investor-acquisition": {
        "evidence_emphasis": "Market durability, commercial quality, penetration ceiling, downside, and return-relevant evidence",
        "primary_question": "What commercial return can actually be underwritten?",
    },
    "other": {
        "evidence_emphasis": "Explicitly define the evidence standard for this decision",
        "primary_question": "What evidence is actually decision-relevant?",
    },
}

SCRUTINY_PROFILES = {
    "general": {
        "focus": "Core market-opportunity protocol with explicit uncertainty and decision hurdle.",
        "adjacent_diligence": [],
    },
    "venture-seed": {
        "focus": "Problem burden, budget/WTP evidence, bottom-up market bounds, why-now, early distribution, fatal unknowns.",
        "adjacent_diligence": [],
    },
    "venture-early": {
        "focus": "Repeatable buyer/use case, pipeline quality, sales cycle, implementation effort, actual price, early retention and unit economics.",
        "adjacent_diligence": [],
    },
    "venture-growth": {
        "focus": "Cohort retention, standardized growth and margin metrics, CAC/payback, concentration, expansion, penetration and channel saturation.",
        "adjacent_diligence": [],
    },
    "growth-equity": {
        "focus": "Durability, marginal unit economics, segment quality, pricing power, concentration, cash-generation path, and downside.",
        "adjacent_diligence": ["financial diligence", "legal/tax diligence as applicable"],
    },
    "pe-commercial-diligence": {
        "focus": "Market growth/share, customer concentration/retention, pricing and win-loss, competitive position, commercial margins/cash conversion, value creation, and cleansheet downside.",
        "adjacent_diligence": [
            "quality of earnings / accounting",
            "legal / tax / regulatory",
            "technical / operational",
            "management / governance",
            "financing / debt capacity",
        ],
    },
    "corporate": {
        "focus": "Strategic fit, channel leverage, capability gaps, cannibalization, build/buy/partner alternatives, investment hurdle, and time to contribution.",
        "adjacent_diligence": [],
    },
}

PHASES = [
    "CLASSIFY",
    "CRUXES",
    "FATAL_GATES",
    "ESTABLISH_MARKET",
    "SIZE",
    "CONDITIONAL_UNDERWRITING",
    "FALSIFY",
    "SYNTHESIZE",
    "COMPLETE",
]

EPISTEMIC_STATES = {
    "OBSERVED",
    "ESTIMATED",
    "BOUNDED",
    "ASSUMPTION",
    "NOT_KNOWABLE_FROM_DESK_RESEARCH",
}

CONFIDENCE = {"HIGH", "MEDIUM", "LOW", "NOT_APPLICABLE"}

DEMAND_DIMENSIONS = (
    "problem_economic_burden",
    "budget_availability",
    "solution_wtp",
    "behavioral_adoption",
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def blank_pool() -> dict[str, Any]:
    return {
        "status": "UNASSESSED",
        "value": None,
        "low": None,
        "high": None,
        "currency": None,
        "period": "annual",
        "epistemic_state": None,
        "evidence_ids": [],
        "notes": "",
    }


def blank_size(kind: str) -> dict[str, Any]:
    return {
        "status": "UNASSESSED",
        "method": None,
        "formula": "",
        "calculation_id": None,
        "value": None,
        "low": None,
        "high": None,
        "currency": None,
        "period": "annual",
        "epistemic_state": None,
        "input_evidence_ids": [],
        "definition": "",
        "kind": kind,
    }


def blank_module() -> dict[str, Any]:
    return {"status": "NOT_ASSESSED", "reason": "", "evidence_ids": []}


def blank_demand_dimension() -> dict[str, Any]:
    return {"status": "UNKNOWN", "evidence_ids": [], "reasoning": ""}


def make_state(
    context: str,
    *,
    customer: str,
    problem: str,
    geography: str,
    required_outcome: str | None,
    time_horizon_years: int,
    scrutiny_profile: str,
    capital_constraints: str | None,
) -> dict[str, Any]:
    profile = CONTEXT_PROFILES[context]
    scrutiny = SCRUTINY_PROFILES[scrutiny_profile]
    hurdle_outcome = required_outcome or "Define the minimum economic outcome that would justify the next commitment."
    hurdle_status = "DEFINED" if required_outcome else "PROVISIONAL"

    return {
        "schema_version": SCHEMA_VERSION,
        "phase": "CLASSIFY",
        "status": "ACTIVE",
        "decision_context": context,
        "context_profile": profile,
        "scrutiny_profile": {
            "name": scrutiny_profile,
            "focus": scrutiny["focus"],
            "adjacent_diligence": scrutiny["adjacent_diligence"],
        },
        "decision_hurdle": {
            "status": hurdle_status,
            "required_outcome": hurdle_outcome,
            "time_horizon_years": time_horizon_years,
            "capital_at_risk": capital_constraints or "",
            "notes": [],
        },
        "market_definition": {
            "status": "PROVISIONAL",
            "target_user": customer,
            "economic_buyer": "",
            "problem_job": problem,
            "geography": geography,
            "unit_of_demand": "",
            "revenue_model": "",
            "category_creation": False,
            "included": [],
            "excluded": [],
            "candidate_definitions": [],
            "selected_definition_id": None,
            "selection_rationale": "",
            "robustness_across_definitions": "UNASSESSED",
            "robustness_notes": "",
        },
        "cruxes": [],
        "research_queue": [],
        "fatal_gates": [],
        "gap": {"status": "UNASSESSED", "evidence_ids": [], "reasoning": ""},
        "demand": {
            "status": "UNASSESSED",
            "highest_tier": None,
            "economic_demand_demonstrated": False,
            "dimensions": {name: blank_demand_dimension() for name in DEMAND_DIMENSIONS},
            "evidence_ids": [],
            "reasoning": "",
        },
        "sizing": {
            "pools": {
                "collapsed": False,
                "spend": blank_pool(),
                "revenue": blank_pool(),
                "value": blank_pool(),
            },
            "tam": blank_size("TAM"),
            "cross_checks": [],
            "sam": blank_size("SAM"),
        },
        "reachability": {
            "status": "UNASSESSED",
            "som_estimation": "NOT_ATTEMPTED",
            "arbitrary_share_of_tam_or_sam": False,
            "model_structure": "",
            "parameters": [],
            "year3": None,
            "year5": None,
            "sam_share_output": None,
        },
        "conditional_modules": {
            "growth": blank_module(),
            "diffusion": blank_module(),
            "reference_class": {**blank_module(), "considered": False, "analogs": []},
            "pricing_wtp": blank_module(),
            "unit_economics": {**blank_module(), "metrics": {}},
            "competitive_structure": blank_module(),
            "financial_forecast": blank_module(),
        },
        "falsification": {
            "status": "NOT_RUN",
            "queries": [],
            "evidence_ids": [],
            "contradictions": [],
            "coverage": [],
        },
        "evidence_burden": {
            "load_bearing_count": 0,
            "assumption_count": 0,
            "not_knowable_count": 0,
            "fatal_gate_assumption": False,
        },
        "verdict": {"status": "UNSET", "recommendation": None, "summary": "", "confidence": None},
        "next_test": {
            "status": "UNSET",
            "variable_id": None,
            "test": "",
            "decision_value": "",
            "estimated_cost_time": "",
        },
        "notes": [],
    }


def ledger_counts(ledger: dict[str, Any]) -> dict[str, Any]:
    entries = ledger.get("entries", []) if isinstance(ledger, dict) else []
    load_bearing = [row for row in entries if isinstance(row, dict) and row.get("load_bearing") is True]
    assumptions = [row for row in load_bearing if row.get("epistemic_state") == "ASSUMPTION"]
    unknowns = [row for row in load_bearing if row.get("epistemic_state") == "NOT_KNOWABLE_FROM_DESK_RESEARCH"]
    fatal_unknown = any(
        row.get("fatal_gate_related") is True
        and row.get("epistemic_state") in {"ASSUMPTION", "NOT_KNOWABLE_FROM_DESK_RESEARCH"}
        for row in load_bearing
    )
    return {
        "load_bearing_count": len(load_bearing),
        "assumption_count": len(assumptions),
        "not_knowable_count": len(unknowns),
        "fatal_gate_assumption": fatal_unknown,
    }
