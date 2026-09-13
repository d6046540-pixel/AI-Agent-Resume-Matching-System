from typing import List, Literal
from pydantic import BaseModel, Field


class SkillMatch(BaseModel):
    skill: str

    required: bool = True

    evidence_level: Literal[
        "strong",
        "weak",
        "none"
    ]

    evidence: List[str] = Field(
        default_factory=list
    )

    score: float = Field(
        default=0,
        ge=0,
        le=100
    )


class MatchResult(BaseModel):

    overall_score: float = Field(
        ge=0,
        le=100
    )

    skill_score: float = Field(
        ge=0,
        le=100
    )

    responsibility_score: float = Field(
        ge=0,
        le=100
    )

    project_evidence_score: float = Field(
        ge=0,
        le=100
    )

    experience_score: float = Field(
        ge=0,
        le=100
    )

    education_score: float = Field(
        ge=0,
        le=100
    )

    semantic_score: float = Field(
        ge=0,
        le=100
    )

    skill_matches: List[SkillMatch] = Field(
        default_factory=list
    )

    strengths: List[str] = Field(
        default_factory=list
    )

    gaps: List[str] = Field(
        default_factory=list
    )

    verification_items: List[str] = Field(
        default_factory=list
    )

    recommendation: Literal[
        "strong_match",
        "match",
        "interview_verify",
        "weak_match"
    ]