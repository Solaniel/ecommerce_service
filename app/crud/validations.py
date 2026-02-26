
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Category, Product


def sku_validation(db: Session, sku: str):
    sku_exists = db.execute(select(Product.id).where(Product.sku == sku)).scalar_one_or_none()
    if sku_exists is not None:
        return {"field": "sku", "message": f"sku={sku} already exists"}
    return None

def category_validation(db: Session, category_id: int):
    category_exists = db.execute(select(Category.id).where(Category.id == category_id)).scalar_one_or_none()
    if category_exists is None:
        return {"field": "category_id", "message": f"category_id={category_id} does not exist"}
    return None