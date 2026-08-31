# Market Opportunity Underwriting Protocol

## Status and scope

This is the canonical methodological specification for **Market Opportunity Underwriting**.

The method is a synthesis of established economic and forecasting methods with widely used venture and investment underwriting practices. **It is not itself a scientifically validated instrument.** There is no single scientifically canonical TAM method. The purpose of this protocol is to make the synthesis explicit, falsifiable, inspectable, and difficult for an AI agent to turn into rigor theater.

The method answers a business-level question:

> **Does a sufficiently large, reachable, economically attractive market exist for this specific opportunity, and what evidence would change that judgment?**

It is not a substitute for product framing, solution shaping, implementation planning, legal diligence, accounting diligence, or actual customer experiments.

<!-- PORTABLE:PROTOCOL:START -->
## 1. Operating principle: crux-first underwriting

Do not research every section evenly.

At the beginning of the study identify the **2–3 load-bearing cruxes**:

> What must be true for this opportunity to be attractive?

Then ask:

> Which of those cruxes is least supported and most decision-sensitive?

Allocate research depth to that uncertainty first.

A **fatal gate** is a condition which, if false, makes the opportunity unattractive regardless of otherwise favorable scores. Examples include no credible willingness to pay, a legally inaccessible market, structurally negative contribution economics, or a reachable population too small for the required outcome.

Attack fatal gates before building elaborate forecasts. If a fatal gate fails, stop unless additional evidence could plausibly reverse the gate. The workflow may legitimately terminate before completing optional sections.

## 2. Decision context changes the evidence standard

Classify the opportunity before judging it.

| Context | Evidence standard | What matters most |
| --- | --- | --- |
| `napkin-stage` | Problem behavior, existing economic sacrifice, WTP proxies, bottom-up bounds | Is there enough evidence to justify testing? |
| `prototype-pre-revenue` | Usage, pilots, behavioral intent, pricing experiments | Does behavior convert into economic demand? |
| `early-revenue` | Cohorts, actual price, CAC, retention, contribution margin | Can the business scale economically? |
| `growth-stage` | Cohort durability, channel saturation, expansion, penetration | How much runway remains? |
| `corporate-market-entry` | Strategic fit, channel leverage, cannibalization, capability gaps, ROIC | Is this attractive for this company? |
| `investor-acquisition` | Quality of earnings, penetration ceiling, durability, downside | What return can actually be underwritten? |
| `other` | Explicitly define the governing decision standard | What evidence is actually decision-relevant? |

Do not require observed CAC from a napkin-stage idea. Do not accept interview enthusiasm as sufficient evidence for a growth-stage acquisition.

## 3. Epistemic state is first-class

For every material claim or variable use one of five states:

### `OBSERVED`
Directly evidenced by a source or actual behavior.

Examples: Census account count, signed contract price, observed cohort retention, regulatory rule.

### `ESTIMATED`
Calculated from reasonably strong observed inputs with a transparent formula.

Examples: eligible accounts after applying sourced filters; weighted average transaction value from observed data.

### `BOUNDED`
A defensible range can be established, but a point estimate would overstate knowledge.

Examples: plausible ACV from comparable prices plus budget evidence; eligible population bracket from two source definitions.

### `ASSUMPTION`
Needed to explore a model but not evidenced strongly enough to be treated as an estimate.

Assumptions must be visible in the evidence burden and sensitivity analysis when they are load-bearing.

### `NOT_KNOWABLE_FROM_DESK_RESEARCH`
The parameter requires new empirical evidence.

Examples for an unlaunched product often include actual CAC, activation, retention, conversion, and sometimes willingness to pay.

This state is a **successful analytical result**. Do not replace it with a benchmark-derived pseudo-estimate merely to complete a table.

For every `NOT_KNOWABLE_FROM_DESK_RESEARCH` load-bearing variable specify the **cheapest discriminating test** that could materially reduce uncertainty.

## 4. Define the market before sizing it

Record:

- target user;
- economic buyer;
- problem/job;
- use case;
- geography;
- time horizon;
- unit of demand;
- revenue model;
- market/category boundary;
- substitutes and current alternatives;
- explicit exclusions;
- decision threshold, if one exists.

State the measurement unit. Do not mix customers, transactions, GMV, supplier revenue, gross profit, and value created.

