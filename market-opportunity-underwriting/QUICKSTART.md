# Quickstart — File-Backed Execution

For the easiest human path, use [`START_HERE.md`](START_HERE.md). Use this guide when the AI can read/write files and run scripts.

## 1. Initialize a study

From the repository root:

```bash
python market-opportunity-underwriting/scripts/init_study.py \
  --workspace research/my-opportunity \
  --idea "..." \
  --customer "..." \
  --problem "..." \
  --geography "United States" \
  --decision "Should we pursue this?" \
  --context napkin-stage \
  --scrutiny-profile general
```

Supported decision contexts: `napkin-stage`, `prototype-pre-revenue`, `early-revenue`, `growth-stage`, `corporate-market-entry`, `investor-acquisition`, and `other`.

Optional scrutiny profiles: `general`, `venture-seed`, `venture-early`, `venture-growth`, `growth-equity`, `pe-commercial-diligence`, and `corporate`.

Use the profile that matches the **actual evidence maturity**. Do not select a later-stage profile to make the report look more sophisticated.

## 2. Persist the whole research contract

Initialization creates:

```text
input.json
research-state.json
evidence-ledger.json
search-plan.json
search-log.json
calculations.json
outputs/
```

At the beginning of **every research move**, reopen all six JSON files. Persisted state is authoritative over chat memory.

## 3. Identify cruxes and build the research queue

Define 2–3 load-bearing cruxes and possible fatal gates. Then add research-queue items with decision impact, uncertainty, expected ability of evidence to change the decision, evidence tractability, cost/time, proposed evidence, and search-plan IDs.

Inspect the ordinal priority:

```bash
python market-opportunity-underwriting/scripts/rank_research_queue.py research/my-opportunity
```

This is not a fake numeric EVSI score. It is a transparent routing rule for deciding what to investigate next.

## 4. Ask for the next move

```bash
python market-opportunity-underwriting/scripts/next_research_move.py research/my-opportunity
```

The output names both the smallest valid phase and, when available, the highest-priority unresolved research item.

## 5. Research the active crux

For every FATAL/HIGH crux, define supporting and refuting observations, preferred source classes, synonym families, confirmatory and adversarial queries, and a stop condition in `search-plan.json`. Record exact searches in `search-log.json` and source lineage in `evidence-ledger.json`.

Do not count different webpages repeating one upstream statistic as independent corroboration.

## 6. Calculate rather than narrate math

Declare market calculations in `calculations.json`, then run:

```bash
python market-opportunity-underwriting/scripts/calculate_study.py research/my-opportunity
```

The language model chooses and defends the formula and evidence inputs. Deterministic code performs the arithmetic.

## 7. Validate before advancing

```bash
python market-opportunity-underwriting/scripts/validate_study.py research/my-opportunity
```

The validator catches arbitrary SOM, unsupported CAC, demand-dimension conflation, top-down-only TAM, false corroboration, hidden unknowns, buried fatal gates, context/scrutiny blindness, ambiguous CAGR, missing adversarial coverage, adversarial theater, hurdle-free final decisions, and stale/non-reproducible calculations.

## 8. Deliver two artifacts

Use [`templates/decision-brief.md`](templates/decision-brief.md) for the short decision surface and [`templates/underwriting-appendix.md`](templates/underwriting-appendix.md) for the audit trail.

## No file tools?

Use [`PORTABLE_PROMPT.md`](PORTABLE_PROMPT.md). Preserve a cumulative state packet containing the decision hurdle, scrutiny profile, active cruxes, research priorities, fatal gates, market definitions, evidence/source lineages, sizing/calculations, unknowns, falsification coverage, and highest-value next evidence.
