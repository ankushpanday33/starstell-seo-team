"""Checks a task's output must pass before the crew moves on.

crewAI re-runs a task whose guardrail returns (False, feedback), giving the agent the
feedback, up to `guardrail_max_retries` times. Two guardrails:

- article_spec: the measurable rules in docs/article-spec.md
- score_gate: Seryvon scores the rendered page; SEO, GEO and AEO must each be 90+
"""
from __future__ import annotations

import functools
import http.server
import json
import re
import subprocess
import tempfile
import threading
from pathlib import Path

from .config import GATE_SCRIPT, SCORE_THRESHOLD, SERYVON_PYTHON
from .models import Article

BANNED = ["guarantee", "guaranteed", "predict", "destiny", "fate", "fortune", "100% accurate", "—"]
DEVANAGARI = {"hi", "mr"}


def _text(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


def article_problems(a: Article, full_body: bool = True) -> list[str]:
    """Every rule in docs/article-spec.md that can be checked in code. Empty list = pass."""
    p = []
    lo, hi = (45, 55) if a.language in DEVANAGARI else (50, 60)
    if a.language in ("ta", "te", "bn"):
        lo, hi = 40, 60
    if not lo <= len(a.title) <= hi:
        p.append(f"Meta title is {len(a.title)} characters; it must be {lo} to {hi}.")
    if not a.title.endswith("| StarsTell"):
        p.append("Meta title must end with ' | StarsTell'.")
    if not 140 <= len(a.description) <= 155:
        p.append(f"Meta description is {len(a.description)} characters; it must be 140 to 155.")
    kw = a.primary_keyword.lower()
    for field in ("title", "description", "h1"):
        if kw not in getattr(a, field).lower():
            p.append(f"Primary keyword '{a.primary_keyword}' is missing from the {field}.")
    if not re.fullmatch(r"/[a-z0-9/-]+", a.slug):
        p.append(f"Slug '{a.slug}' must be lowercase Roman letters, digits and hyphens.")
    lead_words = len(a.lead.split())
    if not 35 <= lead_words <= 70:
        p.append(f"Lead answer is {lead_words} words; it must be about 40 to 60.")
    body = a.body_html
    if "<h1" in body.lower():
        p.append("The body must not contain an H1; the page has exactly one.")
    levels = [int(x) for x in re.findall(r"<h([2-6])", body.lower())]
    if any(b - a_ > 1 for a_, b in zip([1] + levels, levels)):
        p.append("Heading levels skip a level (for example H2 to H4).")
    if full_body:
        words = len(_text(body).split())
        if words < 700:
            p.append(f"Body is {words} words; it must be at least 700.")
        if "<table" not in body.lower():
            p.append("Add at least one comparison table (answer engines lift tables).")
        if not re.search(r'href="https?://', body):
            p.append("Link at least one outside source with an absolute URL.")
        if len(a.faqs) < 3:
            p.append("Add at least 3 FAQs.")
        if not a.defined_terms:
            p.append("List the key terms the article defines (defined_terms).")
    lower = " ".join([a.title, a.description, a.h1, a.lead, _text(body)]).lower()
    found = [w for w in BANNED if w in lower]
    if found:
        p.append(f"Remove banned words or characters: {', '.join(found)}.")
    return p


def article_spec(output) -> tuple[bool, object]:
    """crewAI guardrail for any task whose output_pydantic is Article."""
    article = output.pydantic
    if article is None:
        return False, "Return the article in the required structured format."
    problems = article_problems(article)
    return (True, output) if not problems else (False, "Fix these and return the full article again:\n- " + "\n- ".join(problems))


# ---------------------------------------------------------------- score gate
def render_page(a: Article, site: str = "https://www.starstell.com", date: str | None = None) -> str:
    """The article as it will be published: head tags, schema, lead, body, FAQ."""
    import datetime as _dt
    date = date or _dt.date.today().isoformat()
    image = f"{site}/images{a.slug}/featured.webp"
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q.question, "acceptedAnswer": {"@type": "Answer", "text": q.answer}} for q in a.faqs]}
    post_ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a.h1, "description": a.description,
               "inLanguage": a.language, "mainEntityOfPage": site + a.slug,
               "author": {"@type": "Organization", "name": "StarsTell editorial team", "url": site + "/about"},
               "reviewedBy": {"@type": "Person", "name": "[Reviewer name]", "jobTitle": "[Reviewer role]",
                              "hasCredential": {"@type": "EducationalOccupationalCredential", "name": "[Credential]"}},
               "publisher": {"@type": "Organization", "name": "StarsTell", "url": site},
               "image": [image], "datePublished": date, "dateModified": date}
    terms_ld = {"@context": "https://schema.org", "@type": "DefinedTermSet", "name": "Terms in this article",
                "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t.name, "description": t.description} for t in a.defined_terms]}
    crumbs_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Blog", "item": site + "/blog"},
        {"@type": "ListItem", "position": 2, "name": a.h1, "item": site + a.slug}]}
    faq_html = "".join(f"<h3>{q.question}</h3><p>{q.answer}</p>" for q in a.faqs)
    short = a.title.replace(" | StarsTell", "")
    return f"""<!doctype html><html lang="{a.language}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{a.title}</title>
<meta name="description" content="{a.description}"><link rel="canonical" href="{site}{a.slug}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="article"><meta property="og:title" content="{short}"><meta property="og:description" content="{a.description}">
<meta property="og:url" content="{site}{a.slug}"><meta property="og:image" content="{image}"><meta property="og:image:alt" content="{a.image_alt}">
<meta property="article:published_time" content="{date}"><meta property="article:modified_time" content="{date}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{image}">
<meta name="twitter:title" content="{short}"><meta name="twitter:description" content="{a.description}">
<script type="application/ld+json">{json.dumps([post_ld, faq_ld, terms_ld, crumbs_ld] if a.defined_terms else [post_ld, faq_ld, crumbs_ld], ensure_ascii=False)}</script></head>
<body><header><nav aria-label="Breadcrumb"><a href="/">StarsTell</a> › <a href="/blog">Blog</a></nav></header>
<main><article><h1>{a.h1}</h1><p class="lead">{a.lead}</p>
<p><time datetime="{date}">{date}</time> · By <a href="/about" rel="author">StarsTell editorial team</a></p>{a.body_html}
<section><h2>Questions people ask</h2>{faq_html}</section></article></main>
<footer><a href="/about">About StarsTell</a> · <a href="/blog">All articles</a> · <a href="/consult">Talk to an expert</a> · <a href="/contact">Contact</a></footer></body></html>"""


