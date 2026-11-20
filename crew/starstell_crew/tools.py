"""Tools the crew's agents may call.

The StarsTell bot tools are deliberately not wired to any endpoint yet: their request and
response formats come from the StarsTell API documentation, which has not arrived
(docs/questions.md). Until then they say so, and the knowledge agents must label their
notes as model knowledge to be fact checked.
"""
from __future__ import annotations

import os

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class AskInput(BaseModel):
    question: str = Field(description="The question for the StarsTell bot, written for a blog audience")


class StarsTellBot(BaseTool):
    name: str = "starstell_bot"
    description: str = "Ask a StarsTell knowledge bot."
    args_schema: type[BaseModel] = AskInput
    vertical: str = "vedic"

    def _run(self, question: str) -> str:
        url = os.environ.get(f"STARSTELL_{self.vertical.upper()}_API_URL")
        if not url:
            return (f"NOT CONNECTED: the StarsTell {self.vertical} bot is not configured yet "
                    "(API documentation pending). Answer from your own knowledge, mark every point "
                    "'model knowledge, to be fact checked', and do not invent bot output.")
        # Implemented only from the official API documentation; see integrations/<vertical>/README.md.
        raise NotImplementedError(f"StarsTell {self.vertical} bot adapter is written once its API docs arrive")


def bot_tool(vertical: str) -> StarsTellBot:
    return StarsTellBot(name=f"starstell_{vertical}_bot",
                        description=f"Ask StarsTell's own {vertical} bot. Always try this before using your own knowledge.",
                        vertical=vertical)
