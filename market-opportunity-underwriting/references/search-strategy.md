# Search Strategy and Research Quality

## Principle

Search quality is part of evidence quality. The study must preserve enough of the retrieval process that a reviewer can understand what was looked for, how the search changed, and why it stopped.

## Search lattice per crux

Before broad searching, translate each FATAL/HIGH crux into:

1. **Claim** — what must be true?
2. **Support observation** — what real-world evidence would increase confidence?
3. **Refutation observation** — what evidence would weaken or falsify it?
4. **Preferred source classes** — where should that evidence exist?
5. **Concept families / synonyms** — how might different sources describe it?
6. **Confirmatory queries**
7. **Adversarial queries**
8. **Stop condition**

Do not use one generic query family for the whole market.

## Claim-specific source routing

Prefer sources based on the fact being measured.

| Claim type | Preferred source classes |
| --- | --- |
| population / business denominator | official statistics, regulators, tax/administrative data, industry registries |
| public-company revenue/margins/customers | filings, earnings materials, audited statements |
| pricing | first-party pricing, contracts, procurement docs, paid invoices/pilots |
| regulation | statute/regulator/agency guidance |
| customer behavior | transactions, product/cohort data, procurement, direct traces, field evidence |
| workarounds / unmet needs | direct user traces, Lead User evidence, support/issue records |
| market growth | normalized primary time series where possible |
| competitor outcomes | filings, shutdown/acquisition records, customer switching evidence, credible reporting |
| academic method | peer-reviewed or professional-method standards |

A source can be authoritative yet still have the wrong definition. Record scope, geography, period, and unit.

## Reproducible search log

For decision-critical searches record:

- exact query;
- date/time;
- target crux;
- confirmatory / adversarial / neutral polarity;
- search route or database;
- intended source class;
- result count screened when available;
- evidence IDs created;
- refinement reason;
- stop reason;
- important limitations.

The goal is reproducibility and auditability, not a quota of searches.

## Source lineage

Multiple webpages that repeat one underlying statistic are one evidence lineage.

For sourced evidence record:

- `source_id` — the item actually inspected;
- `lineage_id` — common origin lineage;
- `origin_source_id` when the upstream origin can be identified;
- access date;
- effective/data period.

A cross-check is not independent merely because it comes from a different URL.

## Search branching

Use at least two meaningfully different retrieval routes for a FATAL/HIGH crux when practical, for example:

- official/statistical source + customer/market behavior;
- company filings + independent customer evidence;
- direct pricing + procurement/budget evidence;
- semantic discovery + explicit adversarial search.

Do not mistake many similar search queries for independent branches.

## Falsification coverage

Every FATAL/HIGH crux needs an adversarial pass. Record:

- strongest evidence for;
- strongest evidence against;
- strongest rival explanation;
- adversarial search IDs;
- adjudication after seeing the contradictory evidence;
- whether the crux status changed and why.

Contradictory evidence does not have to flip the conclusion, but it must be adjudicated rather than merely listed.

## Research stopping

Stop desk research on a crux when one of these is true:

- a fatal gate has failed and further desk research is unlikely to reverse it;
- the remaining variable is `NOT_KNOWABLE_FROM_DESK_RESEARCH`;
- additional searches are returning the same evidence lineages without changing the bound;
- plausible source classes have been covered sufficiently for the decision;
- the verdict is robust to the remaining uncertainty.

Record the stop reason.
