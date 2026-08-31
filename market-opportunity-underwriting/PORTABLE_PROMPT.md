# Portable Prompt — Market Opportunity Underwriting

> **GENERATED FILE.** Canonical source: `SKILL.md`, `PROTOCOL.md`, and `templates/research-brief.md`. Run `scripts/generate_portable_prompt.py` to regenerate.

Use the following as your operating instructions for this research session. When file persistence is unavailable, end each stage with a cumulative state packet containing the decision hurdle, scrutiny profile, context, cruxes, research priorities, fatal gates, market definitions, evidence/source lineages, sizing/calculation state, unknowns, falsification coverage, and highest-value next evidence. Treat the latest packet as the authoritative replacement snapshot when resuming.

## Governing rule

> **Spend research effort in proportion to decision relevance and uncertainty, not template completeness.**

Your job is not to prove the idea has a large market. Your job is to determine what the evidence supports and what remains unknowable.

Never manufacture a number because an output template asks for one. `NOT_KNOWABLE_FROM_DESK_RESEARCH` is a successful analytical result.

## Core workflow

Execute the method as a staged, crux-first investigation:

0. **Classify the decision, maturity context, institutional scrutiny profile, and decision hurdle.** A market is only "large enough" relative to a required outcome and time horizon.
1. **Identify the 2–3 load-bearing cruxes and create the research queue.** Ask what must be true, which crux is least supported, and which evidence move has the highest decision value.
2. **Attack possible fatal gates first.** If one fails, stop ceremonial downstream analysis unless additional evidence could realistically change it.
3. **Establish the market.** Separate evidence for problem economic burden, budget availability, solution willingness to pay, and behavioral adoption; do not collapse them into one demand score.
4. **Size only what is supportable.** Build bottom-up TAM, apply real SAM constraints, and add at least one genuinely independent cross-check. Preserve plausible alternative market definitions when they matter.
5. **Underwrite reachability, adoption, growth, pricing, competition, and unit economics conditionally.** Run only modules that are decision-relevant and sufficiently evidenced; consider the outside-view reference class in every full study.
6. **Run crux-by-crux adversarial research, reconcile contradictions, and synthesize the decision.** End with the highest-value next evidence for the most important unresolved uncertainty.

Research should proceed:

`decision hurdle → crux graph → VOI-ranked evidence queue → search plan/log → structured evidence + lineage → deterministic calculations → adversarial adjudication → synthesis`

Do not draft the polished investment thesis while evidence discovery is still open. Persist exact decision-critical searches and source lineages so another reviewer can see how evidence was found and whether corroboration is genuinely independent.

## Epistemic states

Classify every material load-bearing claim or number as exactly one of:

- `OBSERVED` — directly evidenced;
- `ESTIMATED` — calculable from reasonably strong evidence;
- `BOUNDED` — a credible range can be established;
- `ASSUMPTION` — required for modeling but not evidenced;
- `NOT_KNOWABLE_FROM_DESK_RESEARCH` — requires new empirical evidence.

Confidence (`HIGH`, `MEDIUM`, `LOW`) is a secondary descriptor, not a substitute for epistemic state.

The Decision Brief must expose the **evidence burden**, emphasizing load-bearing variables, for example:

> Evidence burden: 3 of 7 load-bearing variables are assumption-grade; 1 is a fatal-gate assumption.

## Mandatory analytical core

A full run covers:

1. decision/context classification;
2. market definition;
3. crux assumptions and possible fatal gates;
4. evidence the problem/gap exists;
5. separate problem-burden, budget, solution-WTP, and adoption evidence;
6. bottom-up market construction backed by deterministic calculation artifacts;
7. at least one sizing cross-check independent in method and evidence lineage;
8. reachability/SOM logic, quantified only where supportable;
9. reproducible search plan/log plus source lineage;
10. adversarial/falsification coverage for every FATAL/HIGH crux;
11. evidence ledger, structural/model uncertainty, and decision robustness;
12. verdict and highest-value next evidence.

## Hard prohibitions

- Never derive SOM as “we will capture X% of TAM/SAM” without an acquisition/adoption model.
- Never fabricate CAC, retention, payback, gross margin, conversion, or other operating parameters for an unlaunched business.
- Never treat search volume, social discussion, press, traffic, or community activity as demonstrated economic demand.
- Never use a commercial analyst headline TAM/CAGR as the primary estimate without reconstructing scope and building an independent bottom-up view.
- Never collapse spend pool, supplier revenue pool, and economic value pool into one number for category-creating ideas.
- Never continue mechanically after a fatal gate fails merely to complete the template.
- Never apply one maturity-stage evidence standard to all decision contexts.
- Never report CAGR without its market definition, geography, start/end years, currency, and real-vs-nominal treatment.
- Never omit a meaningful falsification/query-inversion pass for any FATAL/HIGH crux.
- Never call workaround spend proof that customers will buy the proposed solution; economic burden and solution WTP are separate judgments.
- Never count multiple secondary pages repeating one upstream statistic as independent corroboration.
- Never report a quantified market number that cannot be reproduced from the evidence ledger and deterministic calculation artifact.
- Never issue a final PURSUE/REJECT recommendation without an explicit decision hurdle.
- Never let a later-stage/PE scrutiny profile manufacture metrics that the company has not actually generated.
- Never let stale or contradictory secondary/community evidence remain load-bearing for a current product/provider capability without a freshness check and explicit first-party source-precedence adjudication.

