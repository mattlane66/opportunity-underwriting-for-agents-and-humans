from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / "market-opportunity-underwriting"
SCRIPTS = SKILL / "scripts"
INIT = SCRIPTS / "init_study.py"
VALIDATE = SCRIPTS / "validate_study.py"
NEXT = SCRIPTS / "next_research_move.py"
RANK = SCRIPTS / "rank_research_queue.py"
CALCULATE = SCRIPTS / "calculate_study.py"
GENERATE = SCRIPTS / "generate_portable_prompt.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=REPO, text=True, capture_output=True, check=False)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def evidence(
    evidence_id: str,
    claim: str,
    value,
    *,
    lineage: str,
    unit: str = "count",
    load_bearing: bool = True,
    demand_tier=None,
):
    return {
        "id": evidence_id,
        "claim_input": claim,
        "value": value,
        "low": None,
        "high": None,
        "unit": unit,
        "epistemic_state": "OBSERVED",
        "source": f"https://example.com/{evidence_id.lower()}",
        "source_id": f"SRC-{evidence_id}",
        "lineage_id": lineage,
        "origin_source_id": f"ORIGIN-{lineage}",
        "source_lineage_ids": [lineage],
        "source_date": "2026-08-01",
        "accessed_at": "2026-08-31",
        "effective_period": "2026",
        "source_type": "test fixture",
        "confidence": "HIGH",
        "load_bearing": load_bearing,
        "fatal_gate_related": False,
        "demand_tier": demand_tier,
        "used_by": [],
        "contradictions": [],
        "validation_next_step": None,
        "notes": None,
    }


