from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProductBase(BaseModel):
    description: str
    sale_price: float
    barcode: str
    section: str
    initial_stock: int
    expiration_date: Optional[datetime] = None
    images: Optional[str] = None 

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    description: Optional[str] = None
    sale_price: Optional[float] = None
    barcode: Optional[str] = None
    section: Optional[str] = None
    initial_stock: Optional[int] = None
    expiration_date: Optional[datetime] = None
    images: Optional[str] = None

class ProductInDB(ProductBase):
    id: int
    current_stock: int

    class Config:
        from_attributes = True