from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    """
    Базовая схема для товара
    """
    name: str = Field(..., min_lenght=1, max_length=100, description="Product name")
    description: Optional[str] = Field(None, max_length=500, description="Product description")
    price: Decimal = Field(..., gt=0, decimal_places=2, description="Product price")
    category: str = Field(..., max_length=50, description="Product category")
    sizes: Optional[str] = Field(None, max_length=100, description="Available sizes")


class ProductList(BaseModel):
    """
    Схема для списка товаров с неполными данными
    """
    id: int = Field(..., description="Product ID")
    name: str = Field(..., min_lenght=1, max_length=100, description="Product name")
    price: Decimal = Field(..., gt=0, decimal_places=2, description="Product price")
    category: str = Field(..., max_length=50, description="Product category")

    class Config:
        from_attributes = True


class ProductCreate(ProductBase):
    """
    Схема для создания товара, наследуется от ProductBase
    """
    pass


class ProductFull(ProductBase):
    """
    Схема для товара с полной информацией и его ID
    """
    id: int = Field(..., description="Product ID")

    class Config:
        from_attributes = True