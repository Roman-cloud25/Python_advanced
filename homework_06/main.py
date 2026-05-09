from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import crud, models
from schemas.question import (
    CategoryBase,
    CategoryResponse,
    QuestionCreate,
    QuestionResponse,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Questions & Categories API")



@app.get("/categories", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)


@app.post("/categories", response_model=CategoryResponse, status_code=201)
def create_category(category: CategoryBase, db: Session = Depends(get_db)):
    return crud.create_category(db, category)


@app.put("/categories/{id}", response_model=CategoryResponse)
def update_category(id: int, category: CategoryBase, db: Session = Depends(get_db)):
    db_cat = crud.update_category(db, id, category)
    if not db_cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_cat


@app.delete("/categories/{id}", status_code=204)
def delete_category(id: int, db: Session = Depends(get_db)):
    if not crud.delete_category(db, id):
        raise HTTPException(status_code=404, detail="Category not found")



@app.get("/questions", response_model=list[QuestionResponse])
def get_questions(db: Session = Depends(get_db)):
    return crud.get_questions(db)


@app.post("/questions", response_model=QuestionResponse, status_code=201)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == question.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.create_question(db, question)
