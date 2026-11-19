# 0002: Skill libraries for the agents

- Status: Proposed, awaiting approval
- Date: 19/11/2026

## Context

Four open-source skill libraries were requested for the agents: seomachine, marketingskills, claude-seo and humanizer. Paperclip agents run on the Claude Code runtime and Paperclip supports shared, versioned skills, so these libraries plug in as **agent skills**, not as code inside the Content Service.

## Evaluation (19/11/2026)

| Repo | What it is | Activity | License | Overlap and risk |
|---|---|---|---|---|
| [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) | 29 SEO skills and 20 sub-agents: content briefs, E-E-A-T review, schema, hreflang, sitemap, GEO/AI search, images, technical audits, Google APIs, drift checks. Python helpers in its own runtime | v2.6.2, last commit 15/11/2026, 30,769 stars | MIT | `seo-dataforseo` overlaps OpenSEO. Needs its Python runtime (`/seo setup`) on the agent host |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | 50+ marketing skills: copywriting, copy editing, content strategy, AI SEO, schema, site architecture, competitor profiling, programmatic SEO, CRO, ads, email | v2.14.13, last commit 18/11/2026, 61,339 stars | MIT | CRO, popups, offers, paywalls and urgency-style psychology skills conflict with StarsTell's "never sell fear" rules, so they are not installed for content agents |
| [TheCraigHewitt/seomachine](https://github.com/TheCraigHewitt/seomachine) | A complete Claude Code workspace for SEO blogs: 11 agents (editor, meta creator, internal linker, keyword mapper, headline generator), commands like `/research`, `/write`, `/optimize`, `/scrub`, Python research and scoring modules, WordPress publishing with RankMath/Yoast | Last commit 23/10/2026, 7,633 stars | MIT | Its 26 bundled skills are copies of marketingskills. Its research scripts overlap OpenSEO. WordPress-only publishing |
| [blader/humanizer](https://github.com/blader/humanizer) | Skill that removes 26 signs of AI writing | v4.0.0, 10/11/2026 | MIT | English patterns only; see [humanizing.md](../humanizing.md) |

## Decision

1. **claude-seo** supplies the core SEO skills (brief, content review, schema, hreflang, sitemap, GEO, images, technical audit, drift).
2. **marketingskills** supplies writing and strategy skills (copywriting, copy editing, content strategy, AI SEO, site architecture, competitor profiling). Its conversion and urgency skills are excluded.
3. **seomachine** is used selectively:
   - its `context/` pattern becomes our [context/](../../context/) folder (brand voice, style guide, SEO guidelines, internal link map, target keywords, writing examples), which every agent reads;
   - its agent prompts for meta creation, internal linking, keyword mapping and headline generation are adapted into our agents' instructions;
   - its content scrubber (invisible Unicode and em-dash cleanup) and readability, quality and length scorers run as automated checks;
   - its WordPress publisher and RankMath/Yoast REST snippets are reused **only if the StarsTell CMS is WordPress**.
   Its bundled skill copies and its DataForSEO research scripts are not used (marketingskills and OpenSEO cover them).
4. **humanizer** as decided in [humanizing.md](../humanizing.md).

All four are pinned to exact commits in [skills/manifest.yaml](../../skills/manifest.yaml). OpenSEO stays the single source of keyword and SERP data.

## Safety rules for third-party skills

- **Pinned, never auto-updated.** Upgrades are a reviewed pull request that changes one SHA.
- **Read before install.** Every skill's `SKILL.md` and any script it runs is reviewed before it is enabled for an agent.
- **Least privilege.** A skill is enabled only for the agents listed in the manifest.
- **StarsTell rules win.** When a skill's advice conflicts with the brand voice or the [article spec](../article-spec.md) (for example urgency copy or keyword density targets), the StarsTell context files take priority, and this is stated in each agent's instructions.
- **Attribution kept** in [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md).

## Consequences

- The agent host needs Python for claude-seo and seomachine helpers, in addition to Node for Paperclip.
- Skill count per agent stays small (3 to 6) so instructions don't conflict or bloat context.
- When the CMS is confirmed, the WordPress path is either adopted or dropped.
