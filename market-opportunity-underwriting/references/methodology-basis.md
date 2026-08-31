# Methodological Basis and Limits

This repository does **not** claim that one scientifically canonical market-sizing or investment-underwriting instrument exists. It combines separately established analytical methods with explicit practitioner conventions and then adds deterministic safeguards for AI execution.

## Bottom-up market construction and venture practice

Investor guidance commonly prefers bottom-up construction because it forces explicit customer, price/WTP, and distribution assumptions rather than taking an arbitrary share of an aggregate market.

Representative practitioner sources:

- Y Combinator, startup/pitch guidance: https://www.ycombinator.com/
- Andreessen Horowitz, “16 Startup Metrics”: https://a16z.com/16-startup-metrics/
- Andreessen Horowitz, “Aligning Startup Metrics with Stage of Maturity”: https://a16z.com/aligning-startup-metrics-with-stage-of-maturity-beyond-labels-for-fundraising-rounds/
- Andreessen Horowitz, growth-metrics methodology: https://a16z.com/introducing-a16z-growths-guide-to-growth-metrics/
- Bessemer Venture Partners, “Scaling from $1 to $10 million ARR”: https://www.bvp.com/atlas/scaling-from-1-to-10-million-arr

These are practitioner heuristics and observed investing conventions, not scientific validation of this full protocol. Stage-specific benchmark numbers are context-dependent and should not be copied into an unevidenced company model.

## Institutional / private-equity commercial diligence

Later-stage underwriting should use actual commercial evidence rather than extending early-stage proxies.

Representative practitioner sources:

- Bain & Company, “Integrating Due Diligence to Build Lasting Value”: https://www.bain.com/contentassets/471f0047d66148a7ae93bcdf80e8468a/bain_brief_integrating_due_diligence_to_build_lasting_value_2.pdf
- Bain & Company, “Is Your Tech Due Diligence Good Enough?”: https://www.bain.com/insights/tech-due-diligence-global-private-equity-report-2022/
- McKinsey, “The second look: An adaptive approach to reunderwriting” (2026): https://www.mckinsey.com/industries/private-capital/our-insights/the-second-look-an-adaptive-approach-to-reunderwriting
- McKinsey, “Beating the odds: How private equity firms can improve exit prospects” (2026): https://www.mckinsey.com/industries/private-capital/our-insights/beating-the-odds-how-private-equity-firms-can-improve-exit-prospects

These support the use of thesis-driven integrated commercial diligence, stage-appropriate KPIs, retention/concentration/pricing evidence, value-creation logic, and periodic reunderwriting. This repository remains **commercial/market underwriting**, not a replacement for quality-of-earnings, legal, tax, technical, management, financing, or other diligence.

## Discrete choice and willingness to pay

Daniel McFadden received the 2000 Sveriges Riksbank Prize in Economic Sciences for developing theory and methods for analyzing discrete choice:

https://www.nobelprize.org/nobel_prizes/economic-sciences/laureates/2000/mcfadden-facts.html

Discrete-choice/conjoint methods are relevant when real experimental/respondent data exist. Their existence does not make WTP knowable from desk research alone.

## Reference-class forecasting

The outside-view / reference-class idea is used to counter inside-view optimism by comparing a case with outcomes from a relevant reference class. This protocol requires every full study to **consider** a reference class and uses one only when defensible analogs exist.

One accessible practitioner-academic treatment is Lovallo & Kahneman, “Delusions of Success,” Harvard Business Review (2003):

https://hbr.org/2003/07/delusions-of-success-how-optimism-undermines-executives-decisions

## Diffusion

Frank Bass's 1969 model is a foundational new-product diffusion model:

- Bass, F. M. (1969), “A New Product Growth for Model Consumer Durables,” *Management Science* 15(5), 215–227. https://doi.org/10.1287/mnsc.15.5.215

The model is optional here. Novel products often lack defensible diffusion parameters; the protocol therefore permits “model structure known, parameters unknown.”

## Value of information and research prioritization

Formal Value-of-Information (VOI) analysis evaluates whether reducing uncertainty could improve a decision and whether additional evidence is worth obtaining.

- ISPOR Value of Information Analysis Emerging Good Practices Task Force, introductory report: https://www.ispor.org/heor-resources/good-practices/article/value-of-information-analysis-for-research-decisions-an-introduction
- ISPOR analytical-methods report: https://www.ispor.org/heor-resources/good-practices/article/value-of-information-analytical-methods-report-2

This repository **does not calculate formal EVPI/EVSI for thin startup evidence**. It borrows the decision principle and implements a transparent ordinal queue based on decision impact, uncertainty, expected ability to change the decision, evidence tractability, and cost/time.

## Search reproducibility

Systematic-review search standards provide useful retrieval-discipline principles even though market underwriting is not a systematic clinical review.

Cochrane requires contemporaneous documentation of searched sources, dates, terms, and enough exact search detail to make retrieval reproducible where possible:

https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04

This protocol borrows that reproducibility principle for decision-critical commercial research through `search-plan.json` and `search-log.json`.

## Structural and parameter uncertainty

The protocol distinguishes uncertainty in numeric parameters from uncertainty in the **model/market definition itself**. When plausible alternative definitions could change the decision, they are preserved and the verdict is tested for robustness rather than hidden inside one point estimate.

## Limits

No combination of these methods removes the need for judgment, empirical validation, or domain-specific diligence. The protocol is designed to make assumptions, contradictions, unobservable variables, retrieval gaps, source dependence, and arithmetic drift harder to hide—not to turn uncertain business decisions into scientific certainty.
