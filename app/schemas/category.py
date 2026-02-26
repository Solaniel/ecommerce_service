from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class CategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    parent_id: Optional[int] = None


class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    children: list[CategoryChildRead]

class CategoryChildRead(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    id: int

# Usefull for displaying categories inside the product, but not their children.
class CategoryMiniRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str