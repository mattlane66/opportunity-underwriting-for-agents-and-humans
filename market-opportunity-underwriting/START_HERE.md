# Start Here — Market Opportunity Underwriting

The easiest way to use this methodology is intentionally simple.

## Pick the path that matches your environment

| You are using | Best path | Setup |
| --- | --- | --- |
| ChatGPT, Claude, or Gemini with a research/deep-research mode | **Portable research run** | Turn on the product's research mode, attach or paste `PORTABLE_PROMPT.md`, then provide the five inputs below |
| A persistent ChatGPT/Claude/Gemini project or workspace | **Portable + state packet** | Keep `PORTABLE_PROMPT.md` available and preserve the latest cumulative state packet between runs |
| Codex, Claude Code, Gemini CLI, or another repo/file-capable agent | **Canonical file-backed skill** | Give the agent this repo and ask it to read `market-opportunity-underwriting/SKILL.md`; use the initializer/validator scripts |
| A team running repeated studies | **Repo + CI** | Use the file-backed path and preserve study folders as reviewable artifacts |

If you are unsure, use the first row.

## The five inputs

You do not need to prepare a market model.

```text
Idea:
...

Target customer:
...

Problem / job:
...

Initial geography:
...

Decision to make:
...
```

Optional context can improve the result: business model, price hypothesis, current traction, known competitors, distribution hypothesis, capital constraints, and the economic hurdle that would make the opportunity worth pursuing.

## Fastest path: research-capable chat

1. Open a new chat.
2. Turn on the product's **research / deep research** capability if it has one. Use ordinary web search only when a deeper research mode is unavailable.
3. Attach `PORTABLE_PROMPT.md` if file upload is supported. Otherwise paste its contents.
4. Paste the five inputs above.
5. Add one sentence: **"Run this as a skeptical underwriting study. Do not fill unknowns merely to complete the report."**
6. Review the research plan before it runs, if the product shows one. Make sure it attacks the 2–3 cruxes and possible fatal gates first rather than proposing a generic market report.
7. Run the research.
8. Read the **Decision Brief** first. Open the appendix only when you need the audit trail.

For long studies, do not rely on conversational memory alone. Preserve the latest cumulative state packet and supply it when resuming.

## Best-quality path: file-capable agent

From the repository root:

```bash
python market-opportunity-underwriting/scripts/init_study.py \
  --workspace research/my-opportunity \
  --idea "..." \
  --customer "..." \
  --problem "..." \
  --geography "..." \
  --decision "Should we pursue this?" \
  --context napkin-stage
```

Then tell the agent:

```text
Read market-opportunity-underwriting/SKILL.md and run the Market Opportunity
Underwriting workflow against research/my-opportunity. Reopen persisted state
before every research move. Use the search plan/log and evidence lineage
contracts. Run deterministic calculations and validation before synthesis.
```

Inspect the next move at any time:

```bash
python market-opportunity-underwriting/scripts/next_research_move.py research/my-opportunity
```

Validate the study:

```bash
python market-opportunity-underwriting/scripts/validate_study.py research/my-opportunity
```

## Investment-committee review mode

If the work will be reviewed by investors, tell the agent the scrutiny profile when known:

- `venture-seed`
- `venture-early`
- `venture-growth`
- `growth-equity`
- `pe-commercial-diligence`
- `corporate`
- `general`

Do **not** select a later-stage profile just to make a report look more rigorous. Later-stage profiles require actual operating evidence rather than invented metrics.

## Product-specific notes — current as of 2026-08-31

- **ChatGPT:** Deep research supports uploaded files, public-web research, selectable sources, and a reviewable research plan. If your workspace supports reusable Skills, the repo-backed skill can also be installed rather than pasted each time.
- **Claude:** Research performs multi-step web research with citations; web search must be enabled for Research.
- **Gemini:** Deep Research supports file uploads and produces an editable research plan before the report.
- **Codex:** prefer the canonical repo-backed skill rather than the portable prompt.

Product UI and availability change. If a named research mode is unavailable, use the generic path: enable the strongest web-research capability available, provide the portable prompt, and require citations plus the cumulative state packet.

## What not to do

Do not ask:

> "Give me the TAM for X."

Do not begin by pasting a giant list of market-report numbers.

Do not ask the model to produce year-5 SOM, CAC, or retention when there is no evidence capable of identifying those values.

Give it the business question. Let the skill decide what evidence is needed.
