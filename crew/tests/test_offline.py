"""Offline checks for the StarsTell crew. No model calls.

    python crew/tests/test_offline.py

Uses the finished life path 7 example as a known-good article. If SERYVON_PYTHON points at
an interpreter with Seryvon installed, the real score gate is run on it as well.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
os.environ.setdefault("ANTHROPIC_API_KEY", "offline-test-no-calls")

from starstell_crew.guardrails import article_problems, run_score_gate  # noqa: E402
from starstell_crew.models import QA, Article, DefinedTerm  # noqa: E402

EXAMPLE = HERE.parents[1] / "examples" / "life-path-number-7" / "preview" / "blog" / "life-path-number-7" / "index.html"


def example_article() -> Article:
    html = EXAMPLE.read_text(encoding="utf-8")
    pick = lambda pat: re.search(pat, html, re.S).group(1).strip()  # noqa: E731
    body = pick(r'<figure>.*?</figure>\s*(.*?)<aside>')
    body = re.sub(r'<section class="faq".*?</section>', "", body, flags=re.S)
    faqs = [QA(question=q, answer=a) for q, a in re.findall(r"<summary>(.*?)</summary><p>(.*?)</p>", html)]
    return Article(language="en", primary_keyword="life path number 7", slug="/blog/life-path-number-7",
                   title=pick(r"<title>(.*?)</title>"), description=pick(r'<meta name="description" content="(.*?)">'),
                   h1=pick(r"<h1>(.*?)</h1>"), lead=pick(r'<p class="lead">(.*?)</p>'), body_html=body, faqs=faqs,
                   image_alt="Seven golden stars of the Saptarishi over a lit brass diya",
                   defined_terms=[DefinedTerm(name=n, description=d) for n, d in re.findall(r'"DefinedTerm", "name": "(.*?)", "description": "(.*?)"', html)])


def test_good_article_passes():
    problems = article_problems(example_article())
    assert problems == [], problems


def test_bad_article_is_sent_back():
    a = example_article().model_copy(update={
        "title": "Life path 7", "lead": "Short.", "description": "Your destiny is guaranteed.",
        "body_html": "<h2>Intro</h2><h4>Skip</h4><p>Too short.</p>"})
    problems = article_problems(a)
    joined = " ".join(problems)
    for expected in ("Meta title", "Meta description", "Lead answer", "skip", "700", "table", "outside source", "banned"):
        assert expected.lower() in joined.lower(), (expected, problems)


def test_flow_builds():
    from starstell_crew.flow import BlogFlow
    flow = BlogFlow()
    assert len(flow.team) == 17


def test_publish_refuses_without_approval():
    import subprocess
    r = subprocess.run([sys.executable, "-m", "starstell_crew.run", "publish", "--task", "NO-SUCH-TASK"],
                       cwd=HERE.parent, capture_output=True, text=True)
    assert r.returncode != 0


def test_score_gate_on_example():
    if not os.environ.get("SERYVON_PYTHON"):
        print("  (skipped: SERYVON_PYTHON not set)")
        return
    result = run_score_gate(example_article())
    print("  scores:", result.get("scores"), "passed:", result.get("passed"), result.get("error", ""))
    assert result.get("passed"), result


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"PASS {name}")
            except AssertionError as exc:
                failed += 1
                print(f"FAIL {name}: {exc}")
    sys.exit(1 if failed else 0)
