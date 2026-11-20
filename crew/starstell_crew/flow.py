"""One blog, end to end, as a crewAI Flow.

research -> brief -> knowledge -> English draft -> fact check (loop) ->
6 languages + images -> SEO pass with score gate (loop) -> editor -> awaiting human approval

The flow stops at human approval. Publishing is a separate run that needs Paperclip's
approval id (see run.py), so no agent can put anything live.
"""
from __future__ import annotations

import json
from typing import Literal

from crewai import Crew, Process, Task
from crewai.flow.flow import Flow, listen, or_, router, start
from pydantic import BaseModel

from .agents import build_team
from .config import LANGUAGES, MAX_REVISIONS, OUT_DIR
from .guardrails import article_spec, score_gate
from .models import Article, Brief, ClaimsReport, GapNote, ImagePlan, KeywordPlan


class BlogState(BaseModel):
    task_key: str = ""
    topic: str = ""
    vertical: str = "numerology"          # vedic, tarot or numerology
    keywords: dict = {}
    gap: dict = {}
    brief: dict = {}
    knowledge: str = ""
    articles: dict[str, dict] = {}        # language code -> Article
    claims: dict = {}
    fact_rounds: int = 0
    images: dict = {}
    status: str = "research"
    log: list[str] = []


def _run(agent, description: str, expected: str, output=None, **kw):
    task = Task(description=description, expected_output=expected, agent=agent, output_pydantic=output, **kw)
    result = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff()
    return result.pydantic if output else result.raw


