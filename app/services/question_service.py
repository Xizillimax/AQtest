from typing import Optional
from sqlalchemy.orm import Session
import logging

from app.models.question import Question
from app.schemas.question import QuestionCreate, QuestionWithAnswers

logger = logging.getLogger(__name__)


class QuestionService:
    @staticmethod
    def get_all_questions(db: Session) -> list[Question]:
        """Получить все вопросы"""
        logger.info("Fetching all questions")
        return db.query(Question).order_by(Question.created_at.desc()).all()

    @staticmethod
    def get_question_by_id(db: Session, question_id: int) -> Optional[Question]:
        """Получить вопрос по ID"""
        logger.info(f"Fetching question with id={question_id}")
        return db.query(Question).filter(Question.id == question_id).first()

    @staticmethod
    def create_question(db: Session, question_data: QuestionCreate) -> Question:
        """Создать новый вопрос"""
        logger.info(f"Creating new question: {question_data.text[:50]}...")
        question = Question(text=question_data.text)
        db.add(question)
        db.commit()
        db.refresh(question)
        logger.info(f"Question created with id={question.id}")
        return question

    @staticmethod
    def delete_question(db: Session, question_id: int) -> bool:
        """Удалить вопрос (каскадно удалятся все ответы)"""
        logger.info(f"Deleting question with id={question_id}")
        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            logger.warning(f"Question with id={question_id} not found")
            return False
        db.delete(question)
        db.commit()
        logger.info(f"Question with id={question_id} deleted successfully")
        return True

    @staticmethod
    def get_question_with_answers(db: Session, question_id: int) -> Optional[QuestionWithAnswers]:
        """Получить вопрос со всеми ответами"""
        logger.info(f"Fetching question with id={question_id} and its answers")
        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            return None

        question_dict = {
            "id": question.id,
            "text": question.text,
            "created_at": question.created_at,
            "answers": [
                {
                    "id": answer.id,
                    "question_id": answer.question_id,
                    "user_id": answer.user_id,
                    "text": answer.text,
                    "created_at": answer.created_at,
                }
                for answer in question.answers
            ]
        }
        return QuestionWithAnswers(**question_dict)
