"""StarsTell score gate.

Runs Seryvon (https://github.com/seryvon-com/seryvon, AGPL-3.0, self-hosted, used
unmodified) on a draft's private preview URL and decides whether the draft may go
to the CMS: SEO, GEO and AEO must each score at least the threshold (default 90).

Seryvon refuses private and loopback addresses on purpose. Drafts live on a private
preview host before approval, so this wrapper allows exactly the hosts listed in
STARSTELL_PREVIEW_HOSTS (default 127.0.0.1) and nothing else.

    python scoring/score_gate.py http://127.0.0.1:8767/blog/life-path-number-7/ --out report.json

Exit code 0 = passed, 1 = blocked, 2 = could not score.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys

import seryvon.crawler.safety as safety
from seryvon.core.audit import run_audit
from seryvon.core.config import AuditConfig, CrawlConfig

PILLARS = ("seo", "geo", "aeo")
ALLOWED = {h.strip() for h in os.environ.get("STARSTELL_PREVIEW_HOSTS", "127.0.0.1").split(",") if h.strip()}

_blocked = safety._ip_is_blocked
safety._ip_is_blocked = lambda ip: False if ip in ALLOWED else _blocked(ip)


def criteria_for(report, pillar):
    out = []
    for c in report.criteria:
        if pillar not in c.pillars:
            continue
        status = getattr(c.status, "value", str(c.status))
        out.append({"key": c.key, "score": round(c.score, 1), "status": status,
                    "weight": c.weight, "explanation": c.explanation})
    return sorted(out, key=lambda c: (c["status"] != "measured", c["score"]))


DEFAULT_CONFIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gate-config.yaml")


async def score(url: str, threshold: float, config_path: str = DEFAULT_CONFIG, min_coverage: float = 0.45) -> dict:
    config = AuditConfig.from_yaml(config_path) if config_path else AuditConfig()
    config.crawl = CrawlConfig(max_pages=1, max_depth=0, respect_robots=config.crawl.respect_robots)
    report, _pages = await run_audit(url, config)
    pillars = {}
    for p in PILLARS:
        ps = report.pillars.get(p)
        pillars[p] = {
            "score": round(ps.score, 1) if ps else None,
            "coverage": round(ps.coverage, 2) if ps else 0,
            # A score built from too few measured criteria does not count as a pass.
            "passed": bool(ps and ps.score >= threshold and ps.coverage >= min_coverage),
            "criteria": criteria_for(report, p),
        }
    return {
        "url": url,
        "threshold": threshold,
        "min_coverage": min_coverage,
        "scores": {p: pillars[p]["score"] for p in PILLARS},
        "passed": all(pillars[p]["passed"] for p in PILLARS),
        "pillars": pillars,
        "engine": f"seryvon {report.tool_version}",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--threshold", type=float, default=float(os.environ.get("STARSTELL_SCORE_THRESHOLD", 90)))
    ap.add_argument("--out")
    ap.add_argument("--min-coverage", type=float, default=float(os.environ.get("STARSTELL_MIN_COVERAGE", 0.45)))
    ap.add_argument("--config", default=DEFAULT_CONFIG, help="Seryvon YAML; '' for Seryvon defaults (site run)")
    args = ap.parse_args()
    try:
        result = asyncio.run(score(args.url, args.threshold, args.config, args.min_coverage))
    except Exception as exc:  # noqa: BLE001 - a gate that cannot score must block, loudly
        print(f"BLOCKED: could not score {args.url}: {exc}", file=sys.stderr)
        return 2
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=1, ensure_ascii=False)
    for p in PILLARS:
        pr = result["pillars"][p]
        print(f"{p.upper():4} {pr['score']!s:>6}  {'PASS' if pr['passed'] else 'FAIL'}  (coverage {pr['coverage']})")
        if not pr["passed"]:
            for c in pr["criteria"]:
                if c["status"] != "not_measured" and c["weight"] > 0 and c["score"] < 100:
                    print(f"       {c['score']:>5}  {c['key']}: {c['explanation'][:110]}")
    print("PASSED: may go to the CMS" if result["passed"] else
          f"BLOCKED: SEO, GEO and AEO must each be {args.threshold:g}+ with coverage {args.min_coverage:g}+")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
