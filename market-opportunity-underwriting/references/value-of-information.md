# Value-of-Information Research Prioritization

## Purpose

Crux-first reasoning only works if it controls the next research move.

Use a lightweight, ordinal Value-of-Information (VOI) heuristic to prioritize evidence collection. This borrows the decision principle from formal VOI analysis—additional information matters when it can improve a decision—without pretending that a napkin-stage business has enough probability distributions to calculate formal EVSI or EVPI.

## Research queue fields

For each unresolved research question record:

- target crux;
- decision impact: `FATAL | HIGH | MEDIUM | LOW`;
- uncertainty: `HIGH | MEDIUM | LOW`;
- expected ability of the proposed evidence to change the decision: `YES | UNCLEAR | NO`;
- evidence tractability: `HIGH | MEDIUM | LOW`;
- cost/time: `LOW | MEDIUM | HIGH`;
- proposed evidence/search/test;
- status.

## Priority bands

### P0

A fatal-gate question with meaningful uncertainty where evidence could change the decision.

### P1

A FATAL/HIGH crux with meaningful uncertainty and a tractable evidence path.

### P2

A useful but non-decisive question, or one with low tractability / low expected decision impact.

### DEFER

The variable is low impact, already sufficiently bounded, or cannot be identified by the proposed research.

Within the same band prefer:

1. higher uncertainty;
2. evidence more likely to change the decision;
3. higher tractability;
4. lower cost/time.

Do not generate decimal “information scores.” The ordinal ranking is a research-routing device, not a measured economic quantity.

## Highest-value next evidence

Replace “cheapest test” with:

> **highest-value next evidence**

Cost still matters. Prefer the cheapest evidence **among approaches capable of materially changing the decision**.

If no desk-research route can identify the variable, mark it `NOT_KNOWABLE_FROM_DESK_RESEARCH` and specify the field/pricing/acquisition/retention experiment needed.
