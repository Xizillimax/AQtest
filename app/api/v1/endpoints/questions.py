from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.question import (
    QuestionCreate,
    QuestionResponse,
    QuestionWithAnswers,
)
from app.services.question_service import QuestionService

router = APIRouter()


@router.get("/", response_model=List[QuestionResponse])
async def get_questions(db: Session = Depends(get_db)):
    """Получить список всех вопросов"""
    questions = QuestionService.get_all_questions(db)
    return questions


@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
    question_data: QuestionCreate, db: Session = Depends(get_db)
):
    """Создать новый вопрос"""
    question = QuestionService.create_question(db, question_data)
    return question


@router.get("/{question_id}", response_model=QuestionWithAnswers)
async def get_question(question_id: int, db: Session = Depends(get_db)):
    """Получить вопрос и все ответы на него"""
    question = QuestionService.get_question_with_answers(db, question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Вопрос с id={question_id} не найден",
        )
    return question


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(question_id: int, db: Session = Depends(get_db)):
    """Удалить вопрос (вместе с ответами)"""
    success = QuestionService.delete_question(db, question_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Вопрос с id={question_id} не найден",
        )
