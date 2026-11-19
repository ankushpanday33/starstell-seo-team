# 0001: Paperclip + OpenSEO + Content Service + PostgreSQL

- Status: Proposed, awaiting approval
- Date: 19/11/2026

## Context

StarsTell wants an AI SEO department of 15 agents that uses its existing Vedic Astrology, Tarot and Numerology bots, with human approval before publishing, an audit log, budgets and a dashboard. Four open-source projects were evaluated: Paperclip, OpenSEO, CrawlSEO and n8n.

## Decision

1. **Paperclip** is the management layer: org chart, tasks, approval stages, budgets with hard stops, routines, secrets and activity log are built in. MIT.
2. **OpenSEO** supplies SEO intelligence over MCP, paid per call through DataForSEO. MIT.
3. **StarsTell Content Service** is built in this repo. It is the only component holding bot and CMS credentials, it stores drafts, bot answers and claims, and it blocks publishing without a recorded human approval.
4. **PostgreSQL**, one instance with separate databases for Paperclip, OpenSEO and the Content Service.

## Not chosen

- **CrawlSEO:** most features repeat OpenSEO. Revisit in Phase 4 for crawling, Core Web Vitals and content-decay alerts if OpenSEO's audits and GSC insights fall short.
- **n8n:** Paperclip routines and webhooks already cover scheduling and triggers. A second orchestrator would add a second audit trail. Internal use would be allowed under its Sustainable Use License, so this can be revisited if non-developers need to build workflows.

## Consequences

- Paperclip releases often; pin a version and upgrade deliberately.
- OpenSEO is pre-1.0; agent skills should tolerate tool renames.
- Budget enforcement relies on reported spend; an in-flight run can slightly exceed a cap.
