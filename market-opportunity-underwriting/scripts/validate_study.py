#!/usr/bin/env python3
"""Validate structural and hard methodological contracts for an underwriting study."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any

from _common import (
    CONFIDENCE,
    CONTEXT_PROFILES,
    DEMAND_DIMENSIONS,
    EPISTEMIC_STATES,
    PHASES,
    SCHEMA_VERSION,
    SCRUTINY_PROFILES,
    ledger_counts,
    read_json,
)
from calculate_study import calculate

EVIDENCE_ID = re.compile(r"^E[0-9]{3,}$")
CRUX_ID = re.compile(r"^C[0-9]{2,}$")
GATE_ID = re.compile(r"^F[0-9]{2,}$")
SEARCH_PLAN_ID = re.compile(r"^SP[0-9]{3,}$")
SEARCH_ID = re.compile(r"^S[0-9]{3,}$")
QUEUE_ID = re.compile(r"^RQ[0-9]{3,}$")
CALC_ID = re.compile(r"^CALC[0-9]{3,}$")


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_input(data: Any, errors: list[str]) -> None:
    if not isinstance(data, dict):
        errors.append("input.json must contain an object")
        return
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"input.json schema_version must be {SCHEMA_VERSION}")
    for field in ["idea", "target_customer", "problem_job", "geography", "decision"]:
        if not nonempty(data.get(field)):
            errors.append(f"input.json requires non-empty {field}")
    if data.get("decision_context") not in CONTEXT_PROFILES:
        errors.append("input.json has invalid decision_context")
    if data.get("scrutiny_profile") not in SCRUTINY_PROFILES:
        errors.append("input.json has invalid scrutiny_profile")
    if not isinstance(data.get("time_horizon_years"), int) or data["time_horizon_years"] <= 0:
        errors.append("input.json requires positive time_horizon_years")
    provenance = data.get("input_provenance")
    if not isinstance(provenance, dict):
        errors.append("input.json requires input_provenance object")
    else:
        for field in ["idea", "target_customer", "problem_job", "geography", "decision", "decision_context", "scrutiny_profile"]:
            if provenance.get(field) not in {"USER_SUPPLIED", "EXPLICITLY_PROVISIONAL"}:
                errors.append(f"input.json provenance missing/invalid for {field}")


def validate_ledger(data: Any, errors: list[str]) -> tuple[set[str], dict[str, dict[str, Any]]]:
    ids: set[str] = set()
    by_id: dict[str, dict[str, Any]] = {}
    if not isinstance(data, dict):
        errors.append("evidence-ledger.json must contain an object")
        return ids, by_id
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"evidence-ledger.json schema_version must be {SCHEMA_VERSION}")
    entries = data.get("entries")
    if not isinstance(entries, list):
        errors.append("evidence-ledger.json entries must be a list")
        return ids, by_id

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
            by_id[evidence_id] = row
        if not nonempty(row.get("claim_input")):
            errors.append(f"{owner} requires claim_input")
        state = row.get("epistemic_state")
        if state not in EPISTEMIC_STATES:
            errors.append(f"{owner} has invalid epistemic_state")
        if row.get("confidence") not in CONFIDENCE:
            errors.append(f"{owner} has invalid confidence")
        if not isinstance(row.get("load_bearing"), bool):
            errors.append(f"{owner} load_bearing must be boolean")
        if not isinstance(row.get("fatal_gate_related"), bool):
            errors.append(f"{owner} fatal_gate_related must be boolean")
        if row.get("demand_tier") not in {"A", "B", "C", "D", "E", "F", None}:
            errors.append(f"{owner} has invalid demand_tier")
        if not isinstance(row.get("source_lineage_ids"), list):
            errors.append(f"{owner} source_lineage_ids must be a list")
        if not isinstance(row.get("used_by"), list):
            errors.append(f"{owner} used_by must be a list")
        if not isinstance(row.get("contradictions"), list):
            errors.append(f"{owner} contradictions must be a list")
        if row.get("claim_temporality") not in {"CURRENT_PRODUCT_STATE", "TIME_SERIES", "HISTORICAL", "STRUCTURAL"}:
            errors.append(f"{owner} has invalid claim_temporality")
        if row.get("source_directness") not in {"PRIMARY", "SECONDARY", "COMMUNITY", "UNKNOWN"}:
            errors.append(f"{owner} has invalid source_directness")
        if not isinstance(row.get("contradiction_evidence_ids"), list):
            errors.append(f"{owner} contradiction_evidence_ids must be a list")
        if row.get("conflict_resolution") not in {"NONE", "PRIMARY_OVERRIDES", "SECONDARY_RETAINED_WITH_REASON", "UNRESOLVED"}:
            errors.append(f"{owner} has invalid conflict_resolution")
        if state == "NOT_KNOWABLE_FROM_DESK_RESEARCH" and not nonempty(row.get("validation_next_step")):
            errors.append(f"{owner} NOT_KNOWABLE_FROM_DESK_RESEARCH requires validation_next_step")

        if state == "OBSERVED" and row.get("load_bearing") is True:
            for field in ["source", "source_id", "lineage_id", "accessed_at", "effective_period"]:
                if not nonempty(row.get(field)):
                    errors.append(f"{owner} load-bearing OBSERVED evidence requires {field}")
            lineages = row.get("source_lineage_ids", [])
            if nonempty(row.get("lineage_id")) and row.get("lineage_id") not in lineages:
                errors.append(f"{owner} source_lineage_ids must include lineage_id")

        if state in {"ESTIMATED", "BOUNDED"} and row.get("load_bearing") is True:
            if not row.get("source_lineage_ids") and not nonempty(row.get("validation_next_step")):
                errors.append(f"{owner} load-bearing {state} evidence requires source lineage(s) or a validation next step")

        if row.get("load_bearing") is True and row.get("claim_temporality") == "CURRENT_PRODUCT_STATE":
            if not nonempty(row.get("freshness_checked_at")):
                errors.append(f"{owner} load-bearing CURRENT_PRODUCT_STATE evidence requires freshness_checked_at")
            if row.get("source_directness") != "PRIMARY" and not nonempty(row.get("primary_source_unavailable_reason")):
                # A contradictory primary source is handled in the second pass below. Until then,
                # non-primary current-state evidence must explain why first-party evidence was unavailable.
                contradiction_ids = row.get("contradiction_evidence_ids", [])
                if not contradiction_ids:
                    errors.append(
                        f"{owner} non-primary CURRENT_PRODUCT_STATE evidence requires primary_source_unavailable_reason"
                    )

    # Current-state precedence is evaluated after all evidence IDs are known so contradictions
    # can point forward or backward in the ledger.
    for evidence_id, row in by_id.items():
        owner = f"evidence-ledger {evidence_id}"
        refs = row.get("contradiction_evidence_ids", [])
        if not isinstance(refs, list):
            continue
        for ref in refs:
            if ref not in by_id:
                errors.append(f"{owner} references unknown contradiction evidence id {ref!r}")

        if row.get("claim_temporality") != "CURRENT_PRODUCT_STATE" or row.get("source_directness") == "PRIMARY":
            continue

        opposing_ids = set(ref for ref in refs if ref in by_id)
        opposing_ids.update(
            other_id
            for other_id, other in by_id.items()
            if evidence_id in other.get("contradiction_evidence_ids", [])
        )
        primary_conflicts = [
            other_id
            for other_id in opposing_ids
            if by_id[other_id].get("claim_temporality") == "CURRENT_PRODUCT_STATE"
            and by_id[other_id].get("source_directness") == "PRIMARY"
        ]

        if primary_conflicts:
            resolution = row.get("conflict_resolution")
            if resolution == "NONE":
                errors.append(
                    f"{owner} stale-current-state corroboration: contradictory primary current-state evidence requires conflict_resolution"
                )
            if not nonempty(row.get("conflict_adjudication")):
                errors.append(
                    f"{owner} stale-current-state corroboration: contradictory primary current-state evidence requires conflict_adjudication"
                )
            if row.get("load_bearing") is True and resolution in {"PRIMARY_OVERRIDES", "UNRESOLVED", "NONE"}:
                errors.append(
                    f"{owner} stale-current-state corroboration: non-primary evidence cannot remain load-bearing when current primary evidence overrides or leaves the conflict unresolved"
                )
            if row.get("load_bearing") is True and resolution == "SECONDARY_RETAINED_WITH_REASON":
                if not nonempty(row.get("primary_source_unavailable_reason")):
                    errors.append(
                        f"{owner} retained secondary current-state evidence requires an explicit primary_source_unavailable_reason/exception rationale"
                    )
        elif row.get("load_bearing") is True and not nonempty(row.get("primary_source_unavailable_reason")):
            errors.append(
                f"{owner} non-primary CURRENT_PRODUCT_STATE evidence requires primary_source_unavailable_reason"
            )

    return ids, by_id


def check_evidence_refs(values: Any, known: set[str], owner: str, errors: list[str]) -> None:
    if not isinstance(values, list):
        errors.append(f"{owner} must be a list")
        return
    for value in values:
        if value not in known:
            errors.append(f"{owner} references unknown evidence id {value!r}")


def lineages_for(evidence_ids: list[str], ledger_by_id: dict[str, dict[str, Any]]) -> set[str]:
    result: set[str] = set()
    for evidence_id in evidence_ids:
        row = ledger_by_id.get(evidence_id, {})
        for lineage in row.get("source_lineage_ids", []) if isinstance(row, dict) else []:
            if isinstance(lineage, str) and lineage:
                result.add(lineage)
        lineage = row.get("lineage_id") if isinstance(row, dict) else None
        if isinstance(lineage, str) and lineage:
            result.add(lineage)
    return result


def validate_search_plan(data: Any, crux_ids: set[str], errors: list[str]) -> set[str]:
    ids: set[str] = set()
    if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"search-plan.json schema_version must be {SCHEMA_VERSION}")
        return ids
    entries = data.get("entries")
    if not isinstance(entries, list):
        errors.append("search-plan.json entries must be a list")
        return ids
    for i, row in enumerate(entries):
        owner = f"search-plan entries[{i}]"
        if not isinstance(row, dict):
            errors.append(f"{owner} must be an object")
            continue
        sid = row.get("id")
        if not isinstance(sid, str) or not SEARCH_PLAN_ID.match(sid) or sid in ids:
            errors.append(f"{owner} has invalid/duplicate id")
        else:
            ids.add(sid)
        if row.get("crux_id") not in crux_ids:
            errors.append(f"{owner} references unknown crux_id")
        for field in ["question", "support_observation", "refutation_observation", "stop_condition"]:
            if not nonempty(row.get(field)):
                errors.append(f"{owner} requires {field}")
        if not isinstance(row.get("preferred_source_classes"), list) or not row["preferred_source_classes"]:
            errors.append(f"{owner} requires preferred_source_classes")
        if not isinstance(row.get("concepts"), list) or not row["concepts"]:
            errors.append(f"{owner} requires concept/synonym families")
        queries = row.get("queries")
        if not isinstance(queries, list) or not queries:
            errors.append(f"{owner} requires queries")
    return ids


def validate_search_log(
    data: Any,
    plan_ids: set[str],
    crux_ids: set[str],
    evidence_ids: set[str],
    errors: list[str],
) -> tuple[set[str], dict[str, dict[str, Any]]]:
    ids: set[str] = set()
    by_id: dict[str, dict[str, Any]] = {}
    if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"search-log.json schema_version must be {SCHEMA_VERSION}")
        return ids, by_id
    entries = data.get("entries")
    if not isinstance(entries, list):
        errors.append("search-log.json entries must be a list")
        return ids, by_id
    for i, row in enumerate(entries):
        owner = f"search-log entries[{i}]"
        if not isinstance(row, dict):
            errors.append(f"{owner} must be an object")
            continue
        sid = row.get("id")
        if not isinstance(sid, str) or not SEARCH_ID.match(sid) or sid in ids:
            errors.append(f"{owner} has invalid/duplicate id")
        else:
            ids.add(sid)
            by_id[sid] = row
        if row.get("search_plan_id") not in plan_ids:
            errors.append(f"{owner} references unknown search_plan_id")
        if row.get("crux_id") not in crux_ids:
            errors.append(f"{owner} references unknown crux_id")
        if row.get("polarity") not in {"CONFIRMATORY", "ADVERSARIAL", "NEUTRAL"}:
            errors.append(f"{owner} has invalid polarity")
        for field in ["query", "searched_at", "route", "source_class"]:
            if not nonempty(row.get(field)):
                errors.append(f"{owner} requires {field}")
        check_evidence_refs(row.get("evidence_ids", []), evidence_ids, f"{owner}.evidence_ids", errors)
    return ids, by_id


def validate_calculations(
    data: Any,
    ledger_by_id: dict[str, dict[str, Any]],
    evidence_ids: set[str],
    errors: list[str],
) -> tuple[set[str], dict[str, dict[str, Any]]]:
    ids: set[str] = set()
    by_id: dict[str, dict[str, Any]] = {}
    if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"calculations.json schema_version must be {SCHEMA_VERSION}")
        return ids, by_id
    entries = data.get("entries")
    if not isinstance(entries, list):
        errors.append("calculations.json entries must be a list")
        return ids, by_id
    for i, row in enumerate(entries):
        owner = f"calculations entries[{i}]"
        if not isinstance(row, dict):
            errors.append(f"{owner} must be an object")
            continue
        cid = row.get("id")
        if not isinstance(cid, str) or not CALC_ID.match(cid) or cid in ids:
            errors.append(f"{owner} has invalid/duplicate id")
            continue
        ids.add(cid)
        by_id[cid] = row
        inputs = row.get("input_evidence_ids", [])
        check_evidence_refs(inputs, evidence_ids, f"{owner}.input_evidence_ids", errors)
        if not inputs:
            errors.append(f"{owner} requires input evidence")
            continue
        try:
            expected = calculate(row, ledger_by_id)
        except (ValueError, TypeError, ZeroDivisionError) as exc:
            errors.append(f"{owner} cannot be deterministically calculated: {exc}")
            continue
        expected_output = expected.get("output", {})
        actual_output = row.get("output", {})
        for field in ["value", "low", "high"]:
            a = actual_output.get(field) if isinstance(actual_output, dict) else None
            b = expected_output.get(field)
            if a is None or b is None or not math.isclose(float(a), float(b), rel_tol=1e-9, abs_tol=1e-9):
                errors.append(f"prose-math drift: {cid} output.{field} is stale or not reproducible")
                break
    return ids, by_id


def validate_state(
    data: Any,
    inputs: dict[str, Any],
    ledger: dict[str, Any],
    ledger_by_id: dict[str, dict[str, Any]],
    evidence_ids: set[str],
    search_plan: dict[str, Any],
    search_log: dict[str, Any],
    calculations: dict[str, Any],
    errors: list[str],
) -> None:
    if not isinstance(data, dict):
        errors.append("research-state.json must contain an object")
        return
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"research-state.json schema_version must be {SCHEMA_VERSION}")
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

    scrutiny = data.get("scrutiny_profile")
    scrutiny_name = scrutiny.get("name") if isinstance(scrutiny, dict) else None
    if scrutiny_name not in SCRUTINY_PROFILES:
        errors.append("research-state.json has invalid scrutiny_profile")
    else:
        expected = SCRUTINY_PROFILES[scrutiny_name]
        if scrutiny.get("focus") != expected["focus"] or scrutiny.get("adjacent_diligence") != expected["adjacent_diligence"]:
            errors.append("scrutiny-profile drift: stage-specific institutional review contract changed")
        if inputs.get("scrutiny_profile") != scrutiny_name:
            errors.append("input and research-state scrutiny_profile disagree")

    scrutiny_checks = data.get("scrutiny_checks")
    if not isinstance(scrutiny_checks, list):
        errors.append("scrutiny_checks must be a list")
        scrutiny_checks = []
    expected_check_keys = set(SCRUTINY_PROFILES.get(scrutiny_name, {}).get("required_checks", []))
    actual_check_keys: set[str] = set()
    for i, row in enumerate(scrutiny_checks):
        if not isinstance(row, dict):
            errors.append(f"scrutiny_checks[{i}] must be an object")
            continue
        key = row.get("key")
        if not isinstance(key, str) or not key or key in actual_check_keys:
            errors.append(f"scrutiny_checks[{i}] has invalid/duplicate key")
        else:
            actual_check_keys.add(key)
        if row.get("status") not in {"UNASSESSED", "EVIDENCED", "UNKNOWN", "NOT_APPLICABLE", "OUTSIDE_SCOPE"}:
            errors.append(f"scrutiny_checks[{i}] has invalid status")
        check_evidence_refs(row.get("evidence_ids", []), evidence_ids, f"scrutiny_checks[{i}].evidence_ids", errors)
        if row.get("status") != "UNASSESSED" and not nonempty(row.get("reasoning")):
            errors.append(f"scrutiny_checks[{i}] assessed status requires reasoning")
    if actual_check_keys != expected_check_keys:
        errors.append("scrutiny coverage drift: required institutional review checks do not match scrutiny profile")

    hurdle = data.get("decision_hurdle")
    if not isinstance(hurdle, dict) or hurdle.get("status") not in {"PROVISIONAL", "DEFINED"}:
        errors.append("decision hurdle must be PROVISIONAL or DEFINED")
    elif not nonempty(hurdle.get("required_outcome")):
        errors.append("decision hurdle requires a stated economic outcome")

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
    crux_by_id: dict[str, dict[str, Any]] = {}
    for i, row in enumerate(cruxes):
        if not isinstance(row, dict):
            errors.append(f"cruxes[{i}] must be an object")
            continue
        cid = row.get("id")
        if not isinstance(cid, str) or not CRUX_ID.match(cid) or cid in crux_ids:
            errors.append(f"cruxes[{i}] has invalid/duplicate id")
        else:
            crux_ids.add(cid)
            crux_by_id[cid] = row
        if not nonempty(row.get("claim")):
            errors.append(f"cruxes[{i}] requires claim")
        check_evidence_refs(row.get("evidence_ids", []), evidence_ids, f"cruxes[{i}].evidence_ids", errors)
        if row.get("support_status") == "NOT_KNOWABLE_FROM_DESK_RESEARCH" and not nonempty(row.get("cheapest_test")):
            errors.append(f"cruxes[{i}] unknown crux requires highest-value next evidence/test")

    queue = data.get("research_queue")
    if not isinstance(queue, list):
        errors.append("research_queue must be a list")
        queue = []
    queue_ids: set[str] = set()
    for i, row in enumerate(queue):
        if not isinstance(row, dict):
            errors.append(f"research_queue[{i}] must be an object")
            continue
        qid = row.get("id")
        if not isinstance(qid, str) or not QUEUE_ID.match(qid) or qid in queue_ids:
            errors.append(f"research_queue[{i}] has invalid/duplicate id")
        else:
            queue_ids.add(qid)
        if row.get("crux_id") not in crux_ids:
            errors.append(f"research_queue[{i}] references unknown crux_id")
        for field, allowed in {
            "decision_impact": {"FATAL", "HIGH", "MEDIUM", "LOW"},
            "uncertainty": {"HIGH", "MEDIUM", "LOW"},
            "expected_decision_change": {"YES", "UNCLEAR", "NO"},
            "evidence_tractability": {"HIGH", "MEDIUM", "LOW"},
            "cost_time": {"LOW", "MEDIUM", "HIGH"},
            "status": {"OPEN", "IN_PROGRESS", "RESOLVED", "DEFERRED"},
        }.items():
            if row.get(field) not in allowed:
                errors.append(f"research_queue[{i}] has invalid {field}")

    plan_ids = validate_search_plan(search_plan, crux_ids, errors)
    search_ids, search_by_id = validate_search_log(search_log, plan_ids, crux_ids, evidence_ids, errors)

    for i, row in enumerate(queue):
        if isinstance(row, dict):
            for plan_id in row.get("search_plan_ids", []):
                if plan_id not in plan_ids:
                    errors.append(f"research_queue[{i}] references unknown search plan {plan_id}")

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
        dimensions = demand.get("dimensions")
        if not isinstance(dimensions, dict):
            errors.append("demand dimensions are required; economic burden, budget, WTP, and adoption cannot be collapsed")
            dimensions = {}
        for name in DEMAND_DIMENSIONS:
            row = dimensions.get(name)
            if not isinstance(row, dict):
                errors.append(f"demand dimension missing: {name}")
                continue
            if row.get("status") not in {"STRONG", "MODERATE", "WEAK", "UNKNOWN", "NOT_APPLICABLE"}:
                errors.append(f"demand dimension {name} has invalid status")
            check_evidence_refs(row.get("evidence_ids", []), evidence_ids, f"demand.dimensions.{name}.evidence_ids", errors)
        if demand.get("economic_demand_demonstrated") is True:
            if demand.get("highest_tier") in {"E", "F", None}:
                errors.append("attention/stated preference cannot by itself establish economic demand")
            burden = dimensions.get("problem_economic_burden", {}).get("status")
            wtp = dimensions.get("solution_wtp", {}).get("status")
            if burden not in {"STRONG", "MODERATE"} or wtp not in {"STRONG", "MODERATE"}:
                errors.append("demand-dimension conflation: economic burden and solution WTP must both be supported before market demand is demonstrated")

    candidates = market.get("candidate_definitions", []) if isinstance(market, dict) else []
    if isinstance(candidates, list) and len(candidates) > 1 and data.get("verdict", {}).get("status") == "FINAL":
        if market.get("robustness_across_definitions") not in {"ROBUST", "SENSITIVE"}:
            errors.append("structural uncertainty: final verdict must assess robustness across plausible market definitions")
        if not nonempty(market.get("selection_rationale")) or not nonempty(market.get("robustness_notes")):
            errors.append("structural uncertainty: final verdict requires market-definition selection and robustness rationale")

    sizing = data.get("sizing")
    if not isinstance(sizing, dict):
        errors.append("sizing must be an object")
        sizing = {}
    pools = sizing.get("pools", {}) if isinstance(sizing, dict) else {}
    if market.get("category_creation") is True and isinstance(pools, dict) and pools.get("collapsed") is True:
        errors.append("category-creation collapse: spend, revenue, and value pools must remain separate")

    calc_ids, calc_by_id = validate_calculations(calculations, ledger_by_id, evidence_ids, errors)

    tam = sizing.get("tam", {}) if isinstance(sizing, dict) else {}
    tam_lineages: set[str] = set()
    if isinstance(tam, dict) and tam.get("status") in {"QUANTIFIED", "BOUNDED"}:
        if tam.get("method") != "BOTTOM_UP":
            errors.append("analyst-TAM dependence: primary quantified TAM must be built bottom-up")
        if not nonempty(tam.get("formula")):
            errors.append("quantified/bounded TAM requires an inspectable bottom-up formula")
        tam_inputs = tam.get("input_evidence_ids", [])
        check_evidence_refs(tam_inputs, evidence_ids, "sizing.tam.input_evidence_ids", errors)
        tam_lineages = lineages_for(tam_inputs if isinstance(tam_inputs, list) else [], ledger_by_id)
        calculation_id = tam.get("calculation_id")
        if calculation_id not in calc_ids:
            errors.append("quantified/bounded TAM requires a deterministic calculation_id")
        else:
            output = calc_by_id[calculation_id].get("output", {})
            for state_field, calc_field in [("value", "value"), ("low", "low"), ("high", "high")]:
                state_value = tam.get(state_field)
                calc_value = output.get(calc_field) if isinstance(output, dict) else None
                if state_value is not None and calc_value is not None and not math.isclose(float(state_value), float(calc_value), rel_tol=1e-9, abs_tol=1e-9):
                    errors.append("prose-math drift: TAM narrative/state does not match deterministic calculation")
                    break

        cross_checks = sizing.get("cross_checks")
        if not isinstance(cross_checks, list) or not cross_checks:
            errors.append("decision-relevant TAM requires at least one independent sizing cross-check")
        else:
            independent_found = False
            for i, check in enumerate(cross_checks):
                if not isinstance(check, dict):
                    errors.append(f"sizing.cross_checks[{i}] must be an object")
                    continue
                check_inputs = check.get("input_evidence_ids", [])
                check_evidence_refs(check_inputs, evidence_ids, f"sizing.cross_checks[{i}].input_evidence_ids", errors)
                check_lineages = lineages_for(check_inputs if isinstance(check_inputs, list) else [], ledger_by_id)
                method_different = check.get("method") not in {None, "BOTTOM_UP"}
                lineage_independent = bool(check_lineages - tam_lineages) if tam_lineages else bool(check_lineages)
                override = nonempty(check.get("independence_override_reason"))
                if method_different and (lineage_independent or override):
                    independent_found = True
            if not independent_found:
                errors.append("false corroboration: sizing cross-check must use an independent method plus distinct evidence lineage or explicit independence rationale")

    sam = sizing.get("sam", {}) if isinstance(sizing, dict) else {}
    if isinstance(sam, dict) and sam.get("status") in {"QUANTIFIED", "BOUNDED"}:
        check_evidence_refs(sam.get("input_evidence_ids", []), evidence_ids, "sizing.sam.input_evidence_ids", errors)
        if sam.get("calculation_id") not in calc_ids:
            errors.append("quantified/bounded SAM requires a deterministic calculation_id")

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

    reference = modules.get("reference_class", {}) if isinstance(modules, dict) else {}
    verdict = data.get("verdict")
    if not isinstance(verdict, dict):
        errors.append("verdict must be an object")
        verdict = {}
    if verdict.get("status") == "FINAL" and not (isinstance(reference, dict) and reference.get("considered") is True):
        errors.append("reference-class omission: every final study must consider whether a defensible outside-view reference class exists")

    falsification = data.get("falsification")
    if not isinstance(falsification, dict):
        errors.append("falsification must be an object")
        falsification = {}
    if falsification.get("status") == "COMPLETE":
        coverage = falsification.get("coverage")
        if not isinstance(coverage, list):
            errors.append("falsification coverage must be a list")
            coverage = []
        coverage_by_crux = {row.get("crux_id"): row for row in coverage if isinstance(row, dict)}
        for cid, crux in crux_by_id.items():
            if crux.get("importance") not in {"FATAL", "HIGH"}:
                continue
            row = coverage_by_crux.get(cid)
            if not isinstance(row, dict):
                errors.append(f"falsification coverage missing for {cid}")
                continue
            search_refs = row.get("adversarial_search_ids", [])
            if not isinstance(search_refs, list) or not search_refs:
                errors.append(f"confirmation-only search: {cid} requires an adversarial search")
            else:
                for search_id in search_refs:
                    search_row = search_by_id.get(search_id)
                    if not search_row or search_row.get("polarity") != "ADVERSARIAL":
                        errors.append(f"confirmation-only search: {cid} adversarial_search_ids must reference logged adversarial searches")
            if not nonempty(row.get("adjudication")):
                errors.append(f"adversarial theater: {cid} contradictory evidence must be adjudicated, not merely listed")
            if "status_changed" not in row or not isinstance(row.get("status_changed"), bool):
                errors.append(f"adversarial theater: {cid} must record whether the crux judgment changed")
        check_evidence_refs(falsification.get("evidence_ids", []), evidence_ids, "falsification.evidence_ids", errors)

    if verdict.get("status") in {"DRAFT", "FINAL"} and falsification.get("status") != "COMPLETE":
        errors.append("verdict cannot be drafted/finalized before falsification is complete")
    if verdict.get("status") == "FINAL" and verdict.get("recommendation") not in {"PURSUE", "TEST", "HOLD", "REJECT"}:
        errors.append("final verdict requires PURSUE, TEST, HOLD, or REJECT")
    if verdict.get("status") == "FINAL" and verdict.get("recommendation") in {"PURSUE", "REJECT"}:
        if not isinstance(hurdle, dict) or hurdle.get("status") != "DEFINED":
            errors.append("hurdle-free verdict: PURSUE/REJECT requires a DEFINED decision hurdle")

    if verdict.get("status") == "FINAL":
        unassessed_checks = [
            row.get("key") for row in scrutiny_checks
            if isinstance(row, dict) and row.get("status") == "UNASSESSED"
        ]
        if unassessed_checks:
            errors.append(
                "institutional scrutiny theater: final verdict leaves required scrutiny checks UNASSESSED: "
                + ", ".join(unassessed_checks)
            )

    if scrutiny_name == "pe-commercial-diligence" and verdict.get("status") == "FINAL":
        if not scrutiny.get("adjacent_diligence"):
            errors.append("PE commercial diligence must disclose adjacent diligence outside this skill's scope")

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
    required = [
        "input.json",
        "research-state.json",
        "evidence-ledger.json",
        "search-plan.json",
        "search-log.json",
        "calculations.json",
    ]
    for name in required:
        if not (root / name).is_file():
            errors.append(f"missing required file {name}")
    if errors:
        return errors

    try:
        inputs = read_json(root / "input.json")
        state = read_json(root / "research-state.json")
        ledger = read_json(root / "evidence-ledger.json")
        search_plan = read_json(root / "search-plan.json")
        search_log = read_json(root / "search-log.json")
        calculations = read_json(root / "calculations.json")
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read workspace JSON: {exc}"]

    validate_input(inputs, errors)
    evidence_ids, ledger_by_id = validate_ledger(ledger, errors)
    validate_state(
        state,
        inputs if isinstance(inputs, dict) else {},
        ledger if isinstance(ledger, dict) else {},
        ledger_by_id,
        evidence_ids,
        search_plan if isinstance(search_plan, dict) else {},
        search_log if isinstance(search_log, dict) else {},
        calculations if isinstance(calculations, dict) else {},
        errors,
    )
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
