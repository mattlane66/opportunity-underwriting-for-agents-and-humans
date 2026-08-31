# Market Sizing

## Primary method

Prefer a bottom-up construction from observable economic units. Use top-down, value-based, and reference-class estimates as independent checks.

## Keep the pools distinct

- **Spend pool:** current customer expenditure/sacrifice.
- **Revenue pool:** plausible supplier revenue under the business model.
- **Value pool:** economic value created or losses avoided.

This separation is mandatory for category-creating opportunities.

## Common bottom-up forms

- B2B SaaS: eligible accounts × plausible ACV
- Consumer subscription: eligible paying consumers × annual revenue per payer
- Transaction: eligible transactions × revenue per transaction
- Marketplace: transactions × transaction value = GMV; GMV × take rate = platform revenue
- Usage-based: eligible customers × usage × revenue/unit
- Services: eligible customers × frequency × contract value

## TAM

Annual revenue opportunity if every economically eligible customer adopted the defined offering under the stated market definition.

## SAM

TAM after actual constraints: geography, regulation, segment, product capability, integrations, procurement, channel, service capacity, infrastructure, language, and implementation requirements.

## SOM / reachability

Never set SOM as an arbitrary TAM/SAM percentage.

A generic recurring model is:

`SOM_t = Reach_t × Conversion_t × Retention_t × RevenuePerCustomer_t`

If those parameters are not grounded, report that SOM is not presently estimable and specify the evidence/test needed to identify them.

## Deterministic calculation contract

For any quantified/bounded TAM or SAM:

1. record each load-bearing numeric input as evidence with units and epistemic state;
2. record source lineage(s);
3. declare a calculation in `calculations.json`;
4. run `scripts/calculate_study.py`;
5. copy the calculated values into the narrative/state only after calculation;
6. validate that narrative/state values still match the calculation.

The language model chooses and defends the formula and inputs. Deterministic code performs arithmetic.

## Independent cross-checking

At least one independent cross-check should be used for a decision-relevant size estimate.

Independence has two parts:

- **method independence** — e.g. bottom-up vs top-down/value-based/reference-class;
- **evidence-lineage independence** — not merely another URL repeating the same upstream statistic.

Some inputs can legitimately overlap. When they do, record what remains independent and why.

Reconcile definition differences rather than averaging mechanically.

## Structural uncertainty

If multiple plausible market boundaries materially change the result, preserve 2–3 definitions/models long enough to judge whether the **decision** is robust or sensitive across them.

## Quantitative hygiene

Record source date, access date, effective period, geography, units, currency, market definition, lineage, and epistemic state for every load-bearing sizing input. Avoid overlapping population double-counting.