class UnderwritingContractTests(unittest.TestCase):
    def new_workspace(self, scrutiny_profile: str = "general") -> tuple[tempfile.TemporaryDirectory[str], Path]:
        td = tempfile.TemporaryDirectory()
        root = Path(td.name) / "study"
        result = run(
            str(INIT),
            "--workspace", str(root),
            "--idea", "Test idea",
            "--customer", "Small businesses",
            "--problem", "Costly manual workflow",
            "--geography", "United States",
            "--decision", "Should we build this?",
            "--context", "napkin-stage",
            "--scrutiny-profile", scrutiny_profile,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return td, root

    def assert_invalid(self, root: Path, expected: str) -> None:
        result = run(str(VALIDATE), str(root))
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(expected, result.stdout + result.stderr)

    def seed_cruxes(self, root: Path) -> None:
        state = load(root / "research-state.json")
        state["cruxes"] = [
            {
                "id": "C01",
                "claim": "The problem is economically consequential.",
                "importance": "FATAL",
                "support_status": "UNTESTED",
                "evidence_ids": [],
                "cheapest_test": "Find direct economic-sacrifice evidence.",
            },
            {
                "id": "C02",
                "claim": "The reachable market can clear the decision hurdle.",
                "importance": "HIGH",
                "support_status": "UNTESTED",
                "evidence_ids": [],
                "cheapest_test": "Build the bottom-up denominator.",
            },
        ]
        save(root / "research-state.json", state)

    def sync_burden(self, root: Path) -> None:
        ledger = load(root / "evidence-ledger.json")
        rows = [r for r in ledger["entries"] if r.get("load_bearing")]
        state = load(root / "research-state.json")
        state["evidence_burden"] = {
            "load_bearing_count": len(rows),
            "assumption_count": sum(r["epistemic_state"] == "ASSUMPTION" for r in rows),
            "not_knowable_count": sum(r["epistemic_state"] == "NOT_KNOWABLE_FROM_DESK_RESEARCH" for r in rows),
            "fatal_gate_assumption": any(
                r.get("fatal_gate_related")
                and r["epistemic_state"] in {"ASSUMPTION", "NOT_KNOWABLE_FROM_DESK_RESEARCH"}
                for r in rows
            ),
        }
        save(root / "research-state.json", state)

    def test_clean_initialized_workspace_validates(self):
        td, root = self.new_workspace()
        self.addCleanup(td.cleanup)
        result = run(str(VALIDATE), str(root))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_initializer_creates_six_state_files(self):
        td, root = self.new_workspace()
        self.addCleanup(td.cleanup)
        for name in [
            "input.json",
            "research-state.json",
            "evidence-ledger.json",
            "search-plan.json",
            "search-log.json",
            "calculations.json",
        ]:
            self.assertTrue((root / name).is_file(), name)

    def test_next_move_is_cruxes_after_classification(self):
        td, root = self.new_workspace()
        self.addCleanup(td.cleanup)
        result = run(str(NEXT), str(root))
        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["next_phase"], "CRUXES")

    def test_rank_research_queue_prioritizes_fatal_uncertainty(self):
        td, root = self.new_workspace()
        self.addCleanup(td.cleanup)
        self.seed_cruxes(root)
        state = load(root / "research-state.json")
        state["research_queue"] = [
            {
                "id": "RQ001", "crux_id": "C02", "question": "Market size?",
                "decision_impact": "HIGH", "uncertainty": "MEDIUM",
                "expected_decision_change": "UNCLEAR", "evidence_tractability": "HIGH",
                "cost_time": "LOW", "proposed_evidence": "Official denominator",
                "status": "OPEN", "search_plan_ids": [], "notes": ""
            },
            {
                "id": "RQ002", "crux_id": "C01", "question": "Does anyone pay?",
                "decision_impact": "FATAL", "uncertainty": "HIGH",
                "expected_decision_change": "YES", "evidence_tractability": "MEDIUM",
                "cost_time": "MEDIUM", "proposed_evidence": "Budget and transaction evidence",
                "status": "OPEN", "search_plan_ids": [], "notes": ""
            }
        ]
        save(root / "research-state.json", state)
        result = run(str(RANK), str(root))
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = json.loads(result.stdout)
        self.assertEqual(rows[0]["id"], "RQ002")
        self.assertEqual(rows[0]["priority_band"], "P0")

    def test_deterministic_product_calculation(self):
        td, root = self.new_workspace()
        self.addCleanup(td.cleanup)
        ledger = load(root / "evidence-ledger.json")
        ledger["entries"] = [
            evidence("E001", "Eligible accounts", 100, lineage="L1"),
            evidence("E002", "Annual revenue/account", 20, lineage="L2", unit="USD/account/year"),
        ]
        save(root / "evidence-ledger.json", ledger)
        calculations = load(root / "calculations.json")
        calculations["entries"] = [{
            "id": "CALC001", "kind": "TAM", "operation": "PRODUCT",
            "input_evidence_ids": ["E001", "E002"], "parameters": {},
            "output": {"value": None, "low": None, "high": None, "unit": "USD/year"},
            "notes": ""
        }]
        save(root / "calculations.json", calculations)
        result = run(str(CALCULATE), str(root))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        output = load(root / "calculations.json")["entries"][0]["output"]
        self.assertEqual(output["value"], 2000.0)
        self.assertEqual(output["low"], 2000.0)
        self.assertEqual(output["high"], 2000.0)

    def test_A01_arbitrary_som(self):
        td, root = self.new_workspace(); self.addCleanup(td.cleanup)
        state = load(root / "research-state.json")
        state["reachability"]["arbitrary_share_of_tam_or_sam"] = True
        save(root / "research-state.json", state)
        self.assert_invalid(root, "arbitrary SOM")

    def test_A02_fake_cac(self):
        td, root = self.new_workspace(); self.addCleanup(td.cleanup)
        state = load(root / "research-state.json")
        state["conditional_modules"]["unit_economics"]["metrics"]["cac"] = {
            "value": 237, "currency": "USD", "epistemic_state": "ESTIMATED", "evidence_ids": []
        }
        save(root / "research-state.json", state)
        self.assert_invalid(root, "fake CAC")

    def test_A03_attention_equals_demand(self):
        td, root = self.new_workspace(); self.addCleanup(td.cleanup)
        state = load(root / "research-state.json")
        state["demand"]["status"] = "DEMONSTRATED"
        state["demand"]["highest_tier"] = "F"
        state["demand"]["economic_demand_demonstrated"] = True
        state["demand"]["dimensions"]["problem_economic_burden"]["status"] = "STRONG"
        state["demand"]["dimensions"]["solution_wtp"]["status"] = "STRONG"
        save(root / "research-state.json", state)
        self.assert_invalid(root, "cannot by itself establish economic demand")

    def test_A04_analyst_tam_dependence(self):
        td, root = self.new_workspace(); self.addCleanup(td.cleanup)
        state = load(root / "research-state.json")
        state["sizing"]["tam"].update({"status": "QUANTIFIED", "method": "TOP_DOWN", "formula": "analyst report"})
        save(root / "research-state.json", state)
        self.assert_invalid(root, "analyst-TAM dependence")

    def test_A05_category_creation_collapse(self):
        td, root = self.new_workspace(); self.addCleanup(td.cleanup)
        state = load(root / "research-state.json")
        state["market_definition"]["category_creation"] = True
        state["sizing"]["pools"]["collapsed"] = True
        save(root / "research-state.json", state)
        self.assert_invalid(root, "category-creation collapse")

    def test_A06_unknown_suppression(self):
        td, root = self.new_workspace(); self.addCleanup(td.cleanup)
        ledger = load(root / "evidence-ledger.json")
        ledger["entries"].append({
            "id": "E001", "claim_input": "Actual CAC", "value": None, "low": None, "high": None,
            "unit": "USD/customer", "epistemic_state": "NOT_KNOWABLE_FROM_DESK_RESEARCH",
            "source": None, "source_id": None, "lineage_id": None, "origin_source_id": None,
            "source_lineage_ids": [], "source_date": None, "accessed_at": None, "effective_period": None,
            "source_type": None, "confidence": "NOT_APPLICABLE", "load_bearing": True,
            "fatal_gate_related": True, "demand_tier": None, "used_by": ["unit_economics"],
            "contradictions": [], "validation_next_step": "Run a bounded paid-acquisition test", "notes": None
        })
        save(root / "evidence-ledger.json", ledger)
        self.assert_invalid(root, "evidence burden mismatch")

    def test_A07_fatal_gate_burial(self):
        td, root = self.new_workspace(); self.addCleanup(td.cleanup)
        state = load(root / "research-state.json")
        state["phase"] = "SIZE"
        state["fatal_gates"] = [{"id": "F01", "condition": "Customers will pay", "status": "FAIL", "evidence_ids": [], "continue_reason": None}]
        save(root / "research-state.json", state)
        self.assert_invalid(root, "fatal-gate burial")

    def test_A08_context_blindness(self):
        td, root = self.new_workspace(); self.addCleanup(td.cleanup)
        state = load(root / "research-state.json")
        state["context_profile"] = {
            "evidence_emphasis": "Cohort durability, channel saturation, expansion, market penetration",
            "primary_question": "How much runway remains?"
        }
        save(root / "research-state.json", state)
        self.assert_invalid(root, "context blindness")

    def test_A09_cagr_ambiguity(self):
        td, root = self.new_workspace(); self.addCleanup(td.cleanup)
        state = load(root / "research-state.json")
        state["conditional_modules"]["growth"]["cagr"] = {
            "start_year": 2024, "end_year": 2026, "start_value": 100, "end_value": 150
        }
        save(root / "research-state.json", state)
        self.assert_invalid(root, "CAGR ambiguity")

    def test_A10_confirmation_only_search(self):
        td, root = self.new_workspace(); self.addCleanup(td.cleanup)
        self.seed_cruxes(root)
        state = load(root / "research-state.json")
        state["falsification"] = {
            "status": "COMPLETE", "queries": [], "evidence_ids": [], "contradictions": [],
            "coverage": [
                {"crux_id": "C01", "adversarial_search_ids": [], "strongest_for": "", "strongest_against": "",
                 "rival_explanation": "", "adjudication": "No contrary evidence logged.", "status_changed": False},
                {"crux_id": "C02", "adversarial_search_ids": [], "strongest_for": "", "strongest_against": "",
                 "rival_explanation": "", "adjudication": "No contrary evidence logged.", "status_changed": False}
            ]
        }
        save(root / "research-state.json", state)
        self.assert_invalid(root, "confirmation-only search")

    def test_A11_adversarial_theater(self):
        td, root = self.new_workspace(); self.addCleanup(td.cleanup)
        self.seed_cruxes(root)
        plan = load(root / "search-plan.json")
        plan["entries"] = [{
            "id": "SP001", "crux_id": "C01", "question": "Does the problem matter?",
            "support_observation": "Paid workaround", "refutation_observation": "Customers tolerate status quo",
            "preferred_source_classes": ["customer evidence"],
            "concepts": [{"concept": "problem", "synonyms": ["workflow"]}],
            "queries": [{"query": "why stopped paying for workflow", "polarity": "ADVERSARIAL", "route": "web"}],
            "stop_condition": "Saturation"
        }]
        save(root / "search-plan.json", plan)
        log = load(root / "search-log.json")
        log["entries"] = [{
            "id": "S001", "search_plan_id": "SP001", "crux_id": "C01",
            "query": "why stopped paying for workflow", "searched_at": "2026-08-31",
            "route": "web", "polarity": "ADVERSARIAL", "source_class": "customer evidence",
            "results_screened": 5, "evidence_ids": [], "refinement_reason": "", "stop_reason": "Saturation",
            "limitations": []
        }]
        save(root / "search-log.json", log)
        state = load(root / "research-state.json")
        state["falsification"] = {
            "status": "COMPLETE", "queries": [], "evidence_ids": [], "contradictions": [],
            "coverage": [
                {"crux_id": "C01", "adversarial_search_ids": ["S001"], "strongest_for": "A", "strongest_against": "B",
                 "rival_explanation": "C", "adjudication": "", "status_changed": False},
                {"crux_id": "C02", "adversarial_search_ids": [], "strongest_for": "", "strongest_against": "",
                 "rival_explanation": "", "adjudication": "Not yet tested.", "status_changed": False}
            ]
        }
        save(root / "research-state.json", state)
        self.assert_invalid(root, "adversarial theater")

    def test_A12_false_corroboration(self):
        td, root = self.new_workspace(); self.addCleanup(td.cleanup)
        ledger = load(root / "evidence-ledger.json")
        ledger["entries"] = [
            evidence("E001", "Eligible accounts", 100, lineage="L1"),
            evidence("E002", "Annual revenue/account", 20, lineage="L2", unit="USD/account/year"),
        ]
        save(root / "evidence-ledger.json", ledger)
        calculations = load(root / "calculations.json")
        calculations["entries"] = [{
            "id": "CALC001", "kind": "TAM", "operation": "PRODUCT",
            "input_evidence_ids": ["E001", "E002"], "parameters": {},
            "output": {"value": None, "low": None, "high": None, "unit": "USD/year"}, "notes": ""
        }]
        save(root / "calculations.json", calculations)
        self.assertEqual(run(str(CALCULATE), str(root)).returncode, 0)
        state = load(root / "research-state.json")
        state["sizing"]["tam"].update({
            "status": "QUANTIFIED", "method": "BOTTOM_UP", "formula": "E001 * E002",
            "calculation_id": "CALC001", "value": 2000.0, "low": 2000.0, "high": 2000.0,
            "input_evidence_ids": ["E001", "E002"]
        })
        state["sizing"]["cross_checks"] = [{
            "method": "TOP_DOWN", "status": "BOUNDED", "input_evidence_ids": ["E001", "E002"]
        }]
        save(root / "research-state.json", state)
        self.sync_burden(root)
        self.assert_invalid(root, "false corroboration")

    def test_A13_demand_dimension_conflation(self):
        td, root = self.new_workspace(); self.addCleanup(td.cleanup)
        state = load(root / "research-state.json")
        state["demand"]["status"] = "DEMONSTRATED"
        state["demand"]["highest_tier"] = "B"
        state["demand"]["economic_demand_demonstrated"] = True
        state["demand"]["dimensions"]["problem_economic_burden"]["status"] = "STRONG"
        state["demand"]["dimensions"]["solution_wtp"]["status"] = "WEAK"
        save(root / "research-state.json", state)
        self.assert_invalid(root, "demand-dimension conflation")

    def test_A14_hurdle_free_verdict(self):
        td, root = self.new_workspace(); self.addCleanup(td.cleanup)
        state = load(root / "research-state.json")
        state["verdict"] = {"status": "FINAL", "recommendation": "PURSUE", "summary": "Go", "confidence": "MEDIUM"}
        save(root / "research-state.json", state)
        self.assert_invalid(root, "hurdle-free verdict")

    def test_A15_prose_math_drift(self):
        td, root = self.new_workspace(); self.addCleanup(td.cleanup)
        ledger = load(root / "evidence-ledger.json")
        ledger["entries"] = [
            evidence("E001", "Eligible accounts", 100, lineage="L1"),
            evidence("E002", "Price", 20, lineage="L2"),
        ]
        save(root / "evidence-ledger.json", ledger)
        calculations = load(root / "calculations.json")
        calculations["entries"] = [{
            "id": "CALC001", "kind": "TAM", "operation": "PRODUCT",
            "input_evidence_ids": ["E001", "E002"], "parameters": {},
            "output": {"value": 999, "low": 999, "high": 999, "unit": "USD/year"}, "notes": ""
        }]
        save(root / "calculations.json", calculations)
        self.sync_burden(root)
        self.assert_invalid(root, "prose-math drift")

    def test_A16_structural_uncertainty_hiding(self):
        td, root = self.new_workspace(); self.addCleanup(td.cleanup)
        state = load(root / "research-state.json")
        state["market_definition"]["candidate_definitions"] = [
            {"id": "MD01", "label": "Narrow", "boundary": "Core buyers", "rationale": "Beachhead", "status": "SELECTED"},
            {"id": "MD02", "label": "Broad", "boundary": "Adjacent buyers", "rationale": "Expansion", "status": "CANDIDATE"},
        ]
        state["market_definition"]["selected_definition_id"] = "MD01"
        state["verdict"] = {"status": "FINAL", "recommendation": "TEST", "summary": "Test", "confidence": "LOW"}
        save(root / "research-state.json", state)
        self.assert_invalid(root, "structural uncertainty")


    def test_A17_institutional_scrutiny_theater(self):
        td, root = self.new_workspace("venture-growth"); self.addCleanup(td.cleanup)
        state = load(root / "research-state.json")
        state["verdict"] = {"status": "FINAL", "recommendation": "TEST", "summary": "Test", "confidence": "LOW"}
        save(root / "research-state.json", state)
        self.assert_invalid(root, "institutional scrutiny theater")

    def test_assurance_catalog_contains_v02_cases(self):
        payload = load(REPO / "evals" / "assurance-cases.json")
        cases = payload["cases"]
        self.assertGreaterEqual(len(cases), 17)
        self.assertEqual({c["id"] for c in cases[:17]}, {f"A{i:02d}" for i in range(1, 18)})

    def test_json_schemas_are_v02_and_valid_json(self):
        for path in (SKILL / "schemas").glob("*.json"):
            payload = load(path)
            self.assertEqual(payload["$schema"], "https://json-schema.org/draft/2020-12/schema")
            self.assertEqual(payload["properties"]["schema_version"]["const"], "0.2.0")

    def test_portable_prompt_is_generated_from_canonical_sources(self):
        result = run(str(GENERATE), "--check")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_internal_markdown_links_resolve(self):
        import re
        link = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        for md in REPO.rglob("*.md"):
            text = md.read_text(encoding="utf-8")
            for target in link.findall(text):
                if target.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                clean = target.split("#", 1)[0]
                if not clean:
                    continue
                resolved = (md.parent / clean).resolve()
                self.assertTrue(resolved.exists(), f"broken link in {md.relative_to(REPO)}: {target}")


if __name__ == "__main__":
    unittest.main()
