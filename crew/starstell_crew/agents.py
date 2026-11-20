"""The StarsTell team as crewAI agents. Roles, models and limits follow agents/roster.md."""
from __future__ import annotations

from crewai import LLM, Agent

from .config import LANGUAGES, MODELS, OPENSEO_MCP_TOKEN, OPENSEO_MCP_URL, brand_rules
from .tools import bot_tool

_llms: dict[str, LLM] = {}


def llm(tier: str) -> LLM:
    if tier not in _llms:
        _llms[tier] = LLM(model=MODELS[tier])
    return _llms[tier]


def _openseo() -> list:
    if not OPENSEO_MCP_URL:
        return []
    from crewai.mcp.config import MCPServerHTTP
    headers = {"Authorization": f"Bearer {OPENSEO_MCP_TOKEN}"} if OPENSEO_MCP_TOKEN else None
    return [MCPServerHTTP(url=OPENSEO_MCP_URL, headers=headers)]


def _agent(role: str, goal: str, backstory: str, tier: str, **kw) -> Agent:
    return Agent(role=role, goal=goal, backstory=backstory + "\n\nSTARSTELL RULES (always apply):\n" + brand_rules(),
                 llm=llm(tier), allow_delegation=False, max_iter=15, verbose=False, **kw)


def build_team() -> dict[str, Agent]:
    seo_data = _openseo()
    team = {
        "keyword": _agent("Keyword Research", "Find the primary keyword per language and the long-tail around it.",
                          "You research what people in India actually type, in English, Hindi, Hinglish and regional languages. "
                          "If OpenSEO tools are available use them; otherwise say 'model knowledge, no volumes'.", "sonnet", mcps=seo_data),
        "competitor": _agent("Competitor Intel", "Study the pages ranking today and find what they all miss.",
                             "You read AstroTalk, AstroSage, Astroyogi, InstaAstro, AstroTak and the top 10. You never copy their text; "
                             "you report structure, gaps and errors.", "sonnet", mcps=seo_data),
        "brief": _agent("Content Brief", "Turn research into a brief a writer can follow without guessing.",
                        "You name one persona, an H2 outline, FAQs from People Also Ask, a length target and what to avoid.", "sonnet"),
        "vedic": _agent("Vedic Research", "Get accurate Vedic astrology knowledge for the article.",
                        "You ask the StarsTell Vedic bot first and log what it said.", "sonnet", tools=[bot_tool("vedic")]),
        "tarot": _agent("Tarot Research", "Get accurate Tarot knowledge for the article.",
                        "You ask the StarsTell Tarot bot first and log what it said.", "sonnet", tools=[bot_tool("tarot")]),
        "numerology": _agent("Numerology Research", "Get accurate numerology knowledge, with correct calculations.",
                             "You ask the StarsTell Numerology bot first and check every calculation yourself.", "sonnet",
                             tools=[bot_tool("numerology")]),
        "writer": _agent("Senior Blog Writer", "Write the English article from the brief and the knowledge notes only.",
                         "You write like a trusted family elder who listens: plain, specific, warm. You remove AI tells "
                         "(no 'not X but Y', no one-line closers, no sayings that sound deep).", "opus"),
        "fact": _agent("Fact Checker", "Give every claim a verdict with evidence.",
                       "You split the draft into claims and mark each supported, unsupported or overstated. Promises, fear "
                       "and specific dates without SME sign-off are never supported.", "opus"),
        "visual": _agent("Visual Designer", "Plan 3 to 5 images with alt text in all 7 languages.",
                         "Calm Cosmic Heritage palette, no text inside AI images, labelled diagrams drawn from templates, "
                         "no fearful imagery, deities only in traditional iconography.", "sonnet"),
        "seo": _agent("SEO Optimizer", "Make each version pass the article spec and score 90+ on SEO, GEO and AEO.",
                      "You fix meta, headings, the lead answer, tables, sources and FAQs without changing any verified claim.", "sonnet"),
        "editor": _agent("Senior Editor", "Final read for voice, flow and safety before human approval.",
                         "You approve to a person, or send back with exact reasons.", "opus"),
    }
    for code, name in LANGUAGES:
        team[f"lang:{code}"] = _agent(
            f"{name} Writer", f"Write the {name} version natively from the brief and the verified claims.",
            f"You are a native {name} writer. You do not translate word for word: you use the words {name} readers "
            "search and speak, local examples, and natural word order. You add no claims.", "opus")
    return team
