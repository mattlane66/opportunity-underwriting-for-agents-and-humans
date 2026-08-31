# Research State Contract

The file-backed workflow uses three authoritative JSON files.

## `input.json`

Human-supplied or explicitly provisional study inputs. Inferred values must be labeled as such in `input_provenance` rather than silently treated as user facts.

## `research-state.json`

The current underwriting state: context, phase, market definition, cruxes, fatal gates, gap/demand judgments, sizing, reachability, conditional modules, falsification, evidence burden, verdict, and next test.

## `evidence-ledger.json`

Atomic load-bearing evidence and variables with stable IDs, source/date, epistemic state, confidence, dependencies, contradictions, and validation next step.

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
