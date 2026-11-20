# StarsTell SEO Team

An AI SEO and content marketing department for StarsTell. Fifteen specialised AI agents research keywords, plan content, write articles grounded in StarsTell's own Vedic Astrology, Tarot and Numerology bots, check facts, optimise for search, and publish to the StarsTell site after a person approves each article.

> **Status: architecture proposal, awaiting approval.** No integration code exists yet. Implementation starts only after the architecture is approved and the API documentation for the three StarsTell bots is received. See [docs/questions.md](docs/questions.md).

## The stack in one line

**Paperclip** runs the team, **OpenSEO** supplies search data, one **StarsTell Content Service** (built here) connects the bots and the CMS, and **PostgreSQL** stores it all. CrawlSEO is deferred to Phase 4. n8n is not used.

| Component | Role | Source |
|---|---|---|
| [Paperclip](https://github.com/paperclipai/paperclip) | Org chart, tasks, approval stages, budgets, routines, secrets, activity log | MIT, self-hosted |
| [OpenSEO](https://github.com/every-app/open-seo) | Keywords, SERPs, competitors, backlinks, rank tracking, Search Console, GA4, AI visibility (MCP) | MIT, self-hosted, DataForSEO pay per call |
| StarsTell Content Service | Bot adapters, article store, claims, CMS publish gate, cost ledger, dashboard | Built in this repo |
| PostgreSQL | One instance, three databases | Self-hosted or managed |
| [Seryvon](https://github.com/seryvon-com/seryvon) | Score gate: SEO, GEO and AEO must each be 90+ before the CMS | AGPL-3.0, self-hosted, unmodified |

## See it working

A live 3D agent office built on [The Roving Office](https://github.com/atlassian-labs/roving-office): six departments, every agent seated at its own desk, walking to another department only to hand over work or ask a question. Details in [visualizer/README.md](visualizer/README.md).

![The StarsTell agent office](visualizer/office-screenshot.png)

Needs Node 18 or newer and git. No credentials or `.env` are needed for this part.

```bash
git clone --recurse-submodules https://github.com/ankushpanday33/starstell-seo-team.git
```

```bash
cd starstell-seo-team
```

```bash
node visualizer/starstell-office.mjs
```

Then open http://127.0.0.1:8090/office/STAR-7EAM. Already cloned without submodules? Run `git submodule update --init` first. A step-by-step example with each step's output and the published blog in 7 languages is in [visualizer/walkthrough.html](visualizer/walkthrough.html).

## Score gate: 90+ or it does not publish

Every draft is scored by [Seryvon](https://github.com/seryvon-com/seryvon) on a private preview page. **SEO, GEO and AEO must each reach 90** or the draft goes back for fixes and never reaches the CMS. See [scoring/README.md](scoring/README.md).

## A finished example

[examples/life-path-number-7](examples/life-path-number-7/) is one blog, "Life path number 7", taken end to end by Claude playing every agent: the published page in 7 languages, 4 images with alt text, meta tags and schema, and every step's output from keyword research to the approval queue.

## Credentials and `.env`

This repository is public, so **real values never go in it**. Copy the template, fill it in on the server, and keep it there:

```bash
cp .env.example .env
```

`.env` is git-ignored. In production the same values go into Paperclip's secret store or the server's environment instead.

**What you need today:** nothing. The agent office visualizer runs without any keys.

**What the full system needs, by phase:**

| Variable | Needed in | What it is | Where to get it |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | Phase 1 | Runs the Claude agents through Paperclip | console.anthropic.com > API keys |
| `DATABASE_URL` | Phase 1 | PostgreSQL for the Content Service | Your Postgres server or managed database |
| `DATAFORSEO_API_KEY` | Phase 1 | Keyword, SERP, competitor and rank data for OpenSEO (pay per call) | dataforseo.com > API access |
| `AUTH_MODE` | Phase 1 | OpenSEO sign-in mode; `password` for a self-hosted Docker install | Set it yourself |
| `BETTER_AUTH_SECRET` | Phase 1 | OpenSEO session secret, also encrypts stored Google tokens (32+ random characters) | Generate it yourself |
| `BETTER_AUTH_URL` | Phase 1 | Public URL of the OpenSEO install | Your hosting |
| `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` | Phase 1 | Lets OpenSEO read Search Console and GA4 | Google Cloud Console > Credentials > OAuth client; a Search Console owner then grants access |
| `STARSTELL_VEDIC_API_URL`, `STARSTELL_VEDIC_API_KEY` | Phase 2 | Vedic Astrology bot (placeholder names) | StarsTell team, with the API docs |
| `STARSTELL_TAROT_API_URL`, `STARSTELL_TAROT_API_KEY` | Phase 2 | Tarot bot (placeholder names) | StarsTell team |
| `STARSTELL_NUMEROLOGY_API_URL`, `STARSTELL_NUMEROLOGY_API_KEY` | Phase 2 | Numerology bot (placeholder names) | StarsTell team |
| `GOOGLE_AI_API_KEY`, `OPENAI_API_KEY` | Phase 2 | The two image models tested; only the winner's key stays | Google AI Studio / OpenAI platform |
| `STARSTELL_CMS_API_URL`, `STARSTELL_CMS_API_KEY` | Phase 3 | Publishing to the StarsTell site (placeholder names) | StarsTell web team, once the CMS is confirmed |
| `INDEXNOW_KEY` | Phase 3 | Tells search engines about new pages; any random 8 to 128 character string, also served at `/<key>.txt` | Generate it yourself |
| `PSI_API_KEY` | Phase 1 (score gate) | Core Web Vitals in Seryvon's SEO score | Google Cloud Console > PageSpeed Insights API |
| `GSC_SERVICE_ACCOUNT` | Phase 3 (site run) | Search Console data in Seryvon's weekly site run | Google Cloud service account added to the Search Console property |
| `GEMINI_API_KEY`, `PERPLEXITY_API_KEY` | Optional (score gate) | AI citation tracking, raises GEO coverage (Seryvon also uses `OPENAI_API_KEY` and `ANTHROPIC_API_KEY`) | Google AI Studio / Perplexity |
| `STARSTELL_SCORE_THRESHOLD`, `STARSTELL_MIN_COVERAGE`, `STARSTELL_PREVIEW_HOSTS` | Score gate | Gate rules; defaults `90`, `0.45`, `127.0.0.1` | Set them yourself |
| `PORT`, `SPEED` | Optional | Port and speed of the agent office visualizer | Defaults: `8090`, `1` |

Variables marked "placeholder" are renamed if the StarsTell API or CMS documentation calls for it. Paperclip itself is set up with `npx paperclipai onboard` and keeps its own configuration.

## Read the proposal

- [docs/architecture.md](docs/architecture.md): all 12 sections in Markdown (renders on GitHub, including the ERD)
- [docs/proposal/index.html](docs/proposal/index.html): the designed proposal page; open it in a browser
- [docs/decisions/0001-stack.md](docs/decisions/0001-stack.md): why these four components and not more
- [agents/roster.md](agents/roster.md): the 15 agents, their models, tools and limits
- [docs/article-spec.md](docs/article-spec.md): URL, meta title, meta description, meta tags, headings, images, alt text, keywords for every article
- [docs/multilingual.md](docs/multilingual.md): every blog in 7 languages (English, Hindi, Hinglish, Marathi, Tamil, Telugu, Bengali), so 7 links
- [docs/images.md](docs/images.md): 3 to 5 generated images per blog, alt text in every language
- [docs/humanizing.md](docs/humanizing.md): humanizer skill plus an Indic style guide; what IndicLLMSuite is and is not used for
- [docs/decisions/0002-skill-libraries.md](docs/decisions/0002-skill-libraries.md): how claude-seo, marketingskills, seomachine and humanizer are used; pinned in [skills/manifest.yaml](skills/manifest.yaml)
- [context/](context/): brand voice, style guide and SEO rules every agent reads first
- [docs/competitor-research.md](docs/competitor-research.md): how AstroTalk, AstroSage, Astroyogi, InstaAstro, AstroTak and Drik Panchang are studied before each article
- [docs/questions.md](docs/questions.md): everything needed from the StarsTell team before coding

## Repository layout

```
agents/                    Agent roster; Paperclip agent and skill definitions go here later
context/                   Brand voice, style guide, SEO rules, keyword and link maps read by every agent
skills/manifest.yaml       Third-party skills pinned to exact commits, mapped to agents
docs/                      Architecture, decisions, open questions, proposal page
infra/                     Docker Compose for Paperclip, OpenSEO, Content Service, Postgres (Phase 1)
integrations/
  vedic/                   Vedic Astrology bot adapter   (blocked: waiting for API docs)
  tarot/                   Tarot bot adapter             (blocked: waiting for API docs)
  numerology/              Numerology bot adapter        (blocked: waiting for API docs)
  cms/                     StarsTell CMS adapter         (blocked: waiting for CMS details)
services/content-service/  MCP server and editor web app (Phase 1)
scoring/                   Score gate: Seryvon wrapper and gate config (SEO, GEO, AEO 90+)
.env.example               Variable names only, never values
```

## Ground rules

1. **No invented integrations.** Endpoints, parameters and response shapes come from StarsTell's documentation, never from guesses.
2. **No secrets in this repo.** Keys live in Paperclip secrets or server environment variables. `.env` is git-ignored.
3. **A person approves every article.** Festival, panchang, muhurat and remedy content also needs SME astrologer sign-off.
4. **Brand voice is enforced.** Name the astrological mechanism, tie outcomes to effort, never guarantee results, never sell fear.

## Roadmap

| Weeks | Phase | Done when |
|---|---|---|
| 0 to 1 | Discovery | Every integration is documented |
| 1 to 2 | Foundation | An agent can save a CMS draft |
| 2 to 4 | First pipeline | 5 drafts reach human approval |
| 5 to 7 | Publish and measure | Approved posts go live in one click |
| 8 to 10 | Grow | The weekly report runs on its own |

---

Confidential | Hungama Digital Media Entertainment Pvt. Ltd.