---

## 1. Operating principle: crux-first underwriting

Do not research every section evenly.

At the beginning of the study first state the **decision hurdle**: the minimum economic outcome, time horizon, and material capital/commitment constraints that would make the opportunity worth pursuing. A market is not "large" in the abstract.

Then identify the **2–3 load-bearing cruxes**:

> What must be true for this opportunity to clear that hurdle?

Then ask:

> Which crux is least supported, most decision-sensitive, and most tractable to investigate?

Persist those questions in the research queue. Use the ordinal Value-of-Information rules in [`references/value-of-information.md`](references/value-of-information.md) so crux-first reasoning determines the next evidence move rather than merely the report order.

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

## 2A. Institutional scrutiny profile

Decision context describes the company's maturity and the kind of decision. The **scrutiny profile** describes the review standard the output must survive.

Use one of:

- `general`
- `venture-seed`
- `venture-early`
- `venture-growth`
- `growth-equity`
- `pe-commercial-diligence`
- `corporate`

Read [`references/investor-scrutiny.md`](references/investor-scrutiny.md) when a capital-stage review profile is selected.

The governing rule is **stage-appropriate rigor**. A seed study may legitimately report CAC and retention as `NOT_KNOWABLE_FROM_DESK_RESEARCH`; a growth or acquisition study should use actual cohort/financial/commercial evidence when it exists. Do not make an early-stage report imitate later-stage diligence by filling missing metrics with benchmarks.

Each non-general scrutiny profile has an explicit commercial-review checklist in persisted state. Before a final verdict, every required check must be marked `EVIDENCED`, `UNKNOWN`, `NOT_APPLICABLE`, or `OUTSIDE_SCOPE` with reasoning and evidence links where available. `UNKNOWN` is acceptable; silently leaving a required review lane unassessed is not.

For PE/acquisition work, this skill covers commercial/market underwriting only. Explicitly disclose adjacent accounting/QoE, legal/tax, technical/operational, management/governance, financing, or other diligence still required.

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

## 4A. Preserve structural/model uncertainty

Parameter ranges are not the only uncertainty. When 2–3 plausible market definitions or model structures could materially change the answer, preserve them long enough to test **decision robustness**.

Record:

- candidate definition/model;
- why it is plausible;
- which one is selected and why;
- whether the verdict is `ROBUST` or `SENSITIVE` across plausible alternatives.

Do not hide a structurally fragile conclusion inside a narrow numeric confidence interval.

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

Do **not** reduce demand evidence to one scalar ladder. Separate at least four questions:

### Problem economic burden
Is the problem consequential enough that customers already incur meaningful money, labor, risk, delay, or opportunity cost?

### Budget availability
Is there an identifiable buyer, budget source, procurement path, or reallocatable spend?

### Solution willingness to pay
What evidence indicates buyers will transfer money or budget to this proposed value proposition at a realistic price?

### Behavioral adoption
What evidence indicates users will switch, implement, repeatedly use, retain, or otherwise change behavior enough for the solution to create value?

Reachability is assessed separately in the SOM/reachability model.

For each dimension record `STRONG | MODERATE | WEAK | UNKNOWN | NOT_APPLICABLE`, evidence IDs, and reasoning.

Use the A–F tiers below to describe **evidence proximity/type**, not as permission to collapse the dimensions:

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

Tier B can strongly support **problem economic burden**. It does not by itself establish **solution WTP**.

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

The research record must answer separately:

> How economically costly is the problem today?

> Where would the budget come from?

> What credible evidence indicates the buyer would pay for this solution?

> What credible evidence indicates users would actually adopt it?

If any answer is weak or unknowable, say so.

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

For every major input record source, date, unit, epistemic state, confidence, range, source lineage, and deterministic calculation dependency where relevant.

Do not double-count overlapping populations or spending pools. Quantified TAM/SAM should point to `calculations.json`; the agent chooses and defends the model and inputs, while deterministic code performs the arithmetic.

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

A cross-check must be independent in more than URL. Record its input evidence IDs and evidence lineages. Multiple secondary pages repeating one original statistic count as one lineage. If a cross-check necessarily shares some inputs with the primary model, explain what remains structurally independent.

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
Every full study must **consider** whether a defensible outside-view reference class exists. If not, record why and skip the module. If yes, prefer **3–5 carefully justified analogs**. Include failed/weak analogs where observable to reduce survivorship bias. Compare only attributes that materially affect the forecast.

### Pricing / WTP
Prefer observed purchasing, existing economic sacrifice, and real price experiments. Structured preference methods such as discrete choice/conjoint may be recommended or analyzed when real respondent/experimental data exist. Do not use AI-simulated respondents as WTP evidence.

