from sqlalchemy.orm import Session, selectinload
from app.db.models import Product
from sqlalchemy import select

from app.schemas.product import ProductCreate


def list_all_products(db: Session) -> list[Product]:
    query = select(Product).options(selectinload(Product.category))
    return db.execute(query).scalars().all()

def list_specific_product(db: Session, id: int) -> Product:
    query = select(Product).where(Product.id == id).options(selectinload(Product.category))
    return db.execute(query).scalars().one_or_none()

def create_product_crud(db: Session, payload: ProductCreate):
    data = payload.model_dump()

    if data.get("image"):
        data["image"] = str(data["image"])

    product = Product(**data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product