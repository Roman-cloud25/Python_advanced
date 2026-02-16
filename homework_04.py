from decimal import Decimal
from sqlalchemy import (
    create_engine,
    Integer,
    String,
    Boolean,
    Numeric,
    ForeignKey,
    select,
    func
)
from sqlalchemy.orm import (
    Session,
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)

engine = create_engine("sqlite:///:memory:")


class MyBase(DeclarativeBase):
    pass


class Category(MyBase):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))
    products: Mapped[list["Product"]] = relationship(back_populates="category")


class Product(MyBase):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    in_stock: Mapped[bool] = mapped_column(Boolean)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(back_populates="products")


MyBase.metadata.create_all(engine)

# Task_1
with Session(engine) as session:
    electronics = Category(
        name="Электроника",
        description="Гаджеты и устройства."
    )
    books = Category(
        name="Книги",
        description="Печатные книги и электронные книги."
    )
    clothes = Category(
        name="Одежда",
        description="Одежда для мужчин и женщин."
    )

    session.add_all([electronics, books, clothes])
    session.commit()

    products = [
        Product(
            name="Смартфон",
            price=299.99,
            in_stock=True,
            category=electronics
        ),
        Product(
            name="Ноутбук",
            price=499.99,
            in_stock=True,
            category=electronics
        ),
        Product(
            name="Научно-фантастический роман",
            price=15.99,
            in_stock=True,
            category=books
        ),
        Product(
            name="Джинсы",
            price=40.50,
            in_stock=True,
            category=clothes
        ),
        Product(
            name="Футболка",
            price=20.00,
            in_stock=True,
            category=clothes)
    ]

    session.add_all(products)
    session.commit()

    # Task_2
    categories = session.query(Category).all()

    print("\nКатегории и продукты:")
    for category in categories:
        print(f"Категория: {category.name}")
        for product in category.products:
            print(f" - {product.name}: {product.price}")

    # Task_3
    smartphone = session.scalar(select(Product).where(Product.name == "Смартфон"))

    if smartphone:
        smartphone.price = Decimal("349.99")
        session.commit()

    # Task_4
    results = (
        select(Category.name, func.count(Product.id))
        .join(Product)
        .group_by(Category.id)
    )

    print("\nKоличество продуктов по категориям:")
    for name, count in session.execute(results):
        print(f"{name}: {count}")

    # Task_5
    result = (
        select(Category.name, func.count(Product.id))
        .join(Product)
        .group_by(Category.id)
        .having(func.count(Product.id) > 1)
    )

    print("\nКатегории с более чем одним продуктом:")
    for name, count in session.execute(result):
        print(f"{name}: {count}")
