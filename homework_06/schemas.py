from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class QuestionCreate(BaseModel):
    text: str
    category_id: int


class QuestionResponse(BaseModel):
    id: int
    text: str
    category: CategoryResponse

    class Config:
        from_attributes = True