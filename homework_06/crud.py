from sqlalchemy.orm import Session
import models
from schemas.question import CategoryBase, QuestionCreate


def get_categories(db: Session):
    return db.query(models.Category).all()


def create_category(db: Session, category: CategoryBase):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(db: Session, category_id: int, category_data: CategoryBase):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category:
        db_category.name = category_data.name
        db.commit()
        db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category:
        # сначала удаляем все вопросы этой категории
        db.query(models.Question).filter(models.Question.category_id == category_id).delete()
        db.delete(db_category)
        db.commit()
        return True
    return False


def get_questions(db: Session):
    return db.query(models.Question).all()


def create_question(db: Session, question: QuestionCreate):
    db_question = models.Question(
        text=question.text,
        category_id=question.category_id
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question