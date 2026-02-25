from app.db.models import Category
from sqlalchemy import select

def list_all_categories(db) -> list[Category]:
    return db.execute(select(Category)).scalars().all()

def create_category_crud(db, payload):
    category = Category(**payload.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category