# Research State Contract

The file-backed workflow uses six authoritative JSON files.

## `input.json`

Human-supplied or explicitly provisional study inputs, including decision context and institutional scrutiny profile. Inferred values must be labeled rather than silently treated as user facts.

## `research-state.json`

The current underwriting state:

- context and scrutiny profile;
- decision hurdle;
- market definitions and structural robustness;
- cruxes and Value-of-Information research queue;
- fatal gates;
- gap/demand dimensions;
- sizing and reachability;
- conditional modules;
- falsification coverage/adjudication;
- evidence burden;
- verdict and highest-value next evidence.

## `evidence-ledger.json`

Atomic load-bearing evidence and variables with stable IDs, values/ranges, epistemic state, demand tier where relevant, source/date, source lineage, dependencies, contradictions, and validation next step.

For source-backed claims the ledger also records claim temporality, source directness, freshness-check time, contradiction evidence IDs, and conflict resolution/adjudication. Load-bearing current-product-state claims therefore preserve whether the evidence is primary or non-primary and how contradictory current first-party evidence was handled.

## `search-plan.json`

The intended search lattice for decision-critical cruxes: support/refutation observations, source classes, synonym families, queries, and stop conditions.

## `search-log.json`

What was actually searched: exact query, date, route, polarity, source class, screened results, evidence created, refinements, limitations, and stop reason.

## `calculations.json`

Deterministic arithmetic derived from evidence-ledger inputs. Quantified TAM/SAM and other material calculations should point here rather than relying on prose math.

## Authority

When these files exist, they are authoritative over conversational recollection. Narrative outputs are derived views and must not silently modify state.

## Epistemic states

Allowed values:

- `OBSERVED`
- `ESTIMATED`
- `BOUNDED`
- `ASSUMPTION`
- `NOT_KNOWABLE_FROM_DESK_RESEARCH`

## Confidence

Allowed secondary confidence values:

- `HIGH`
- `MEDIUM`
- `LOW`
- `NOT_APPLICABLE`

Confidence does not replace epistemic state.

## Source lineage

Multiple secondary pages that repeat one upstream statistic are one evidence lineage. Load-bearing observed evidence records its inspected source and lineage; estimates/bounds record the lineages on which they depend.

## State-before-story

Research and calculation state must be written before final narrative synthesis. A polished brief that disagrees with persisted state is invalid.
