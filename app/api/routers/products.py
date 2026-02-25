from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud.products import create_product_crud, list_all_products, list_specific_product, update_product_crud
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

@router.get("/", response_model=list[ProductRead])
def get_products(db: Session = Depends(get_db)):
    return list_all_products(db)

@router.get("/{product_id}", response_model=ProductRead)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    return list_specific_product(db, product_id)

@router.post("/", response_model=ProductRead)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product_crud(db, product)

@router.patch("/{product_id}", response_model=ProductRead)
def update_product_by_id(product_id: int, category: ProductUpdate, db: Session = Depends(get_db)):
    return update_product_crud(db, product_id, category)