from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, field_validator

from app.schemas.answer import AnswerResponse


class QuestionCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Текст вопроса")

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Текст вопроса не может быть пустым")
        return v.strip()


class QuestionResponse(BaseModel):
    id: int
    text: str
    created_at: datetime

    class Config:
        from_attributes = True


class QuestionWithAnswers(QuestionResponse):
    answers: List[AnswerResponse] = []

    class Config:
        from_attributes = True
