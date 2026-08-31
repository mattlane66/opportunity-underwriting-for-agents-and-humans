#!/usr/bin/env python3
"""Generate the portable fallback prompt from canonical marked source sections."""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
PROTOCOL = ROOT / "PROTOCOL.md"
BRIEF = ROOT / "templates" / "research-brief.md"
OUTPUT = ROOT / "PORTABLE_PROMPT.md"


def extract(path: Path, start: str, end: str) -> str:
    text = path.read_text(encoding="utf-8")
    if start not in text or end not in text:
        raise ValueError(f"missing portable markers in {path}")
    return text.split(start, 1)[1].split(end, 1)[0].strip()


def render() -> str:
    skill_core = extract(SKILL, "<!-- PORTABLE:SKILL:START -->", "<!-- PORTABLE:SKILL:END -->")
    protocol_core = extract(PROTOCOL, "<!-- PORTABLE:PROTOCOL:START -->", "<!-- PORTABLE:PROTOCOL:END -->")
    brief = BRIEF.read_text(encoding="utf-8").strip()
    return f'''# Portable Prompt — Market Opportunity Underwriting\n\n> **GENERATED FILE.** Canonical source: `SKILL.md`, `PROTOCOL.md`, and `templates/research-brief.md`. Run `scripts/generate_portable_prompt.py` to regenerate.\n\nUse the following as your operating instructions for this research session. When file persistence is unavailable, end each stage with a cumulative state packet containing the decision hurdle, scrutiny profile, context, cruxes, research priorities, fatal gates, market definitions, evidence/source lineages, sizing/calculation state, unknowns, falsification coverage, and highest-value next evidence. Treat the latest packet as the authoritative replacement snapshot when resuming.\n\n{skill_core}\n\n---\n\n{protocol_core}\n\n---\n\n## Human input\n\n{brief}\n\n## Required final output\n\nReturn a concise **Decision Brief** first, followed by an **Underwriting Appendix** only to the depth the evidence supports. Never create missing metrics merely to fill the appendix.\n'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render()
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != expected:
            print("PORTABLE_PROMPT.md is out of sync. Regenerate it.")
            return 1
        print("PORTABLE_PROMPT.md is synchronized")
        return 0
    OUTPUT.write_text(expected, encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
