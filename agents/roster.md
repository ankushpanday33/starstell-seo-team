# Agent roster

Fifteen agents plus the human board. Each becomes a Paperclip agent with its own role, reporting line, budget and skill set. Models are a starting point and will be tuned on measured cost and quality: Opus 5.5 where judgement or writing matters, Sonnet 5.5 for research, Haiku 5.5 for mechanical steps.

| # | Agent | Team | Model | Tools it can use | Produces | Cannot do |
|---|---|---|---|---|---|---|
| 0 | Head of SEO | Leadership | Opus 5.5 | OpenSEO read, Content Service read, Paperclip tasks | Monthly plan, approved opportunities, weekly report | Publish, edit drafts |
| 1 | Keyword Research | SEO Research | Sonnet 5.5 | OpenSEO keyword and SERP tools | Scored keywords and clusters | Create articles |
| 2 | Competitor Intelligence | SEO Research | Sonnet 5.5 | OpenSEO domain, SERP and backlink tools, web fetch | Monthly keyword gap vs watched competitors, per-article top 10 study, gap note ([playbook](../docs/competitor-research.md)) | Write content, copy competitor text |
| 3 | Search Intent | SEO Research | Sonnet 5.5 | OpenSEO SERP tools | Format, questions, snippet targets | Write content |
| 4 | Content Strategist | SEO Research | Opus 5.5 | Content Service clusters, OpenSEO saved keywords | Calendar, pillar map, cannibalization check | Publish |
| 5 | Vedic Astrology Research | Domain Knowledge | Sonnet 5.5 | `vedic_*` tools only | Logged bot answers, terminology check | Call Tarot or Numerology tools |
| 6 | Tarot Research | Domain Knowledge | Sonnet 5.5 | `tarot_*` tools only | Logged bot answers, card checks | Call other bots |
| 7 | Numerology Research | Domain Knowledge | Sonnet 5.5 | `numerology_*` tools only | Logged answers, calculation checks | Call other bots |
| 8 | Content Brief | Content Production | Sonnet 5.5 | Content Service briefs | Outline, persona, FAQs, link plan | Write body copy |
| 9 | Senior Blog Writer | Content Production | Opus 5.5 | Briefs, logged bot answers, sources | Draft version | Call bots directly, publish |
| 10 | SEO Optimization | Content Production | Sonnet 5.5 | Draft read and write, schema builder | Meta, headings, links, alt text, JSON-LD | Change factual claims |
| 11 | Fact Checking | Content Production | Opus 5.5 | Claims table, bot logs, web search and fetch | Verdict per claim with evidence | Edit the draft |
| 12 | Senior Editor | Content Production | Opus 5.5 | Draft, claims, brand rubric | Approve to human, or send back | Publish |
| 13 | CMS Publishing | Publishing and Analytics | Haiku 5.5 | `cms_create_draft`, `cms_publish` (needs approval id) | CMS draft, live post, sitemap ping | Publish without a human approval |
| 14 | SEO Performance Analyst | Publishing and Analytics | Sonnet 5.5 | OpenSEO GSC and GA4 tools, metrics tables | Daily metrics, weekly numbers | Edit content |
| 15 | Content Refresh | Publishing and Analytics | Sonnet 5.5 | Metrics, articles, OpenSEO | Refresh tasks with reasons | Publish changes |
