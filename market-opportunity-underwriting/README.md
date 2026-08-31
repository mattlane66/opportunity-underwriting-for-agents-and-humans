# Market Opportunity Underwriting

Evidence-based market opportunity underwriting for deciding whether a sufficiently large, reachable, economically attractive market exists for a specific business opportunity.

## Start in 60 seconds

If you just want to use it, go to **[START_HERE.md](START_HERE.md)**.

The simplest path is:

1. turn on the strongest research/deep-research mode in ChatGPT, Claude, Gemini, or another research-capable chat;
2. attach or paste [`PORTABLE_PROMPT.md`](PORTABLE_PROMPT.md);
3. provide five inputs: idea, customer, problem, geography, decision;
4. run the research;
5. read the Decision Brief first.

## Choose your path

### Research-capable chat — lowest friction

Use [`START_HERE.md`](START_HERE.md) and [`PORTABLE_PROMPT.md`](PORTABLE_PROMPT.md).

The portable path preserves the core methodology and a cumulative state packet, but cannot make persistence, search logging, deterministic math, and validation as reliable as a file-backed agent.

### Agent with files/code — highest execution quality

Use [`QUICKSTART.md`](QUICKSTART.md) and [`SKILL.md`](SKILL.md).

The workflow persists `input.json`, `research-state.json`, `evidence-ledger.json`, `search-plan.json`, `search-log.json`, and `calculations.json`.

### Audit or adapt the methodology

Read [`PROTOCOL.md`](PROTOCOL.md) and the focused references under [`references/`](references/).

## What v0.2 adds

The method now separates problem economic burden, budget availability, solution willingness to pay, behavioral adoption, and reachability.

It also adds explicit decision hurdles, stage-specific institutional scrutiny from seed VC through growth equity and PE commercial diligence, Value-of-Information-style research prioritization, reproducible search plans/logs, source-lineage tracking, structural/model uncertainty, deterministic market calculations, and crux-by-crux adversarial adjudication.

## Minimum human input

Idea, target customer, problem/job, initial geography, and decision to make are enough to start.

Additional inputs are optional. The method should research, bound, explicitly assume, or mark missing parameters as `NOT_KNOWABLE_FROM_DESK_RESEARCH`; it must not invent them merely to complete a model.

## What the workflow returns

The human-facing output is a **Decision Brief** organized around:

> hurdle → verdict → cruxes → market-in-gap dimensions → best-supported size → reachability → economics if knowable → structural robustness → fatal gate → evidence burden → highest-value next evidence

The **Underwriting Appendix** preserves the audit trail: market definitions, search plan/log, deterministic calculations, source lineages, evidence ledger, contradictory evidence, assumptions, conditional modules, sensitivity, and adversarial adjudication.

A valid result may be `PURSUE`, `TEST`, `HOLD`, or `REJECT`. It may also state that the market cannot yet be responsibly underwritten.

## Scope boundary

This skill underwrites the **market/commercial opportunity**. In PE/acquisition contexts it does not replace quality-of-earnings/accounting, legal/tax, technical/operational, management/governance, financing/debt-capacity, or other transaction diligence.
