# Quickstart

## 1. Initialize a study

From the repository root:

```bash
python market-opportunity-underwriting/scripts/init_study.py \
  --workspace research/my-opportunity \
  --idea "..." \
  --customer "..." \
  --problem "..." \
  --geography "United States" \
  --decision "Should we build this?" \
  --context napkin-stage
```

Supported decision contexts:

- `napkin-stage`
- `prototype-pre-revenue`
- `early-revenue`
- `growth-stage`
- `corporate-market-entry`
- `investor-acquisition`
- `other`

The initializer refuses a non-empty workspace.

## 2. Ask for the next move

```bash
python market-opportunity-underwriting/scripts/next_research_move.py research/my-opportunity
```

The output is deterministic. It recommends the smallest valid next move from persisted state rather than assuming the last chat turn completed a stage.

## 3. Research only the active crux

At every move:

1. reopen `input.json`, `research-state.json`, and `evidence-ledger.json`;
2. identify the 2–3 load-bearing assumptions and the least-supported one;
3. concentrate research on that uncertainty;
4. record evidence and contradictions before writing narrative prose;
5. use one of the five epistemic states for every load-bearing variable:
   - `OBSERVED`
   - `ESTIMATED`
   - `BOUNDED`
   - `ASSUMPTION`
   - `NOT_KNOWABLE_FROM_DESK_RESEARCH`

## 4. Validate before advancing

```bash
python market-opportunity-underwriting/scripts/validate_study.py research/my-opportunity
```

The validator catches structural errors and several methodological violations, including arbitrary SOM, unsupported napkin-stage CAC, attention-only demand claims, ambiguous CAGR metadata, and suppression of required unknowns.

## 5. Deliver two artifacts

Use:

- [`templates/decision-brief.md`](templates/decision-brief.md) for the short decision surface;
- [`templates/underwriting-appendix.md`](templates/underwriting-appendix.md) for the inspectable audit trail.

Do not make the brief look more certain than the evidence ledger.

## No file tools?

Use [`PORTABLE_PROMPT.md`](PORTABLE_PROMPT.md). At the end of each research stage, preserve a cumulative state packet containing the active decision, cruxes, fatal gates, evidence ledger, market calculations, unknowns, and next test. Treat the latest packet as the authoritative replacement snapshot when resuming.