class BlogFlow(Flow[BlogState]):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.team = build_team()

    def _note(self, msg: str) -> None:
        self.state.log.append(msg)
        print(f"[{self.state.task_key}] {msg}")

    # ---------------------------------------------------------------- SEO Research
    @start()
    def research(self):
        s, t = self.state, self.team
        kw = Task(description=f"Keyword research for '{s.topic}' ({s.vertical}). Primary keyword for each of: en, hi, hi-Latn, mr, ta, te, bn.",
                  expected_output="A KeywordPlan", agent=t["keyword"], output_pydantic=KeywordPlan)
        gap = Task(description=f"Study the pages ranking for the English primary keyword of '{s.topic}'. Report structure, gaps and errors; never copy text.",
                   expected_output="A GapNote", agent=t["competitor"], output_pydantic=GapNote, context=[kw])
        Crew(agents=[t["keyword"], t["competitor"]], tasks=[kw, gap], process=Process.sequential).kickoff()
        s.keywords, s.gap = kw.output.pydantic.model_dump(), gap.output.pydantic.model_dump()
        self._note("research done")

    @listen(research)
    def brief(self):
        s = self.state
        b = _run(self.team["brief"], f"Write the brief for '{s.topic}'.\nKeywords: {json.dumps(s.keywords)}\nGap note: {json.dumps(s.gap)}",
                 "A Brief", Brief)
        s.brief = b.model_dump()
        self._note(f"brief done, persona {b.persona}")

    # ---------------------------------------------------------------- Knowledge
    @listen(brief)
    def knowledge(self):
        s = self.state
        s.knowledge = _run(self.team[s.vertical], f"Collect what the writer needs for this brief:\n{json.dumps(s.brief)}",
                           "Numbered knowledge notes, each marked with its source (bot or model knowledge)")
        self._note("knowledge notes logged")

    # ---------------------------------------------------------------- Writing Room
    @listen(knowledge)
    def draft_english(self):
        self._write_english("Write the English article.")

    def _write_english(self, instruction: str):
        s = self.state
        a = _run(self.team["writer"],
                 f"{instruction}\nBrief: {json.dumps(s.brief)}\nKnowledge notes:\n{s.knowledge}\n"
                 f"Primary keyword: {s.keywords.get('primary', {}).get('en', s.topic)}",
                 "An Article in English", Article, guardrail=article_spec, guardrail_max_retries=3)
        s.articles["en"] = a.model_dump()
        self._note("English draft ready")

    @router(or_(draft_english, "revise"))
    def fact_check(self) -> Literal["verified", "needs_fix", "too_many_rounds"]:
        s = self.state
        report = _run(self.team["fact"], f"Fact check this article against the knowledge notes.\nArticle: {json.dumps(s.articles['en'])}\n"
                      f"Knowledge notes:\n{s.knowledge}", "A ClaimsReport", ClaimsReport)
        s.claims = report.model_dump()
        if not report.failing:
            self._note(f"fact check passed ({len(report.claims)} claims)")
            return "verified"
        s.fact_rounds += 1
        self._note(f"fact check: {len(report.failing)} claims failed (round {s.fact_rounds})")
        return "needs_fix" if s.fact_rounds <= MAX_REVISIONS else "too_many_rounds"

    @router("needs_fix")
    def fix_claims(self) -> Literal["revise"]:
        # A router, so its "revise" label sends the flow back to fact_check.
        failing = [c for c in self.state.claims["claims"] if c["verdict"] != "supported"]
        self._write_english(f"Rewrite the article: fix or remove these claims, change nothing else: {json.dumps(failing)}")
        return "revise"

    # ---------------------------------------------------------------- Language Desk + Design
    @listen("verified")
    def languages_and_images(self):
        s, t = self.state, self.team
        claims = json.dumps([c["text"] for c in s.claims["claims"]], ensure_ascii=False)
        tasks = [Task(description=f"Write the {name} version of this article natively.\nEnglish article: {json.dumps(s.articles['en'], ensure_ascii=False)}\n"
                                  f"Verified claims (add none): {claims}\nPrimary keyword: {s.keywords.get('primary', {}).get(code, '')}",
                      expected_output=f"An Article in {name}", agent=t[f"lang:{code}"], output_pydantic=Article,
                      guardrail=article_spec, guardrail_max_retries=3, async_execution=True)
                 for code, name in LANGUAGES]
        images = Task(description=f"Plan 3 to 5 images for this article, alt text in en, hi, hi-Latn, mr, ta, te, bn.\nBrief: {json.dumps(s.brief)}",
                      expected_output="An ImagePlan", agent=t["visual"], output_pydantic=ImagePlan, async_execution=True)
        finish = Task(description="Confirm all language versions and the image plan are complete.", expected_output="OK",
                      agent=t["editor"], context=tasks + [images])
        Crew(agents=[t[f"lang:{c}"] for c, _ in LANGUAGES] + [t["visual"], t["editor"]], tasks=tasks + [images, finish]).kickoff()
        for (code, _), task in zip(LANGUAGES, tasks):
            s.articles[code] = task.output.pydantic.model_dump()
        s.images = images.output.pydantic.model_dump()
        self._note("6 languages and the image plan done")

    # ---------------------------------------------------------------- SEO pass + score gate
    @listen(languages_and_images)
    def seo_and_score_gate(self):
        s = self.state
        for code, art in list(s.articles.items()):
            fixed = _run(self.team["seo"], f"Optimise this article. It must pass the article spec and score 90+ on SEO, GEO and AEO.\n"
                         f"Change no verified claim.\nArticle: {json.dumps(art, ensure_ascii=False)}",
                         "The optimised Article", Article, guardrail=score_gate, guardrail_max_retries=3)
            s.articles[code] = fixed.model_dump()
            self._note(f"{code}: passed the score gate")

    # ---------------------------------------------------------------- Editor, then stop for a person
    @listen(seo_and_score_gate)
    def editor_and_handoff(self):
        s = self.state
        verdict = _run(self.team["editor"], f"Final read of all versions for voice and safety: {json.dumps(s.articles, ensure_ascii=False)[:60000]}",
                       "APPROVE TO HUMAN, or SEND BACK with reasons")
        s.status = "awaiting_human_approval" if verdict.strip().upper().startswith("APPROVE") else "sent_back_by_editor"
        self._save()
        self._note(f"status: {s.status}")

    @listen("too_many_rounds")
    def escalate(self):
        self.state.status = "escalated_to_people"
        self._save()
        self._note("escalated: claims still failing after revisions")

    def _save(self):
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        path = OUT_DIR / f"{self.state.task_key}.json"
        path.write_text(self.state.model_dump_json(indent=1), encoding="utf-8")
        self._note(f"saved {path}")
