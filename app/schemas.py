from pydantic import BaseModel, Field, validator
from typing import List

VALID_POINTS = {1, 2, 3, 5, 8, 13}

class ScrumOutput(BaseModel):
    user_story: str
    acceptance_criteria: List[str]
    definition_of_done: List[str]
    technical_approach: str
    test_cases: List[str]
    story_points: int
    priority: str
    confidence: str
    estimation_reasoning: str
    risks: List[str]

    @validator("story_points")
    def validate_story_points(cls, v):
        if v not in VALID_POINTS:
            raise ValueError("Invalid story points")
        return v

    @validator("priority")
    def validate_priority(cls, v):
        if v not in ["Low", "Medium", "High"]:
            raise ValueError("Invalid priority")
        return v
