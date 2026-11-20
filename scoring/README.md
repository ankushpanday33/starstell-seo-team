# Score gate: SEO, GEO and AEO must each be 90+

No draft goes to the CMS until its own preview page scores **90 or more on SEO, GEO and AEO**. A draft below that goes back to the writer and the SEO Optimizer with the list of failing checks, and is scored again.

## The two repos we evaluated (20/11/2026)

| Repo | What it is | License | Decision |
|---|---|---|---|
| [seryvon-com/seryvon](https://github.com/seryvon-com/seryvon) | Self-hosted, deterministic audit engine: SEO, GEO, GSO, AEO and ASO scores, every criterion explained. Python. Very new (created 16/06/2026, last commit 29/09/2026) | AGPL-3.0 | **Used as the scoring engine**, unmodified, pinned to commit `ab060ed`. Internal use only; if we ever change its code and offer it to people outside StarsTell over a network, AGPL requires publishing those changes |
| [automationbyexperts/seo-geo-aeo-audit](https://github.com/automationbyexperts/seo-geo-aeo-audit) | Not code: a README and examples for a paid cloud service (an Apify Actor). The scoring itself is closed source and runs in their cloud | MIT (docs only) | **Not used as the gate.** It can only crawl public URLs, so it cannot see a draft before approval, and it needs an Apify token. Its 45+ check list is a useful reference, and it could audit live pages after publishing |

## How the gate works

1. The Content Service renders the draft as a real page on a **private preview host**, with its final head tags, schema and images.
2. `score_gate.py` runs Seryvon on that one page with [gate-config.yaml](gate-config.yaml).
3. **Pass** only if SEO, GEO and AEO are each 90+ and each has at least 45% of its criteria measured. A score built on too few checks does not count.
4. Fail: the failing checks go back to the writer and SEO Optimizer; the draft is re-scored after the fix. Every run is saved with the article.

Seryvon refuses private and loopback addresses on purpose. The wrapper allows exactly the hosts in `STARSTELL_PREVIEW_HOSTS` (default `127.0.0.1`), nothing else.

### Article gate vs site run

Some Seryvon criteria describe the whole site or only exist after publishing, so a draft page can never pass them. [gate-config.yaml](gate-config.yaml) gives them weight 0 for the article gate and lists each one with its reason:

- **Preview only:** HTTPS, sitemap (the live site has both).
- **Site and brand, owned by the website team:** About page, StarsTell in Wikidata / Knowledge Graph, `sameAs` links to official StarsTell profiles, internal link graph.
- **After publishing:** backlinks, domain authority, Search Console position and CTR.

These are checked by a **weekly site run** on the live starstell.com with Seryvon's defaults (`--config ''`), and that run is expected to reach 90+ as well.

## Run it

```bash
pip install -r scoring/requirements.txt
```

```bash
python scoring/score_gate.py http://127.0.0.1:8767/blog/life-path-number-7/ --out report.json
```

Exit code `0` passed, `1` blocked, `2` could not score (also blocks).

| Setting | Default | Meaning |
|---|---|---|
| `STARSTELL_SCORE_THRESHOLD` | `90` | Minimum for each of SEO, GEO, AEO |
| `STARSTELL_MIN_COVERAGE` | `0.45` | Minimum share of a pillar's criteria that must be measured |
| `STARSTELL_PREVIEW_HOSTS` | `127.0.0.1` | Private hosts the gate may score |

Optional Seryvon keys that raise coverage: `PSI_API_KEY` (Core Web Vitals), `GSC_SERVICE_ACCOUNT` (Search Console), `OPENAI_API_KEY` / `GEMINI_API_KEY` / `PERPLEXITY_API_KEY` / `ANTHROPIC_API_KEY` (AI citation tracking, GEO), `DATAFORSEO_API_KEY` (authority). See the main README's credentials table.

## Proof on the life path 7 example

| Run | SEO | GEO | AEO | Result |
|---|---:|---:|---:|---|
| English, first draft, Seryvon defaults | 88.4 | 68.4 | 53.2 | Blocked |
| English, after fixes, gate config | 100 | 100 | 100 | Passed |
| Hindi | 100 | 93.2 | 100 | Passed |
| Tamil (summary only, full body not yet written) | 91.4 | 100 | 84.8 | Blocked |

Fixes that moved English from blocked to passed: a direct-answer first paragraph, a Mulank vs Bhagyank comparison table, `DefinedTermSet` schema, the reviewer's structured credentials, links to outside sources, and complete Twitter card tags. Reports are in [examples/life-path-number-7/scores](../examples/life-path-number-7/scores/).

Known limits: GEO coverage is about 54% until AI citation keys are added; Seryvon's entity-density heuristic reads lower on Devanagari text (Hindi GEO 93.2 for that reason).
