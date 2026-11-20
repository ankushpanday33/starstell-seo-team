"""Settings for the StarsTell blog crew. Values come from the environment (see .env.example)."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # repository root
CONTEXT = ROOT / "context"
OUT_DIR = Path(os.environ.get("STARSTELL_CREW_OUT", ROOT / "crew" / "out"))

# Claude models by job, as in agents/roster.md.
MODELS = {
    "opus": os.environ.get("STARSTELL_MODEL_OPUS", "anthropic/claude-opus-5-5"),
    "sonnet": os.environ.get("STARSTELL_MODEL_SONNET", "anthropic/claude-sonnet-5-5"),
    "haiku": os.environ.get("STARSTELL_MODEL_HAIKU", "anthropic/claude-haiku-5-5"),
}

# The 6 languages written after English (code, name).
LANGUAGES = [("hi", "Hindi"), ("hi-Latn", "Hinglish"), ("mr", "Marathi"),
             ("ta", "Tamil"), ("te", "Telugu"), ("bn", "Bengali")]

# OpenSEO's MCP endpoint, when self-hosted. Without it the research agents work from their own knowledge
# and say so in their output.
OPENSEO_MCP_URL = os.environ.get("OPENSEO_MCP_URL")
OPENSEO_MCP_TOKEN = os.environ.get("OPENSEO_MCP_TOKEN")

# Score gate (scoring/score_gate.py). SERYVON_PYTHON is the interpreter that has Seryvon installed.
SCORE_THRESHOLD = float(os.environ.get("STARSTELL_SCORE_THRESHOLD", 90))
SERYVON_PYTHON = os.environ.get("SERYVON_PYTHON")
GATE_SCRIPT = ROOT / "scoring" / "score_gate.py"

# How many times a step may be sent back before a person is asked to step in.
MAX_REVISIONS = int(os.environ.get("STARSTELL_MAX_REVISIONS", 2))


def brand_rules() -> str:
    """The StarsTell voice every agent works to (context/brand-voice.md + style guide)."""
    parts = []
    for name in ("brand-voice.md", "style-guide.md"):
        path = CONTEXT / name
        if path.exists():
            parts.append(path.read_text(encoding="utf-8"))
    return "\n\n".join(parts)
