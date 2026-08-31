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
GENERATE = SCRIPTS / "generate_portable_prompt.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=REPO, text=True, capture_output=True, check=False)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


class UnderwritingContractTests(unittest.TestCase):
    def new_workspace(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
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
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return td, root

    def assert_invalid(self, root: Path, expected: str) -> None:
        result = run(str(VALIDATE), str(root))
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(expected, result.stdout + result.stderr)

    def test_clean_initialized_workspace_validates(self):
        td, root = self.new_workspace()
        self.addCleanup(td.cleanup)
        result = run(str(VALIDATE), str(root))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_next_move_is_cruxes_after_classification(self):
        td, root = self.new_workspace()
        self.addCleanup(td.cleanup)
        result = run(str(NEXT), str(root))
        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["next_phase"], "CRUXES")

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
        state["demand"].update({"status": "DEMONSTRATED", "highest_tier": "F", "economic_demand_demonstrated": True})
        save(root / "research-state.json", state)
        self.assert_invalid(root, "cannot by itself establish economic demand")

    def test_A04_analyst_tam_dependence(self):
        td, root = self.new_workspace(); self.addCleanup(td.cleanup)
        state = load(root / "research-state.json")
        state["sizing"]["tam"].update({"status": "QUANTIFIED", "method": "TOP_DOWN", "formula": "analyst report headline"})
        state["sizing"]["cross_checks"] = [{"method": "VALUE_BASED", "status": "BOUNDED"}]
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
            "source": None, "source_date": None, "source_type": None, "confidence": "NOT_APPLICABLE",
            "load_bearing": True, "fatal_gate_related": True, "used_by": ["unit_economics"],
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
        state["conditional_modules"]["growth"]["cagr"] = {"start_year": 2024, "end_year": 2026, "start_value": 100, "end_value": 150}
        save(root / "research-state.json", state)
        self.assert_invalid(root, "CAGR ambiguity")

    def test_A10_confirmation_only_search(self):
        td, root = self.new_workspace(); self.addCleanup(td.cleanup)
        state = load(root / "research-state.json")
        state["falsification"] = {
            "status": "COMPLETE",
            "queries": [{"query": "best market for test idea", "inverted": False}],
            "evidence_ids": [], "contradictions": []
        }
        save(root / "research-state.json", state)
        self.assert_invalid(root, "confirmation-only search")

    def test_assurance_catalog_contains_exactly_named_minimum_cases(self):
        payload = load(REPO / "evals" / "assurance-cases.json")
        cases = payload["cases"]
        self.assertGreaterEqual(len(cases), 10)
        self.assertEqual({c["id"] for c in cases[:10]}, {f"A{i:02d}" for i in range(1, 11)})

    def test_json_schemas_are_valid_json(self):
        for path in (SKILL / "schemas").glob("*.json"):
            payload = load(path)
            self.assertEqual(payload["$schema"], "https://json-schema.org/draft/2020-12/schema")

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
