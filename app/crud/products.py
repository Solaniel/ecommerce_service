from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload
from app.core.errors import ValidationErrors
from app.crud.validations import category_validation, sku_validation
from app.db.models import Product
from sqlalchemy import select

from app.schemas.product import ProductCreate, ProductParams, ProductUpdate


def list_all_products(db: Session) -> list[Product]:
    statement = select(Product).options(selectinload(Product.category))
    return db.execute(statement).scalars().all()

def list_specific_product(db: Session, id: int) -> Product:
    statement = select(Product).where(Product.id == id).options(selectinload(Product.category))
    return db.execute(statement).scalars().one_or_none()

def create_product_crud(db: Session, payload: ProductCreate):
    errors = []
    data = payload.model_dump()

    # Validations.
    if data.get("image"):
        data["image"] = str(data["image"])
    if data.get("sku"):
        valid_sku = sku_validation(db, sku=data["sku"])
        if valid_sku is not None:
            errors.append(valid_sku)
    # Casting to string, because it is always present and it can be 0 and this is false by default.
    if str(data.get("category_id")):
        valid_category = category_validation(db, data["category_id"])
        if valid_category is not None:
            errors.append(valid_category)
    if errors:
        print(f"Errors: {errors}")
        raise ValidationErrors(errors)

    # Creating the product.
    product = Product(**data)
    db.add(product)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise IntegrityError("Integrity error while creating product", e.params, e.orig)

    db.refresh(product)
    return product

def update_product_crud(db: Session, id: int, payload: ProductUpdate) -> Product:
    errors = []
    statement = select(Product).where(Product.id == id).options(selectinload(Product.category))
    product = db.execute(statement).scalars().one_or_none()
    if product is None:
        return None

    updates = payload.model_dump(exclude_unset=True)

    # Validations.
    if updates.get("sku"):
        valid_sku = sku_validation(db, sku=updates["sku"])
        if valid_sku is not None:
            errors.append(valid_sku)
    if updates.get("category_id") is not None:
        valid_category = category_validation(db, updates["category_id"])
        if valid_category is not None:
            errors.append(valid_category)
    if errors:
        print(f"Errors: {errors}")
        raise ValidationErrors(errors)

    # Updating the product.
    for (key, value) in updates.items():
        if key == "image" and value is not None:
            value = str(value)
        setattr(product, key, value)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise IntegrityError("Integrity error while updating product", e.params, e.orig)

    db.refresh(product)
    return product

def delete_product_crud(db: Session, id: int) -> None:
    statement = select(Product).where(Product.id == id).options(selectinload(Product.category))
    product = db.execute(statement).scalars().one_or_none()
    if product is None:
        return None
    db.delete(product)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise IntegrityError("Integrity error while deleting product", e.params, e.orig)

def search_for_product(db: Session, query: ProductParams):
    statement = select(Product).options(selectinload(Product.category))
    if query.title:
        statement = statement.where(Product.title.ilike(f"%{query.title}%"))
    if query.sku:
        statement = statement.where(Product.sku == query.sku)
    if query.min_price:
        statement = statement.where(Product.price >= query.min_price)
    if query.max_price:
        statement = statement.where(Product.price <= query.max_price)
    if query.category_id:
        statement = statement.where(Product.category_id == query.category_id)
    if query.min_price and query.max_price:
        if query.min_price > query.max_price:
            raise ValidationErrors({"field": "min_price & max_price", "message": f"min_price cannot be higher than max_price."})
    statement = statement.order_by(Product.id)
    statement = statement.offset(query.offset).limit(query.limit)
    return db.execute(statement).scalars().all()