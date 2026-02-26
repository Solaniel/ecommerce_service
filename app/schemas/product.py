from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from pydantic.types import condecimal

from app.schemas.category import CategoryMiniRead


Money = condecimal(max_digits=12, decimal_places=2, ge=0)


class ProductBase(BaseModel):
    sku: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None

    image: Optional[HttpUrl] = None

    price: Money
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    sku: Optional[str] = Field(default=None, min_length=1, max_length=64)
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    image: Optional[HttpUrl] = None
    price: Optional[Money] = None
    category_id: Optional[int] = None


class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category: Optional[CategoryMiniRead] = None

class ProductParams(BaseModel):
    title: str = Field(default=None, min_length=1, max_length=255)
    sku: str = Field(default=None, min_length=1, max_length=64)
    min_price: int = Field(default=None, ge=0)
    max_price: int = Field(default=None)
    category_id: int = Field(default=None, gt=0)
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)