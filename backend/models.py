"""Bounded specifications; model output is data, never executable code."""
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

ShortText = Annotated[str, Field(min_length=1, max_length=300)]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Event(StrictModel):
    title: str = Field(min_length=2, max_length=120)
    when: str = Field(max_length=120, description="Date/time copied from input, or 'Not provided'")
    location: str = Field(max_length=120)
    detail: str = Field(max_length=400)


class Section(StrictModel):
    heading: str = Field(min_length=2, max_length=100)
    body: str = Field(min_length=2, max_length=700)


class AppSpec(StrictModel):
    events: list[Event] = Field(default_factory=list, max_length=8)
    tasks: list[ShortText] = Field(default_factory=list, max_length=12)
    sections: list[Section] = Field(default_factory=list, max_length=8)


class ScoreBreakdown(StrictModel):
    scope: int = Field(ge=0, le=40, description="Feasibility of the small MVP scope")
    template_fit: int = Field(ge=0, le=35, description="Fit to supported template interactions")
    source_clarity: int = Field(ge=0, le=25, description="Clarity of source requirements")


class Idea(StrictModel):
    title: str = Field(min_length=3, max_length=80)
    pitch: str = Field(min_length=5, max_length=260)
    audience: str = Field(min_length=1, max_length=120)
    template: Literal["event", "checklist", "info"]
    verdict: Literal["GO", "REVIEW", "NO-GO"]
    score: int = Field(ge=0, le=100)
    reason: str = Field(min_length=1, max_length=300)
    features: list[ShortText] = Field(min_length=1, max_length=3)
    complexity: Literal["low", "medium"] = "low"
    score_breakdown: ScoreBreakdown | None = None
    spec: AppSpec = Field(default_factory=AppSpec)

    @model_validator(mode="after")
    def consistent_score(self):
        if self.score_breakdown:
            self.score = sum(self.score_breakdown.model_dump().values())
            self.verdict = "GO" if self.score >= 75 else "REVIEW" if self.score >= 50 else "NO-GO"
        return self


class Analysis(StrictModel):
    source_summary: str = Field(min_length=5, max_length=900)
    problem: str = Field(min_length=5, max_length=500)
    facts: list[ShortText] = Field(max_length=8)
    actions: list[ShortText] = Field(max_length=8)
    ideas: list[Idea] = Field(min_length=3, max_length=3)
    confidence_note: str = Field(min_length=1, max_length=300)

    @model_validator(mode="after")
    def distinct_ranked_ideas(self):
        if len({idea.title.casefold() for idea in self.ideas}) != 3:
            raise ValueError("Provide three different idea titles")
        self.ideas.sort(key=lambda idea: idea.score, reverse=True)
        return self


class AnalyzeRequest(StrictModel):
    description: str = Field(default="", max_length=2500)
    image_data_url: str | None = Field(default=None, max_length=7_000_000)


class BuildRequest(StrictModel):
    analysis: Analysis
    idea: Idea
