from typing import List
from typing import Optional
from decimal import Decimal
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Numeric


from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    sku: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    image: Mapped[Optional[str]] = mapped_column(String(2048), nullable=True)

    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    @validates("price")
    def validate_price(self, key, price):
        if price < 0:
            raise ValueError("Price should be a positive decimal.")
        return price

    category_id: Mapped[int] = mapped_column(
        ForeignKey('categories.id', ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="products"
    )

 

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    parent: Mapped[Optional["Category"]] = relationship(
        "Category",
        remote_side="Category.id",
        back_populates="children"
    )

    children: Mapped[List["Category"]] = relationship(
        "Category",
        back_populates="parent",
    )

    products: Mapped[List["Product"]] = relationship(
        "Product",
        back_populates="category",
    )