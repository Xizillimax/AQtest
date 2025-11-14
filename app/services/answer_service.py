from typing import Optional
from sqlalchemy.orm import Session
import logging

from app.models.answer import Answer
from app.models.question import Question
from app.schemas.answer import AnswerCreate

logger = logging.getLogger(__name__)


class AnswerService:
    @staticmethod
    def get_answer_by_id(db: Session, answer_id: int) -> Optional[Answer]:
        """Получить ответ по ID"""
        logger.info(f"Fetching answer with id={answer_id}")
        return db.query(Answer).filter(Answer.id == answer_id).first()

    @staticmethod
    def create_answer(
        db: Session, question_id: int, answer_data: AnswerCreate
    ) -> Optional[Answer]:
        """Создать ответ на вопрос"""
        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            logger.warning(f"Question with id={question_id} not found")
            return None

        logger.info(
            f"Creating answer for question_id={question_id} by user_id={answer_data.user_id}"
        )
        answer = Answer(
            question_id=question_id,
            user_id=answer_data.user_id,
            text=answer_data.text,
        )
        db.add(answer)
        db.commit()
        db.refresh(answer)
        logger.info(f"Answer created with id={answer.id}")
        return answer

    @staticmethod
    def delete_answer(db: Session, answer_id: int) -> bool:
        """Удалить ответ"""
        logger.info(f"Deleting answer with id={answer_id}")
        answer = db.query(Answer).filter(Answer.id == answer_id).first()
        if not answer:
            logger.warning(f"Answer with id={answer_id} not found")
            return False
        db.delete(answer)
        db.commit()
        logger.info(f"Answer with id={answer_id} deleted successfully")
        return True

