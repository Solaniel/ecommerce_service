from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud.categories import create_category_crud, delete_category_crud, list_all_categories, list_specific_category, update_category_crud
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)

@router.get("/", response_model=list[CategoryRead])
def get_categories(db: Session = Depends(get_db)):
    return list_all_categories(db)

@router.get("/{category_id}", response_model=CategoryRead)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    category = list_specific_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/", response_model=CategoryRead, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return create_category_crud(db, category)

@router.patch("/{category_id}", response_model=CategoryRead)
def update_category_by_id(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    updated_category = update_category_crud(db, category_id, category)
    if updated_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category

@router.delete("/{category_id}", status_code=204)
def delete_category_by_id(category_id: int, db: Session = Depends(get_db)):
    category = list_specific_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    delete_category_crud(db, category_id)
    return Response(status_code=204)