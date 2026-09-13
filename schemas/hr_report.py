from typing import List, Literal
from pydantic import BaseModel, Field


class EvidenceItem(BaseModel):

    claim: str

    evidence: List[str] = Field(
        default_factory=list
    )

    status: Literal[
        "supported",
        "insufficient"
    ]


class HRReport(BaseModel):

    overall_assessment: str

    strengths: List[str] = Field(
        default_factory=list
    )

    weaknesses: List[str] = Field(
        default_factory=list
    )

    evidence: List[EvidenceItem] = Field(
        default_factory=list
    )

    risks: List[str] = Field(
        default_factory=list
    )

    verification_items: List[str] = Field(
        default_factory=list
    )

    interview_focus: List[str] = Field(
        default_factory=list
    )

    recommendation: Literal[
        "recommend",
        "interview",
        "hold",
        "not_recommend"
    ]