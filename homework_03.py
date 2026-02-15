from decimal import Decimal
from sqlalchemy import (
    create_engine,
    Integer,
    String,
    Boolean,
    Numeric,
    ForeignKey
)
from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)

# Task_1
engine = create_engine("sqlite:///:memory:")

# Task_2
Session = sessionmaker(bind=engine)
session = Session()


# Task_3
class MyBase(DeclarativeBase):
    __abstract__ = True


class Product(MyBase):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    in_stock: Mapped[bool] = mapped_column(Boolean)


# Task_4
class Category(MyBase):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))


# Task_5
category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
category: Mapped["Category"] = relationship(back_populates="products")
products: Mapped[list["Product"]] = relationship(back_populates="category")
