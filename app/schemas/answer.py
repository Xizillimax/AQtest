from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class AnswerCreate(BaseModel):
    user_id: str = Field(..., min_length=1, description="Идентификатор пользователя")
    text: str = Field(..., min_length=1, max_length=5000, description="Текст ответа")

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Текст ответа не может быть пустым")
        return v.strip()

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Идентификатор пользователя не может быть пустым")
        return v.strip()


class AnswerResponse(BaseModel):
    id: int
    question_id: int
    user_id: str
    text: str
    created_at: datetime

    class Config:
        from_attributes = True
