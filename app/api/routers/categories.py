from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud.categories import create_category_crud, list_all_categories
from app.schemas.category import CategoryCreate, CategoryRead

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)

@router.get("/", response_model=list[CategoryRead])
def get_categories(db: Session = Depends(get_db)):
    return list_all_categories(db)

@router.post("/", response_model=CategoryRead, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return create_category_crud(db, category)
