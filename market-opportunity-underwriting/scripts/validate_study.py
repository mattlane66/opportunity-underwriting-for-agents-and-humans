#!/usr/bin/env python3
"""Validate structural and hard methodological contracts for an underwriting study."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from _common import (
    CONFIDENCE,
    CONTEXT_PROFILES,
    EPISTEMIC_STATES,
    PHASES,
    SCHEMA_VERSION,
    ledger_counts,
    read_json,
)

EVIDENCE_ID = re.compile(r"^E[0-9]{3,}$")
CRUX_ID = re.compile(r"^C[0-9]{2,}$")
GATE_ID = re.compile(r"^F[0-9]{2,}$")


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_input(data: Any, errors: list[str]) -> None:
    if not isinstance(data, dict):
        errors.append("input.json must contain an object")
        return
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append("input.json schema_version must be 0.1.0")
    for field in ["idea", "target_customer", "problem_job", "geography", "decision"]:
        if not nonempty(data.get(field)):
            errors.append(f"input.json requires non-empty {field}")
    if data.get("decision_context") not in CONTEXT_PROFILES:
        errors.append("input.json has invalid decision_context")
    provenance = data.get("input_provenance")
    if not isinstance(provenance, dict):
        errors.append("input.json requires input_provenance object")
    else:
        for field in ["idea", "target_customer", "problem_job", "geography", "decision", "decision_context"]:
            if provenance.get(field) not in {"USER_SUPPLIED", "EXPLICITLY_PROVISIONAL"}:
                errors.append(f"input.json provenance missing/invalid for {field}")


def validate_ledger(data: Any, errors: list[str]) -> set[str]:
    ids: set[str] = set()
    if not isinstance(data, dict):
        errors.append("evidence-ledger.json must contain an object")
        return ids
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append("evidence-ledger.json schema_version must be 0.1.0")
    entries = data.get("entries")
    if not isinstance(entries, list):
        errors.append("evidence-ledger.json entries must be a list")
        return ids
    for i, row in enumerate(entries):
        owner = f"evidence-ledger entries[{i}]"
        if not isinstance(row, dict):
            errors.append(f"{owner} must be an object")
            continue
        evidence_id = row.get("id")
        if not isinstance(evidence_id, str) or not EVIDENCE_ID.match(evidence_id):
            errors.append(f"{owner} has invalid id")
        elif evidence_id in ids:
            errors.append(f"duplicate evidence id {evidence_id}")
        else:
            ids.add(evidence_id)
        if not nonempty(row.get("claim_input")):
            errors.append(f"{owner} requires claim_input")
        state = row.get("epistemic_state")
        if state not in EPISTEMIC_STATES:
            errors.append(f"{owner} has invalid epistemic_state")
        if row.get("confidence") not in CONFIDENCE:
            errors.append(f"{owner} has invalid confidence")
        if not isinstance(row.get("load_bearing"), bool):
            errors.append(f"{owner} load_bearing must be boolean")
        if not isinstance(row.get("fatal_gate_related", False), bool):
            errors.append(f"{owner} fatal_gate_related must be boolean")
        if not isinstance(row.get("used_by"), list):
            errors.append(f"{owner} used_by must be a list")
        if not isinstance(row.get("contradictions"), list):
            errors.append(f"{owner} contradictions must be a list")
        if state == "NOT_KNOWABLE_FROM_DESK_RESEARCH" and not nonempty(row.get("validation_next_step")):
            errors.append(f"{owner} NOT_KNOWABLE_FROM_DESK_RESEARCH requires validation_next_step")
        if state in {"OBSERVED", "ESTIMATED", "BOUNDED"} and row.get("load_bearing") is True:
            if state == "OBSERVED" and not nonempty(row.get("source")):
                errors.append(f"{owner} load-bearing OBSERVED evidence requires a source")
    return ids


def check_evidence_refs(values: Any, known: set[str], owner: str, errors: list[str]) -> None:
    if not isinstance(values, list):
        errors.append(f"{owner} must be a list")
        return
    for value in values:
        if value not in known:
            errors.append(f"{owner} references unknown evidence id {value!r}")


def validate_state(data: Any, inputs: dict[str, Any], ledger: dict[str, Any], evidence_ids: set[str], errors: list[str]) -> None:
    if not isinstance(data, dict):
        errors.append("research-state.json must contain an object")
        return
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append("research-state.json schema_version must be 0.1.0")
    if data.get("phase") not in PHASES:
        errors.append("research-state.json has invalid phase")
    if data.get("status") not in {"ACTIVE", "BLOCKED", "COMPLETE"}:
        errors.append("research-state.json has invalid status")

    context = data.get("decision_context")
    if context not in CONTEXT_PROFILES:
        errors.append("research-state.json has invalid decision_context")
    else:
        if data.get("context_profile") != CONTEXT_PROFILES[context]:
            errors.append("context blindness: context_profile does not match decision_context evidence standard")
        if inputs.get("decision_context") != context:
            errors.append("input and research-state decision_context disagree")

    market = data.get("market_definition")
    if not isinstance(market, dict):
        errors.append("market_definition must be an object")
        market = {}
    elif market.get("status") not in {"UNSET", "PROVISIONAL", "DEFINED"}:
        errors.append("market_definition has invalid status")

    cruxes = data.get("cruxes")
    if not isinstance(cruxes, list):
        errors.append("cruxes must be a list")
        cruxes = []
    if len(cruxes) > 3:
        errors.append("crux-first contract allows at most 3 active cruxes")
    crux_ids: set[str] = set()
    for i, row in enumerate(cruxes):
        if not isinstance(row, dict):
            errors.append(f"cruxes[{i}] must be an object")
            continue
        cid = row.get("id")
        if not isinstance(cid, str) or not CRUX_ID.match(cid) or cid in crux_ids:
            errors.append(f"cruxes[{i}] has invalid/duplicate id")
        else:
            crux_ids.add(cid)
        if not nonempty(row.get("claim")):
            errors.append(f"cruxes[{i}] requires claim")
        check_evidence_refs(row.get("evidence_ids", []), evidence_ids, f"cruxes[{i}].evidence_ids", errors)
        if row.get("support_status") == "NOT_KNOWABLE_FROM_DESK_RESEARCH" and not nonempty(row.get("cheapest_test")):
            errors.append(f"cruxes[{i}] unknown crux requires cheapest_test")

    gates = data.get("fatal_gates")
    if not isinstance(gates, list):
        errors.append("fatal_gates must be a list")
        gates = []
    gate_ids: set[str] = set()
    failed_gates = []
    for i, row in enumerate(gates):
        if not isinstance(row, dict):
            errors.append(f"fatal_gates[{i}] must be an object")
            continue
        gid = row.get("id")
        if not isinstance(gid, str) or not GATE_ID.match(gid) or gid in gate_ids:
            errors.append(f"fatal_gates[{i}] has invalid/duplicate id")
        else:
            gate_ids.add(gid)
        check_evidence_refs(row.get("evidence_ids", []), evidence_ids, f"fatal_gates[{i}].evidence_ids", errors)
        if row.get("status") == "FAIL":
            failed_gates.append(row)

    if failed_gates and data.get("phase") not in {"SYNTHESIZE", "COMPLETE"}:
        unexcused = [g for g in failed_gates if not nonempty(g.get("continue_reason"))]
        if unexcused:
            errors.append("fatal-gate burial: failed fatal gate requires synthesis/stop or an explicit evidence-changing continue_reason")

    gap = data.get("gap", {})
    demand = data.get("demand", {})
    if isinstance(gap, dict):
        check_evidence_refs(gap.get("evidence_ids", []), evidence_ids, "gap.evidence_ids", errors)
    if isinstance(demand, dict):
        check_evidence_refs(demand.get("evidence_ids", []), evidence_ids, "demand.evidence_ids", errors)
        if demand.get("economic_demand_demonstrated") is True and demand.get("highest_tier") in {"E", "F", None}:
            errors.append("attention/stated preference cannot by itself establish economic demand")

    sizing = data.get("sizing")
    if not isinstance(sizing, dict):
        errors.append("sizing must be an object")
        sizing = {}
    pools = sizing.get("pools", {}) if isinstance(sizing, dict) else {}
    if market.get("category_creation") is True and isinstance(pools, dict) and pools.get("collapsed") is True:
        errors.append("category-creation collapse: spend, revenue, and value pools must remain separate")

    tam = sizing.get("tam", {}) if isinstance(sizing, dict) else {}
    if isinstance(tam, dict) and tam.get("status") in {"QUANTIFIED", "BOUNDED"}:
        if tam.get("method") != "BOTTOM_UP":
            errors.append("analyst-TAM dependence: primary quantified TAM must be built bottom-up")
        if not nonempty(tam.get("formula")):
            errors.append("quantified/bounded TAM requires an inspectable bottom-up formula")
        check_evidence_refs(tam.get("input_evidence_ids", []), evidence_ids, "sizing.tam.input_evidence_ids", errors)
        if not sizing.get("cross_checks"):
            errors.append("decision-relevant TAM requires at least one independent sizing cross-check")

    sam = sizing.get("sam", {}) if isinstance(sizing, dict) else {}
    if isinstance(sam, dict) and sam.get("status") in {"QUANTIFIED", "BOUNDED"}:
        check_evidence_refs(sam.get("input_evidence_ids", []), evidence_ids, "sizing.sam.input_evidence_ids", errors)

    reach = data.get("reachability")
    if not isinstance(reach, dict):
        errors.append("reachability must be an object")
        reach = {}
    if reach.get("arbitrary_share_of_tam_or_sam") is True:
        errors.append("arbitrary SOM is prohibited; build reachability from acquisition/adoption mechanics")
    if reach.get("som_estimation") in {"QUANTIFIED", "BOUNDED"}:
        if not nonempty(reach.get("model_structure")):
            errors.append("quantified/bounded SOM requires explicit model_structure")
        parameters = reach.get("parameters")
        if not isinstance(parameters, list) or not parameters:
            errors.append("quantified/bounded SOM requires supported parameters")
        else:
            for i, parameter in enumerate(parameters):
                if not isinstance(parameter, dict):
                    errors.append(f"reachability.parameters[{i}] must be an object")
                    continue
                state = parameter.get("epistemic_state")
                if state not in {"OBSERVED", "ESTIMATED", "BOUNDED"}:
                    errors.append(f"reachability.parameters[{i}] is not supported enough for quantified SOM")
                evidence_id = parameter.get("evidence_id")
                if evidence_id not in evidence_ids:
                    errors.append(f"reachability.parameters[{i}] requires a valid evidence_id")
    if reach.get("som_estimation") == "NOT_ESTIMABLE" and not nonempty(reach.get("model_structure")):
        errors.append("NOT_ESTIMABLE SOM should still state the model structure to be identified")

    modules = data.get("conditional_modules")
    if not isinstance(modules, dict):
        errors.append("conditional_modules must be an object")
        modules = {}

    unit = modules.get("unit_economics", {}) if isinstance(modules, dict) else {}
    metrics = unit.get("metrics", {}) if isinstance(unit, dict) else {}
    if isinstance(metrics, dict):
        cac = metrics.get("cac")
        if isinstance(cac, dict) and cac.get("epistemic_state") in {"OBSERVED", "ESTIMATED", "BOUNDED"}:
            evidence = cac.get("evidence_ids", [])
            if not isinstance(evidence, list) or not evidence or any(e not in evidence_ids for e in evidence):
                errors.append("fake CAC: grounded CAC requires valid supporting evidence ids")

    growth = modules.get("growth", {}) if isinstance(modules, dict) else {}
    cagr = growth.get("cagr") if isinstance(growth, dict) else None
    if cagr is not None:
        if not isinstance(cagr, dict):
            errors.append("growth.cagr must be an object")
        else:
            required = ["start_year", "end_year", "start_value", "end_value", "geography", "market_definition", "currency", "real_or_nominal"]
            missing = [field for field in required if cagr.get(field) in {None, ""}]
            if missing:
                errors.append("CAGR ambiguity: missing " + ", ".join(missing))
            if cagr.get("real_or_nominal") == "REAL" and cagr.get("base_year") in {None, ""}:
                errors.append("CAGR ambiguity: real CAGR requires inflation/base_year metadata")

    falsification = data.get("falsification")
    if not isinstance(falsification, dict):
        errors.append("falsification must be an object")
        falsification = {}
    if falsification.get("status") == "COMPLETE":
        queries = falsification.get("queries")
        if not isinstance(queries, list) or not any(isinstance(q, dict) and q.get("inverted") is True for q in queries):
            errors.append("confirmation-only search: completed falsification requires at least one inverted query")
        check_evidence_refs(falsification.get("evidence_ids", []), evidence_ids, "falsification.evidence_ids", errors)

    verdict = data.get("verdict")
    if not isinstance(verdict, dict):
        errors.append("verdict must be an object")
        verdict = {}
    if verdict.get("status") in {"DRAFT", "FINAL"} and falsification.get("status") != "COMPLETE":
        errors.append("verdict cannot be drafted/finalized before falsification is complete")
    if verdict.get("status") == "FINAL" and verdict.get("recommendation") not in {"PURSUE", "TEST", "HOLD", "REJECT"}:
        errors.append("final verdict requires PURSUE, TEST, HOLD, or REJECT")

    expected_burden = ledger_counts(ledger)
    if data.get("evidence_burden") != expected_burden:
        errors.append(
            "unknown suppression/evidence burden mismatch: research-state evidence_burden must exactly reflect load-bearing ledger states"
        )

    next_test = data.get("next_test")
    if not isinstance(next_test, dict):
        errors.append("next_test must be an object")
    elif next_test.get("status") == "DEFINED":
        for field in ["test", "decision_value", "estimated_cost_time"]:
            if not nonempty(next_test.get(field)):
                errors.append(f"defined next_test requires {field}")


def validate_workspace(root: Path) -> list[str]:
    errors: list[str] = []
    required = ["input.json", "research-state.json", "evidence-ledger.json"]
    for name in required:
        if not (root / name).is_file():
            errors.append(f"missing required file {name}")
    if errors:
        return errors

    try:
        inputs = read_json(root / "input.json")
        state = read_json(root / "research-state.json")
        ledger = read_json(root / "evidence-ledger.json")
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read workspace JSON: {exc}"]

    validate_input(inputs, errors)
    evidence_ids = validate_ledger(ledger, errors)
    validate_state(state, inputs if isinstance(inputs, dict) else {}, ledger if isinstance(ledger, dict) else {}, evidence_ids, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace")
    args = parser.parse_args()
    errors = validate_workspace(Path(args.workspace))
    if errors:
        print("Validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Validation PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