def run_score_gate(a: Article) -> dict:
    """Serve the rendered page on 127.0.0.1 for one Seryvon run and return its result."""
    if not SERYVON_PYTHON:
        return {"passed": False, "error": "SERYVON_PYTHON is not set: the score gate cannot run, so the draft is blocked."}
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / a.slug.strip("/") / "index.html"
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(render_page(a), encoding="utf-8")
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=tmp)
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        report = Path(tmp) / "report.json"
        try:
            url = f"http://127.0.0.1:{server.server_address[1]}{a.slug.rstrip('/')}/"
            proc = subprocess.run([SERYVON_PYTHON, str(GATE_SCRIPT), url, "--out", str(report),
                                   "--threshold", str(SCORE_THRESHOLD)], capture_output=True, text=True, timeout=600)
        finally:
            server.shutdown()
        if not report.exists():
            return {"passed": False, "error": (proc.stderr or proc.stdout)[-500:]}
        return json.loads(report.read_text(encoding="utf-8"))


def score_gate(output) -> tuple[bool, object]:
    """crewAI guardrail: blocks the SEO task until SEO, GEO and AEO are each 90+."""
    article = output.pydantic
    if article is None:
        return False, "Return the article in the required structured format."
    problems = article_problems(article)
    if problems:
        return False, "Fix these first:\n- " + "\n- ".join(problems)
    result = run_score_gate(article)
    if result.get("passed"):
        return True, output
    if "error" in result:
        return False, result["error"]
    lines = [f"{p.upper()} {result['pillars'][p]['score']}" for p in ("seo", "geo", "aeo")]
    for p in ("seo", "geo", "aeo"):
        for c in result["pillars"][p]["criteria"]:
            if c["status"] != "not_measured" and c["weight"] > 0 and c["score"] < 100:
                lines.append(f"{p.upper()} {c['key']}: {c['explanation'][:160]}")
    return False, (f"Score gate failed: SEO, GEO and AEO must each be {SCORE_THRESHOLD:g}+.\n- " + "\n- ".join(lines)
                   + "\nFix the article and return it again.")
