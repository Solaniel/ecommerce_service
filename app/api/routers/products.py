from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

@router.get("/")
def get_products(db: Session = Depends(get_db)):
    return []