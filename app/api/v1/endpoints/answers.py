from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.answer import AnswerCreate, AnswerResponse
from app.services.answer_service import AnswerService

router = APIRouter()


@router.post(
    "/questions/{question_id}/answers/",
    response_model=AnswerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_answer(
    question_id: int, answer_data: AnswerCreate, db: Session = Depends(get_db)
):
    """Добавить ответ к вопросу"""
    answer = AnswerService.create_answer(db, question_id, answer_data)
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Вопрос с id={question_id} не найден",
        )
    return answer


@router.get("/answers/{answer_id}", response_model=AnswerResponse)
async def get_answer(answer_id: int, db: Session = Depends(get_db)):
    """Получить конкретный ответ"""
    answer = AnswerService.get_answer_by_id(db, answer_id)
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ответ с id={answer_id} не найден",
        )
    return answer


@router.delete("/answers/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_answer(answer_id: int, db: Session = Depends(get_db)):
    """Удалить ответ"""
    success = AnswerService.delete_answer(db, answer_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ответ с id={answer_id} не найден",
        )
