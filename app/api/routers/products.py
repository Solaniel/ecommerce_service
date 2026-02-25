from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud.products import create_product_crud, list_all_products
from app.schemas.product import ProductCreate, ProductRead

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

@router.get("/", response_model=list[ProductRead])
def get_products(db: Session = Depends(get_db)):
    return list_all_products(db)

@router.post("/", response_model=ProductRead)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product_crud(db, product)
