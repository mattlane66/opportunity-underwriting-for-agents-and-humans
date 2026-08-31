# Market Opportunity Underwriting

Evidence-based market opportunity underwriting for deciding whether a sufficiently large, reachable, economically attractive market exists for a specific business opportunity.

## Choose your path

### Run with an agent and files — recommended

Use [`QUICKSTART.md`](QUICKSTART.md) and [`SKILL.md`](SKILL.md). The workflow persists an explicit research state and evidence ledger, validates hard methodological safeguards, and determines the smallest valid next move from the evidence actually available.

### Run in a plain chat product

Use [`PORTABLE_PROMPT.md`](PORTABLE_PROMPT.md). It is a generated fallback for ChatGPT, Claude, Gemini, or another capable research model. It preserves the core rules but cannot make state persistence as reliable as the file-backed workflow.

### Audit or adapt the methodology

Read [`PROTOCOL.md`](PROTOCOL.md) and the focused references under [`references/`](references/).

## Minimum human input

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
...
```

Additional inputs are optional. The method should research, bound, explicitly assume, or mark missing parameters as `NOT_KNOWABLE_FROM_DESK_RESEARCH`; it must not invent them merely to complete a model.

## What the workflow returns

The human-facing output is a **Decision Brief** organized around:

> decision → verdict → strongest evidence → load-bearing uncertainty → best-supported market size → reachability → economics if knowable → fatal gate → cheapest discriminating test

The **Underwriting Appendix** preserves the audit trail: market definitions, calculations, evidence ledger, contradictory evidence, searches, assumptions, conditional modules, sensitivity, and falsification.

A valid result may be `PURSUE`, `TEST`, `HOLD`, or `REJECT`. It may also state that the market cannot yet be responsibly underwritten.

## Core sequence

```text
0 Classify decision/context
  ↓
1 Find 2–3 cruxes
  ↓
2 Attack fatal gates
  ↓
3 Establish gap + economic demand
  ↓
4 Size only what is supportable
  ↓
5 Underwrite adoption/economics conditionally
  ↓
6 Falsify + synthesize decision
```

If a fatal gate fails, the workflow may stop early. Completion of sections is never a goal in itself.
