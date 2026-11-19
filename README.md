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

## Read the proposal

- [docs/architecture.md](docs/architecture.md): all 12 sections in Markdown (renders on GitHub, including the ERD)
- [docs/proposal/index.html](docs/proposal/index.html): the designed proposal page; open it in a browser
- [docs/decisions/0001-stack.md](docs/decisions/0001-stack.md): why these four components and not more
- [agents/roster.md](agents/roster.md): the 15 agents, their models, tools and limits
- [docs/questions.md](docs/questions.md): everything needed from the StarsTell team before coding

## Repository layout

```
agents/                    Agent roster; Paperclip agent and skill definitions go here later
docs/                      Architecture, decisions, open questions, proposal page
infra/                     Docker Compose for Paperclip, OpenSEO, Content Service, Postgres (Phase 1)
integrations/
  vedic/                   Vedic Astrology bot adapter   (blocked: waiting for API docs)
  tarot/                   Tarot bot adapter             (blocked: waiting for API docs)
  numerology/              Numerology bot adapter        (blocked: waiting for API docs)
  cms/                     StarsTell CMS adapter         (blocked: waiting for CMS details)
services/content-service/  MCP server and editor web app (Phase 1)
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
