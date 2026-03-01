from sqlalchemy.orm import Session
import models, schemas

def get_categories(db: Session):
    return db.query(models.Category).all()

def create_category(db: Session, category: schemas.CategoryBase):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def create_question(db: Session, question: schemas.QuestionCreate):
    db_question = models.Question(
        text=question.text,
        category_id=question.category_id
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question