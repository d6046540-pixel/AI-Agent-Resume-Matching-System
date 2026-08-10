from pydantic import BaseModel


class CareerReport(BaseModel):

    score: int

    strengths: list[str]

    weaknesses: list[str]

    suggestions: list[str]