from typing import List, Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    questions: Mapped[List["Question"]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan",
    )


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(255), nullable=False)

    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True,
    )

    category: Mapped[Optional[Category]] = relationship(
        back_populates="questions"
    )
