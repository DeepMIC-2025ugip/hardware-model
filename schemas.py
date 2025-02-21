from datetime import date, datetime
from typing import Dict, List

from pydantic import UUID4, BaseModel, ConfigDict


class ConversationCreate(BaseModel):
    from_system: bool
    content: str
    visible: bool = True


class ConversationResponse(ConversationCreate):
    id: UUID4
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class AnalysisCreate(BaseModel):
    report: str
    keyword: List[str]
    feelings: Dict[str, int]


class AnalysisResponse(AnalysisCreate):
    id: UUID4
    date: date

    model_config = ConfigDict(from_attributes=True)


# schema/character.py CharacterModelと同じ
class CharacterCreate(BaseModel):
    personality: str
    strengths: List[str]
    weaknesses: List[str]
    hobbies: List[str]
    family: str
    friends: List[str]
    school_life: str
    future_dream: str
    likes: List[str]
    dislikes: List[str]
    stress: str
    worries: str
    favorite_food: List[str]
    other: str


class CharacterResponse(CharacterCreate):
    id: UUID4
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
