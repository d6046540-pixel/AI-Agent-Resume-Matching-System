from typing import List
from pydantic import BaseModel, Field


class InterviewQuestion(BaseModel):

    question: str = Field(
        description="面试问题"
    )

    purpose: str = Field(
        description="为什么问这个问题"
    )

    evidence_to_check: str = Field(
        description="希望验证候选人的什么能力"
    )

    follow_up: List[str] = Field(
        default_factory=list,
        description="候选人回答模糊时的追问"
    )


class InterviewPlan(BaseModel):

    interview_strategy: str = Field(
        description="整体面试策略"
    )

    priority_areas: List[str] = Field(
        default_factory=list
    )

    questions: List[InterviewQuestion] = Field(
        default_factory=list
    )

    red_flags: List[str] = Field(
        default_factory=list
    )