When multiple market definitions are legitimate, model 2–3 candidate definitions briefly and choose the definition most relevant to the decision. Record how the choice affects the result.

## 5. Establish whether the gap is real

Absence of competitors is not evidence of an opportunity.

Investigate what customers do today:

- direct competitors;
- indirect competitors;
- internal build;
- consultants/services;
- manual labor;
- spreadsheets or tool stacks;
- process compromises;
- doing nothing.

Look for persistent deficiencies:

- costly workarounds;
- repeated switching or failed adoption;
- user-created solutions;
- abandoned purchases;
- measurable poor outcomes;
- requests for missing capabilities;
- internal headcount or process burden;
- risk or opportunity cost.

Then investigate **why the gap exists**. Plausible explanations include weak demand, low WTP, technical infeasibility, regulation, fragmented demand, bad distribution economics, switching costs, incumbent bundling, or historical timing. Opportunity-positive explanations may include a new enabling technology, cost curve, regulatory shift, channel change, or behavior change.

The analysis must consider both classes of explanation.

## 6. Establish whether there is a market in the gap

Use this evidence hierarchy.

### Tier A — Transactional evidence

- purchases;
- signed contracts;
- paid pilots;
- deposits/preorders;
- actual switching;
- budget reallocation.

### Tier B — Existing economic sacrifice

- spend on inferior substitutes;
- consultants;
- internal headcount;
- manual labor;
- workaround software stacks;
- measurable cost or risk from the problem.

### Tier C — Behavioral demand

- repeated usage;
- retention;
- active procurement;
- internal-build attempts;
- high-intensity workaround behavior;
- repeated requests with consequential follow-through.

### Tier D — Structured preference evidence

- choice-based conjoint;
- discrete-choice experiments;
- real pricing experiments;
- reservation-price / willingness-to-pay studies.

### Tier E — Stated preference

- surveys;
- interviews;
- stated purchase intent.

### Tier F — Attention signals

- search volume;
- social discussion;
- traffic;
- press;
- community activity.

Tier E and F may support discovery or interpretation. They do **not** by themselves establish economic demand.

The research record must answer:

> If this solution existed tomorrow at a realistic price, what credible evidence indicates that customers would actually change behavior and transfer money or budget toward it?

If the answer is weak, say so.

## 7. Keep three economic pools separate

Especially for category-creating ideas, distinguish:

### Spend pool
What customers currently spend solving the problem.

### Revenue pool
What suppliers could plausibly capture as revenue under a viable business model.

### Value pool
The economic value the solution could create or losses it could avoid.

Current spend does not automatically cap future revenue/value. Likewise, a large theoretical value pool does not imply customers will pay an equivalent amount.

## 8. Build bottom-up TAM first when feasible

TAM is the annual revenue opportunity if every economically eligible customer adopted the defined offering under the stated market definition.

Use an observable unit model appropriate to the business:

- B2B: eligible accounts × plausible annual contract revenue;
- consumer subscription: eligible consumers × annual revenue per paying consumer;
- transaction: eligible annual transactions × revenue per transaction;
- marketplace: GMV = transactions × transaction value; supplier/platform revenue = GMV × sustainable take rate;
- usage-based: eligible customers × usage × revenue per unit;
- services: eligible customers × frequency × contract value.

For every major input record source, date, unit, epistemic state, confidence, and range where relevant.

Do not double-count overlapping populations or spending pools.

## 9. Require an independent sizing cross-check

Use at least one independent check when a sizing conclusion is decision-relevant.

Possible methods:

### Top-down cross-check
Use authoritative aggregate data to bound the economic activity. Prefer official statistics, regulatory filings, company financials, industry associations, peer-reviewed research, then high-quality proprietary research. Commercial analyst reports are secondary evidence, not a substitute for reconstruction.

### Value-based cross-check
Estimate economic value lost/created × addressable share × plausible monetization share. This can establish a ceiling or alternative view for category-creating markets.

### Reference-class cross-check
Use comparable market outcomes as an outside-view constraint when defensible analogs exist.

Do not average conflicting methods mechanically. Explain definition differences and reconcile them.

## 10. Calculate SAM with actual constraints

SAM is the portion of TAM the proposed offering and business model can genuinely serve within the relevant strategic horizon.

Apply material constraints such as:

