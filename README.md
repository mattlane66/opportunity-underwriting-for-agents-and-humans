# Opportunity Underwriting for Agents and Humans

Turn a business idea or market hypothesis into an evidence-backed **pursue / test / hold / reject** decision—without letting the agent manufacture certainty.

This repository contains reusable methods for business-level opportunity underwriting. Its first canonical skill is **[Market Opportunity Underwriting](./market-opportunity-underwriting/README.md)**: a crux-first, stateful workflow for deciding whether a sufficiently large, reachable, economically attractive market exists for a specific opportunity.

> **Spend research effort in proportion to decision relevance and uncertainty, not template completeness.**

The goal is not to produce a large TAM or an impressive-looking five-year model. A valid result is:

> We cannot yet underwrite this market. We have established X and Y, but Z is the load-bearing unknown. Here is the cheapest evidence that would change the decision.

## What this is—and is not

This methodology synthesizes established economic and forecasting methods with widely used venture and investment underwriting practices. **It is not itself a scientifically validated instrument**, and it does not claim that one canonical scientific TAM method exists.

It combines, when decision-relevant:

- bottom-up market construction with independent cross-checks;
- revealed-behavior and willingness-to-pay evidence;
- TAM / SAM / reachability logic without arbitrary “percent of TAM” SOM;
- reference-class forecasting and adoption modeling;
- unit economics when the inputs are actually knowable;
- competitive structure and “why does this gap exist?” analysis;
- explicit uncertainty, falsification, and fatal-gate reasoning.

## Relationship to Planning Skills

This repository answers a different question from [Planning Skills for Agents and Humans](https://github.com/mattlane66/planning-skills-for-agents-and-humans):

```text
Opportunity Underwriting
Should this opportunity be pursued?
        ↕
Evidence methods as needed
including Lead User Research
        │
   pursue? YES
        │
        ▼
Planning Skills
What should we make, and how?
```

The relationship is **not a fixed conveyor belt**.

- Opportunity Underwriting may invoke [Lead User Research](https://github.com/mattlane66/planning-skills-for-agents-and-humans/tree/main/lead-user-research) when a load-bearing uncertainty concerns future-facing needs, advanced users, emerging workarounds, or transferability.
- Lead User Research may hand off here when it establishes an important need but the remaining question is whether that need constitutes a sufficiently large, reachable, economically attractive market.
- Evidence from either method does not automatically become accepted product-planning truth. A human still decides whether to pursue the opportunity and what to commit to.

## First useful interaction

A human can start with only five inputs:

```text
Idea:
...

Target customer:
...

Problem / job:
...

Initial geography:
...

Decision to make:
Should I build this? / Should we enter this market? / Should we invest? / Other
```

The skill owns the research method. Missing information is researched, bounded, explicitly assumed, or marked **NOT_KNOWABLE_FROM_DESK_RESEARCH** rather than silently invented.

See the [Quickstart](./market-opportunity-underwriting/QUICKSTART.md) for the file-backed path and [Portable Prompt](./market-opportunity-underwriting/PORTABLE_PROMPT.md) for a copy-paste fallback.

## Canonical implementation

The robust path is the repo-backed skill:

- [`SKILL.md`](./market-opportunity-underwriting/SKILL.md) — agent operating contract;
- [`PROTOCOL.md`](./market-opportunity-underwriting/PROTOCOL.md) — canonical methodology;
- [`schemas/`](./market-opportunity-underwriting/schemas/) — input, research-state, and evidence-ledger contracts;
- [`scripts/`](./market-opportunity-underwriting/scripts/) — initialization, validation, next-move, portable-prompt generation;
- [`templates/`](./market-opportunity-underwriting/templates/) — human intake, Decision Brief, and Underwriting Appendix;
- [`evals/assurance-cases.json`](./evals/assurance-cases.json) — ten methodological failure cases;
- [`tests/`](./tests/) — deterministic enforcement of the hardest safeguards.

The portable prompt is generated from canonical marked sections of the skill/protocol so it cannot silently drift from the repo-backed method.

## Core epistemic states

Every load-bearing claim or variable should be classified as:

- **OBSERVED** — directly evidenced;
- **ESTIMATED** — calculable from reasonably strong evidence;
- **BOUNDED** — a credible range can be established;
- **ASSUMPTION** — required for modeling but not evidenced;
- **NOT_KNOWABLE_FROM_DESK_RESEARCH** — requires new empirical evidence.

`NOT_KNOWABLE_FROM_DESK_RESEARCH` is a successful analytical result.

## License

MIT. See [LICENSE](./LICENSE).
