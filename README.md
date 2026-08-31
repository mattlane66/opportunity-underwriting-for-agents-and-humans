# Opportunity Underwriting for Agents and Humans

Turn a business idea or market hypothesis into an evidence-backed **pursue / test / hold / reject** decision—without letting the agent manufacture certainty.

This repository contains reusable methods for business-level opportunity underwriting. Its first canonical skill is **[Market Opportunity Underwriting](./market-opportunity-underwriting/README.md)**: a crux-first, stateful workflow for deciding whether a sufficiently large, reachable, economically attractive market exists for a specific opportunity.

> **Spend research effort in proportion to decision relevance and uncertainty, not template completeness.**

## Use it

**Want the easiest path?** Open **[Start Here](./market-opportunity-underwriting/START_HERE.md)**.

For most people:

> turn on a research/deep-research mode → attach/paste the portable prompt → provide idea, customer, problem, geography, and decision → run

For repeatable or investment-committee-grade work, use the repo-backed skill so the agent persists search logs, source lineages, deterministic calculations, and validated research state.

## What this is—and is not

This methodology synthesizes established economic and forecasting methods with widely used venture and investment underwriting practices. **It is not itself a scientifically validated instrument**, and it does not claim that one canonical scientific TAM method exists.

It combines, when decision-relevant:

- crux-first and fatal-gate underwriting;
- stage-specific scrutiny from seed venture through growth and PE commercial diligence;
- bottom-up market construction with independent cross-checks;
- separate economic-burden, budget, solution-WTP, adoption, and reachability judgments;
- revealed-behavior and willingness-to-pay evidence;
- TAM / SAM / reachability logic without arbitrary “percent of TAM” SOM;
- reference-class forecasting and adoption modeling;
- unit economics when inputs are actually knowable;
- explicit decision hurdles and structural/model uncertainty;
- reproducible search logs and source lineage;
- deterministic calculations;
- explicit uncertainty and crux-by-crux falsification.

The goal is not to produce a large TAM or an impressive-looking five-year model. A valid result is:

> We cannot yet underwrite this market. We have established X and Y, but Z is the load-bearing unknown. Here is the highest-value evidence that would change the decision.

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

## Canonical implementation

- [`START_HERE.md`](./market-opportunity-underwriting/START_HERE.md) — shortest human path;
- [`SKILL.md`](./market-opportunity-underwriting/SKILL.md) — agent operating contract;
- [`PROTOCOL.md`](./market-opportunity-underwriting/PROTOCOL.md) — canonical methodology;
- [`schemas/`](./market-opportunity-underwriting/schemas/) — input, state, evidence, search, and calculation contracts;
- [`scripts/`](./market-opportunity-underwriting/scripts/) — initialization, VOI routing, calculations, validation, and portable-prompt generation;
- [`templates/`](./market-opportunity-underwriting/templates/) — human intake, Decision Brief, and Underwriting Appendix;
- [`evals/assurance-cases.json`](./evals/assurance-cases.json) — machine-checkable methodological failure cases;
- [`tests/`](./tests/) — deterministic enforcement of the hardest safeguards.

The portable prompt is generated from canonical marked sections of the skill/protocol so it cannot silently drift from the repo-backed method.

## Core epistemic states

Every load-bearing claim or variable should be classified as:

- **OBSERVED**
- **ESTIMATED**
- **BOUNDED**
- **ASSUMPTION**
- **NOT_KNOWABLE_FROM_DESK_RESEARCH**

`NOT_KNOWABLE_FROM_DESK_RESEARCH` is a successful analytical result.

## License

MIT. See [LICENSE](./LICENSE).
