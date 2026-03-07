from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import crud, schemas, models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Questions & Categories API")


@app.get("/categories", response_model=list[schemas.CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)


@app.post("/categories", response_model=schemas.CategoryResponse)
def create_category(category: schemas.CategoryBase, db: Session = Depends(get_db)):
    return crud.create_category(db, category)


@app.put("/categories/{id}", response_model=schemas.CategoryResponse)
def update_category(id: int, category: schemas.CategoryBase, db: Session = Depends(get_db)):
    db_cat = crud.update_category(db, id, category)
    if not db_cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_cat


@app.delete("/categories/{id}")
def delete_category(id: int, db: Session = Depends(get_db)):
    if not crud.delete_category(db, id):
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}


@app.post("/questions", response_model=schemas.QuestionResponse)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    return crud.create_question(db, question)


@app.get("/questions", response_model=list[schemas.QuestionResponse])
def get_questions(db: Session = Depends(get_db)):
    return db.query(models.Question).all()
