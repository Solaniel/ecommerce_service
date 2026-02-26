from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud.products import create_product_crud, delete_product_crud, list_all_products, list_specific_product, search_for_product, update_product_crud
from app.schemas.product import ProductCreate, ProductParams, ProductRead, ProductUpdate

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

@router.get("/", response_model=list[ProductRead])
def get_products(db: Session = Depends(get_db)):
    return list_all_products(db)

@router.get("/search", response_model=list[ProductRead])
def search_products(query: Annotated[ProductParams, Query()], db: Session = Depends(get_db)):
    return search_for_product(db, query)

@router.get("/{product_id}", response_model=ProductRead)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = list_specific_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductRead, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product_crud(db, product)

@router.patch("/{product_id}", response_model=ProductRead)
def update_product_by_id(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    updated_product = update_product_crud(db, product_id, product)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/{product_id}", status_code=204)
def delete_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = list_specific_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    delete_product_crud(db, product_id)
    return Response(status_code=204)