- geography;
- regulation;
- segment/customer size;
- product capability;
- integration requirements;
- procurement model;
- channel reach;
- service capacity;
- language/infrastructure;
- implementation complexity.

Show the exclusions explicitly.

## 11. Reachability and SOM: model structure before numbers

Never define SOM as an arbitrary share such as “2% of TAM.”

Use an acquisition/adoption model appropriate to the business. A generic recurring structure is:

`SOM_t = Reach_t × Conversion_t × Retention_t × RevenuePerCustomer_t`

For cohort businesses, explicitly model opening customers + new customers − churned customers = closing customers.

If reach, conversion, retention, or revenue-per-customer parameters are unsupported, **do not fill them with convenient benchmarks**.

A valid conclusion is:

> **SOM is presently not estimable.**
>
> Model structure: knowable.  
> Parameter values: currently unknown.  
> Experiment required: specified.

Report SOM as a percentage of SAM only as an output after building the acquisition/adoption model, never as the input assumption that creates the forecast.

## 12. Conditional modules

Run these only when they are decision-relevant and evidentially supportable.

### Growth / CAGR
Use only when a coherent historical market exists. Every CAGR must state:

- start value/year;
- end value/year;
- geography;
- exact market definition;
- currency;
- nominal vs real treatment;
- inflation/base year when real values are used.

Formula:

`CAGR = (V_end / V_start)^(1/n) - 1`

Do not copy a published CAGR as a forward forecast without decomposing drivers such as population/accounts, penetration, frequency/usage, price, substitution, technology, and regulation.

### Bass/diffusion modeling
Use only when a diffusion model fits the adoption mechanism and enough assumptions can be justified. The existence of a canonical diffusion model does not make its parameters observable for a novel product.

### Reference class
Prefer **3–5 carefully justified analogs**. Include failed/weak analogs where observable to reduce survivorship bias. Compare only attributes that materially affect the forecast.

### Pricing / WTP
Prefer observed purchasing, existing economic sacrifice, and real price experiments. Structured preference methods such as discrete choice/conjoint may be recommended or analyzed when real respondent/experimental data exist. Do not use AI-simulated respondents as WTP evidence.

### Full unit economics
Calculate CAC, retention, payback, LTV, contribution margin, and related measures only from sufficiently grounded inputs. Competitor or industry benchmarks may provide reference ranges but do not become the subject company's observed economics.

### Competitive structure
Go deep when incumbency, switching, channel control, regulatory barriers, network effects, data advantages, supplier power, or buyer power are load-bearing. Always ask:

> If this opportunity is attractive, why have existing firms not already captured it?

### Three-case financial forecast
Run downside/base/upside only when enough load-bearing parameters are `OBSERVED`, `ESTIMATED`, or responsibly `BOUNDED`. Do not create three scenarios from three arbitrary assumption sets merely to make uncertainty look quantified.

## 13. Adversarial research is mandatory

Do not simply append words like “risk” or “criticism” to the same confirmatory queries. Invert the hypothesis.

Seed patterns include:

- `"[category] startup shut down"`
- `"[competitor] churn"`
- `"[product] switched back"`
- `"[problem] not worth paying for"`
- `"[category] failed adoption"`
- `"why we stopped using [category]"`
- `"[competitor] layoffs customers revenue"`
- `"[category] procurement barriers"`
- `"[category] cancellation reasons"`
- `"[solution] cheaper alternative"`
- `"built internally instead of buying [category]"`
- `"couldn't sell [category]"`

Also search for evidence that:

- the problem is rare or tolerable;
- customers prefer the status quo;
- WTP is lower than assumed;
- competitors solve the problem adequately;
- adoption repeatedly failed;
- customers switch back;
- procurement/switching costs dominate benefits;
- acquisition economics are weak;
- regulation blocks entry;
- market growth is slowing;
- internal build or substitutes are improving.

Record meaningful negative searches and contradictory evidence. “No evidence found” is not proof of absence.

## 14. Evidence ledger and evidence burden

Maintain a persistent ledger with stable IDs. Minimum fields:

- claim/input;
- value/range;
- unit;
- epistemic state;
- source and date;
- confidence;
- used-by (crux/TAM/SAM/reachability/economics/etc.);
- contradiction links/notes;
- validation next step.

The final brief must make the **evidence burden** visible. Count load-bearing variables, not every incidental assumption.

At minimum report:

