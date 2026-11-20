# The StarsTell blog crew (crewAI)

The AI team that produces one blog, written with [crewAI](https://github.com/crewAIInc/crewAI) (MIT, pinned to 1.15.44). 17 agents from [agents/roster.md](../agents/roster.md) work through one **crewAI Flow** per blog and stop at human approval.

```
research -> brief -> knowledge -> English draft -> fact check --(claims fail)--> fix claims --+
                                                       |   ^-------------------------------+
                                                       |   (after 2 rounds: escalate to people)
                                                       v
                         6 languages + image plan (in parallel) -> SEO pass with score gate -> editor -> awaiting human approval
```

## Who does what

| Step | crewAI agents | Model | Output (validated) |
|---|---|---|---|
| Research | Keyword Research, Competitor Intel | Sonnet 5.5 | `KeywordPlan`, `GapNote` |
| Brief | Content Brief | Sonnet 5.5 | `Brief` |
| Knowledge | Vedic, Tarot or Numerology Research (StarsTell bot tool) | Sonnet 5.5 | knowledge notes, each marked bot or model knowledge |
| Draft | Senior Blog Writer | Opus 5.5 | `Article` (English) |
| Fact check | Fact Checker | Opus 5.5 | `ClaimsReport`; any failed claim loops back to the writer |
| Languages | Hindi, Hinglish, Marathi, Tamil, Telugu, Bengali Writers (run in parallel) | Opus 5.5 | 6 `Article`s |
| Images | Visual Designer | Sonnet 5.5 | `ImagePlan` (3 to 5 images, alt text in 7 languages) |
| SEO + gate | SEO Optimizer | Sonnet 5.5 | each `Article`, re-done until it passes the gate |
| Final read | Senior Editor | Opus 5.5 | approve to a person, or send back |

## The checks are code, not prompts

crewAI **task guardrails** run after a task and send it back with feedback until it passes (up to 3 retries):

- **`article_spec`** on every article: title and description lengths, keyword placement, slug, 40 to 60 word lead, no skipped headings, 700+ words, a comparison table, outside sources, 3+ FAQs, defined terms, no banned words.
- **`score_gate`** on the SEO step: the article is rendered as its real page, served on 127.0.0.1 and scored by Seryvon. **SEO, GEO and AEO must each be 90+** ([scoring/README.md](../scoring/README.md)).
- The **fact-check loop** is a Flow router: failed claims go back to the writer; after 2 rounds a person is asked.

## Where crewAI sits next to Paperclip

- **Paperclip** stays the management layer: org chart, schedules, budgets, approvals, audit log. A Paperclip task (ST-144) starts one crew run, and Paperclip's approval is the only way to publish.
- **crewAI** is how one blog is produced: the agents, their order, the loops and the checks, as versioned, testable code.
- `publish` refuses to run without a Paperclip approval id, a run that ended at `awaiting_human_approval`, and all 7 language versions. The CMS adapter is written once the CMS is confirmed.

## Run it

```bash
pip install -r crew/requirements.txt
```

Check the whole team and flow without calling any model (draws `crew/out/flow.html`):

```bash
cd crew && python -m starstell_crew.run produce --task ST-144 --topic "Life path number 7" --vertical numerology --dry-run
```

Real run (needs `ANTHROPIC_API_KEY`; `SERYVON_PYTHON` for the score gate; `OPENSEO_MCP_URL` for live SEO data):

```bash
cd crew && python -m starstell_crew.run produce --task ST-144 --topic "Life path number 7" --vertical numerology
```

```bash
cd crew && python -m starstell_crew.run publish --task ST-144 --approval-id <paperclip approval id>
```

Tests (no model calls; runs the real score gate too when `SERYVON_PYTHON` is set):

```bash
python crew/tests/test_offline.py
```

## Not connected yet

| Piece | Until then |
|---|---|
| StarsTell bots | The bot tool answers "not connected" and the knowledge agent marks its notes as model knowledge, which the fact checker then checks |
| OpenSEO | Research agents work from model knowledge and say "no volumes" |
| Image model | The Visual Designer outputs prompts and alt text, not images |
| CMS | `publish` stops before sending anything |
