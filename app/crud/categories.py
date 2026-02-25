from sqlalchemy.orm import Session, selectinload
from app.db.models import Category
from sqlalchemy import select

from app.schemas.category import CategoryCreate

def list_all_categories(db: Session) -> list[Category]:
    query = select(Category).options(selectinload(Category.children))
    return db.execute(query).scalars().all()

def list_specific_category(db: Session, id: int) -> Category:
    statement = select(Category).where(Category.id == id).options(selectinload(Category.children))
    return db.execute(statement).scalars().one_or_none()

def create_category_crud(db: Session, payload: CategoryCreate) -> Category:
    category = Category(**payload.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category