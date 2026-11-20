"""Structured outputs each crew task must return. crewAI validates them (output_pydantic)."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class Keyword(BaseModel):
    term: str
    language: str
    intent: str = "informational"
    note: str = ""


class KeywordPlan(BaseModel):
    primary: dict[str, str] = Field(description="Primary keyword per language code: en, hi, hi-Latn, mr, ta, te, bn")
    secondary: list[Keyword] = []
    data_source: str = Field(description="'OpenSEO' or 'model knowledge, no volumes'")


class Competitor(BaseModel):
    url: str
    notes: str


class GapNote(BaseModel):
    competitors: list[Competitor]
    must_cover: list[str]
    missing_everywhere: list[str]
    our_angle: str
    target_words: int


class Brief(BaseModel):
    persona: str
    h1: str
    outline: list[str] = Field(description="H2 headings in order")
    faqs: list[str]
    target_words: int
    must_avoid: list[str]


class QA(BaseModel):
    question: str
    answer: str


class DefinedTerm(BaseModel):
    name: str
    description: str


class Article(BaseModel):
    language: str = Field(description="en, hi, hi-Latn, mr, ta, te or bn")
    primary_keyword: str
    slug: str
    title: str = Field(description="Meta title, ends with ' | StarsTell'")
    description: str = Field(description="Meta description, 140 to 155 characters")
    h1: str
    lead: str = Field(description="40 to 60 word direct answer, the first paragraph after the H1")
    body_html: str = Field(description="Article body as HTML: H2/H3, paragraphs, at least one comparison table, links to outside sources. No H1.")
    faqs: list[QA]
    defined_terms: list[DefinedTerm] = Field(default=[], description="Key terms the article explains, with one-line definitions")
    image_alt: str = Field(default="", description="Alt text for the featured image, in this article's language")


class Claim(BaseModel):
    text: str
    verdict: Literal["supported", "unsupported", "overstated"]
    evidence: str


class ClaimsReport(BaseModel):
    claims: list[Claim]

    @property
    def failing(self) -> list[Claim]:
        return [c for c in self.claims if c.verdict != "supported"]


class ImageSpec(BaseModel):
    file: str
    kind: Literal["illustration", "diagram"]
    prompt: str = Field(description="Image-model prompt for illustrations, or the diagram's content")
    alt: dict[str, str] = Field(description="Alt text per language code, under 125 characters, no text inside AI images")


class ImagePlan(BaseModel):
    images: list[ImageSpec] = Field(min_length=3, max_length=5)
