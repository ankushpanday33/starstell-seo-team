# 0003: crewAI runs the blog pipeline; Paperclip manages the team

- Status: Proposed, built and tested offline
- Date: 20/11/2026

## Context

The team was asked to use [crewAI](https://github.com/crewAIInc/crewAI) for the AI agents' work. Paperclip (decision 0001) already provides the org chart, schedules, budgets, approvals and audit log. Both can "run agents", so the split has to be clear or there are two orchestrators doing the same job.

crewAI at 1.15.44 (19/11/2026): MIT, about 61,000 stars, releases almost daily. Native Claude support (`anthropic/claude-opus-5-5`), Flows with routers for loops, task guardrails with automatic retries, structured outputs, parallel tasks, MCP servers on agents.

## Decision

- **crewAI defines how one blog is produced**: the 17 agents, the order, the fact-check loop, the parallel language and image work, and two code guardrails (article spec, Seryvon score gate 90+). Code in [crew/](../../crew/).
- **Paperclip decides when, who and whether**: it starts a crew run for a task, holds the budget, and its human approval is the only way to publish. The crew's `publish` command refuses to run without a Paperclip approval id.
- Guardrails are code, not instructions in a prompt, so a model cannot talk its way past them.

## Consequences

- One more dependency that moves fast; it is pinned to 1.15.44 and upgraded deliberately.
- Agent definitions now live in two places (Paperclip's org chart for management, crewAI for execution). `agents/roster.md` stays the single source both follow.
- Cost per blog is unchanged in shape (the same models do the same steps); crewAI adds guardrail retries, which the cost estimate's "rejected drafts" margin already covers.
- The agent office visualizer can later be fed from crewAI's event bus instead of the simulation.
