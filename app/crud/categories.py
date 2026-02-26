from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload
from app.core.errors import ValidationErrors
from app.crud.validations import category_validation
from app.db.models import Category
from sqlalchemy import select

from app.schemas.category import CategoryCreate, CategoryUpdate

def list_all_categories(db: Session) -> list[Category]:
    query = select(Category).options(selectinload(Category.children))
    return db.execute(query).scalars().all()

def list_specific_category(db: Session, id: int) -> Category:
    statement = select(Category).where(Category.id == id).options(selectinload(Category.children))
    return db.execute(statement).scalars().one_or_none()

def create_category_crud(db: Session, payload: CategoryCreate) -> Category:
    category = Category(**payload.model_dump())
    db.add(category)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise IntegrityError("Integrity error while creating category", e.params, e.orig)

    db.refresh(category)
    return category

def update_category_crud(db: Session, id: int, payload: CategoryUpdate) -> Category:
    errors = []
    statement = select(Category).where(Category.id == id).options(selectinload(Category.children))
    category = db.execute(statement).scalars().one_or_none()
    if category is None:
        return None
    
    if payload.parent_id is not None:
        valid_category = category_validation(db, payload.parent_id)
        if valid_category is not None:
            errors.append(valid_category)
        if payload.parent_id == id:
            errors.append({"field": "parent_id", "message": f"parent_id = {payload.parent_id} must be different than the ID of the category."})
    
    if errors:
        raise ValidationErrors(errors)
    
    category.parent_id = payload.parent_id
    category.name = payload.name

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise IntegrityError("Integrity error while updating category", e.params, e.orig)
    db.refresh(category)
    return category

def delete_category_crud(db: Session, id: int) -> None:
    statement = select(Category).where(Category.id == id)
    category = db.execute(statement).scalars().one_or_none()
    if category is None:
        return None
    db.delete(category)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise IntegrityError("Integrity error while deleting category", e.params, e.orig)
