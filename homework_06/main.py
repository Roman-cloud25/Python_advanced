from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base, get_db
import crud, schemas, models


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Questions API")


@app.post("/categories", response_model=schemas.CategoryResponse)
def create_category(category: schemas.CategoryBase, db: Session = Depends(get_db)):
    return crud.create_category(db, category)


@app.post("/questions", response_model=schemas.QuestionResponse)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    return crud.create_question(db, question)

@app.get("/questions", response_model=list[schemas.QuestionResponse])
def get_questions(db: Session = Depends(get_db)):
    return db.query(models.Question).all()