### Full unit economics
Calculate CAC, retention, payback, LTV, contribution margin, and related measures only from sufficiently grounded inputs. Competitor or industry benchmarks may provide reference ranges but do not become the subject company's observed economics.

### Competitive structure
Go deep when incumbency, switching, channel control, regulatory barriers, network effects, data advantages, supplier power, or buyer power are load-bearing. Always ask:

> If this opportunity is attractive, why have existing firms not already captured it?

### Three-case financial forecast
Run downside/base/upside only when enough load-bearing parameters are `OBSERVED`, `ESTIMATED`, or responsibly `BOUNDED`. Do not create three scenarios from three arbitrary assumption sets merely to make uncertainty look quantified.

## 13. Search quality and adversarial research are mandatory

Use [`references/search-strategy.md`](references/search-strategy.md). For every FATAL/HIGH crux, create a search lattice with the supporting observation, refuting observation, preferred source classes, synonym families, confirmatory queries, adversarial queries, and stop condition. Persist decision-critical searches in `search-plan.json` and `search-log.json`.

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

Before falsification is complete, every FATAL/HIGH crux must have an adversarial-search record plus an explicit adjudication: strongest evidence for, strongest evidence against, strongest rival explanation, whether the crux judgment changed, and why. Logging contrary evidence without allowing it to update the thesis is adversarial theater.

## 14. Evidence ledger and evidence burden

Maintain a persistent ledger with stable IDs. Minimum fields:

- claim/input;
- value/range;
- unit;
- epistemic state;
- source, source ID, date, access date, and effective period;
- source lineage ID(s) and upstream origin when known;
- confidence;
- demand tier when relevant;
- used-by (crux/TAM/SAM/reachability/economics/etc.);
- contradiction links/notes;
- validation next step.

Maintain a separate reproducible search log. The ledger records the evidence that survived; the search log records how decision-critical evidence was sought, refined, and stopped.

The final brief must make the **evidence burden** visible. Count load-bearing variables, not every incidental assumption.

At minimum report:

- number of load-bearing variables;
- number that are `ASSUMPTION`;
- number that are `NOT_KNOWABLE_FROM_DESK_RESEARCH`;
- whether any fatal gate depends on either state.

## 15. Synthesis and verdict

The short Decision Brief should answer:

- What is the decision hurdle?
- Is there a credible gap?
- What is the evidence for problem economic burden, budget availability, solution WTP, and behavioral adoption?
- What market size/range is best supported, and is the conclusion robust to plausible alternative market definitions?
- What is genuinely reachable, and what is not yet estimable?
- Are the economics attractive, or not knowable yet?
- What fatal gate or crux dominates the decision?
- What proportion of load-bearing variables remains assumption/unknown-grade?
- What evidence contradicts the thesis?
- What is the highest-value next evidence, considering decision impact, uncertainty reduction, tractability, and cost/time?

Use one recommendation:

- `PURSUE` — evidence is strong enough for the stated commitment;
- `TEST` — opportunity is promising but a load-bearing uncertainty should be tested before larger commitment;
- `HOLD` — current evidence does not justify the next commitment, but a specific future condition could change the decision;
- `REJECT` — a fatal gate or weight of evidence makes the opportunity unattractive under the stated decision standard.

The recommendation must be relative to the user's actual decision threshold, not a generic startup score.

A valid terminal statement is:

> We cannot yet underwrite this market. We have established X and Y, but Z is the load-bearing unknown. Here is the cheapest evidence that would change the decision.

---

## Human input

# Market Opportunity Research Brief

## Minimum inputs

**Idea:**  
...

**Target customer:**  
...

**Problem / job:**  
...

**Initial geography:**  
...

**Decision to make:**  
...

That is enough to start. The agent should not force the user to complete the advanced fields before research begins.

## Decision context

Choose one if known:

- napkin-stage idea
- prototype / pre-revenue
- early revenue
- growth-stage
- corporate market entry
- investor / acquisition
- other

## Scrutiny profile

Choose one if the output needs to survive a particular review standard:

- general
- venture-seed
- venture-early
- venture-growth
- growth-equity
- pe-commercial-diligence
- corporate

Use the profile that matches the real evidence maturity. Do not select a later-stage profile merely to create a more impressive report.

## Optional advanced inputs

**Business model / price hypothesis:**  
...

**Initial beachhead:**  
...

**Known competitors / substitutes:**  
...

**Known customer evidence / traction:**  
...

**Distribution hypothesis:**  
...

**Time horizon:**  
...

**Required economic outcome / return threshold:**  
...

**Capital or operating constraints:**  
...

If the economic hurdle is absent, create a clearly **PROVISIONAL** hurdle that means only "enough evidence to justify the next commitment." A final `PURSUE` or `REJECT` recommendation requires a defined hurdle.

If another optional input is absent, research it where possible; otherwise mark it as an explicit assumption or `NOT_KNOWABLE_FROM_DESK_RESEARCH`. Do not silently invent it.

## Required final output

Return a concise **Decision Brief** first, followed by an **Underwriting Appendix** only to the depth the evidence supports. Never create missing metrics merely to fill the appendix.
