from app.db.models import Product
from sqlalchemy import select


def list_all_products(db) -> list[Product]:
    return db.execute(select(Product)).scalars().all()

def create_product_crud(db, payload):
    data = payload.model_dump()

    if data.get("image"):
        data["image"] = str(data["image"])

    product = Product(**data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product