- number of load-bearing variables;
- number that are `ASSUMPTION`;
- number that are `NOT_KNOWABLE_FROM_DESK_RESEARCH`;
- whether any fatal gate depends on either state.

## 15. Synthesis and verdict

The short Decision Brief should answer:

- Is there a credible gap?
- Is there credible economic demand in that gap?
- What market size/range is best supported?
- What is genuinely reachable, and what is not yet estimable?
- Are the economics attractive, or not knowable yet?
- What fatal gate or crux dominates the decision?
- What proportion of load-bearing variables remains assumption/unknown-grade?
- What evidence contradicts the thesis?
- What is the next cheapest discriminating test?

Use one recommendation:

- `PURSUE` — evidence is strong enough for the stated commitment;
- `TEST` — opportunity is promising but a load-bearing uncertainty should be tested before larger commitment;
- `HOLD` — current evidence does not justify the next commitment, but a specific future condition could change the decision;
- `REJECT` — a fatal gate or weight of evidence makes the opportunity unattractive under the stated decision standard.

The recommendation must be relative to the user's actual decision threshold, not a generic startup score.

A valid terminal statement is:

> We cannot yet underwrite this market. We have established X and Y, but Z is the load-bearing unknown. Here is the cheapest evidence that would change the decision.
<!-- PORTABLE:PROTOCOL:END -->

## 16. File-backed state progression

The canonical state files are:

```text
input.json
research-state.json
evidence-ledger.json
outputs/
```

The state progression is deliberately smaller than the report outline:

```text
CLASSIFY
→ CRUXES
→ FATAL_GATES
→ ESTABLISH_MARKET
→ SIZE
→ CONDITIONAL_UNDERWRITING
→ FALSIFY
→ SYNTHESIZE
→ COMPLETE
```

A failed fatal gate can route directly from `FATAL_GATES` or any later phase to `SYNTHESIZE`.

At the start of every move, reopen the state files from disk. Do not rely on prior conversational memory when persisted state exists.

Structured evidence/state must be written **before** final narrative synthesis.

## 17. Research sufficiency

Research sufficiency is decision-relative, not quota-relative.

A study may stop when:

- the decision is already dominated by a failed fatal gate;
- additional desk research is unlikely to change a load-bearing variable;
- the remaining uncertainty is explicitly `NOT_KNOWABLE_FROM_DESK_RESEARCH` and a field test is specified;
- sizing methods have converged sufficiently for the decision;
- the conclusion is robust across reasonable bounds on the remaining assumptions.

Do not keep searching merely to fill a source count or complete every optional module.

## 18. Source quality

Prefer the source closest to the underlying fact:

1. official/statistical/regulatory data;
2. company filings or direct transaction/product evidence;
3. peer-reviewed research;
4. credible industry associations and high-quality proprietary datasets;
5. commercial market research;
6. reputable secondary reporting;
7. community/social evidence;
8. weak or unattributed secondary claims.

Source authority does not eliminate definition risk. Always record geography, population, time period, units, and market definition for material quantitative claims.

Where multiple sources repeat one underlying statistic, treat them as one evidence lineage rather than independent corroboration.

## 19. Methodological basis and limits

The protocol deliberately combines several traditions rather than pretending they form one validated instrument:

- bottom-up market construction and investor underwriting heuristics;
- revealed preference and discrete-choice / conjoint traditions for demand and willingness to pay;
- reference-class forecasting / outside-view reasoning;
- diffusion models such as Bass when appropriate;
- sensitivity analysis and explicit uncertainty;
- standard unit-economic analysis appropriate to the business model.

See [`references/methodology-basis.md`](references/methodology-basis.md) for source notes and limitations.

## 20. Cross-method handoffs

### To Lead User Research

Use [Lead User Research](https://github.com/mattlane66/planning-skills-for-agents-and-humans/tree/main/lead-user-research) when the active crux depends on future-facing trend evidence, advanced users, emerging workarounds, high-benefit needs, or advanced analogs.

Lead User evidence remains evidence. It does not itself establish prevalence, TAM, WTP, unit economics, or a build decision.

### To product planning

When underwriting supports pursuit and the human accepts the opportunity, pass the smallest set of accepted evidence implications into [Planning Skills for Agents and Humans](https://github.com/mattlane66/planning-skills-for-agents-and-humans). Do not automatically convert underwriting claims into product requirements.
