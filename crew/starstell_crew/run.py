"""Run the StarsTell blog crew for one Paperclip task.

    python -m starstell_crew.run produce --task ST-144 --topic "Life path number 7" --vertical numerology
    python -m starstell_crew.run produce --task ST-144 --topic "Life path number 7" --vertical numerology --dry-run
    python -m starstell_crew.run publish --task ST-144 --approval-id ap_5521

`produce` runs the flow and stops at human approval; its state is saved to crew/out/<task>.json.
`publish` refuses to run without a Paperclip approval id and a passed score gate.
`--dry-run` builds the whole team and flow and draws it, without calling any model.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

from .config import LANGUAGES, OUT_DIR


def produce(args) -> int:
    if args.dry_run:
        os.environ.setdefault("ANTHROPIC_API_KEY", "dry-run-no-calls")
    from .flow import BlogFlow
    flow = BlogFlow()
    if args.dry_run:
        team = flow.team
        print(f"Team: {len(team)} agents")
        for key, agent in team.items():
            tools = [t.name for t in (agent.tools or [])]
            print(f"  {agent.role:<22} {agent.llm.model:<22} {', '.join(tools)}")
        steps = [m for m in ("research", "brief", "knowledge", "draft_english", "fact_check", "fix_claims",
                             "languages_and_images", "seo_and_score_gate", "editor_and_handoff", "escalate")]
        print("Flow steps:", " -> ".join(steps))
        out = OUT_DIR / "flow.html"
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        try:
            flow.plot(str(out.with_suffix("")))
            print(f"Flow diagram: {out}")
        except Exception as exc:  # plotting is a nicety, never a failure
            print(f"(flow diagram skipped: {exc})")
        return 0
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY is not set. Use --dry-run to check the crew without calling a model.", file=sys.stderr)
        return 2
    flow.kickoff(inputs={"task_key": args.task, "topic": args.topic, "vertical": args.vertical})
    print(f"Status: {flow.state.status}")
    return 0 if flow.state.status == "awaiting_human_approval" else 1


def publish(args) -> int:
    path = OUT_DIR / f"{args.task}.json"
    if not path.exists():
        print(f"No produced blog for {args.task} ({path}).", file=sys.stderr)
        return 2
    state = json.loads(path.read_text(encoding="utf-8"))
    if state.get("status") != "awaiting_human_approval":
        print(f"{args.task} is '{state.get('status')}', not awaiting approval. Nothing published.", file=sys.stderr)
        return 1
    if not args.approval_id:
        print("A Paperclip approval id is required to publish.", file=sys.stderr)
        return 1
    missing = [code for code in ["en"] + [c for c, _ in LANGUAGES] if code not in state.get("articles", {})]
    if missing:
        print(f"Missing language versions: {', '.join(missing)}. Nothing published.", file=sys.stderr)
        return 1
    if not os.environ.get("STARSTELL_CMS_API_URL"):
        print("CMS not connected yet (STARSTELL_CMS_API_URL unset; CMS details pending). Nothing published.", file=sys.stderr)
        return 2
    raise NotImplementedError("CMS adapter is written once the StarsTell CMS is confirmed (integrations/cms/README.md)")


def main() -> int:
    ap = argparse.ArgumentParser(prog="starstell_crew")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("produce", help="research, write, check and score one blog; stops at human approval")
    p.add_argument("--task", required=True)
    p.add_argument("--topic", required=True)
    p.add_argument("--vertical", choices=["vedic", "tarot", "numerology"], required=True)
    p.add_argument("--dry-run", action="store_true")
    q = sub.add_parser("publish", help="publish an approved blog (needs a Paperclip approval id)")
    q.add_argument("--task", required=True)
    q.add_argument("--approval-id")
    args = ap.parse_args()
    return produce(args) if args.cmd == "produce" else publish(args)


if __name__ == "__main__":
    sys.exit(main())
