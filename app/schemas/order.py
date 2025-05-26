from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.schemas.product import ProductInDB

class OrderProduct(BaseModel):
    product_id: int
    quantity: int

class OrderBase(BaseModel):
    client_id: int
    products: List[OrderProduct]

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[str] = None 

class OrderInDB(BaseModel):
    id: int
    client_id: int
    order_date: datetime
    status: str
    total_amount: float
    products: List[ProductInDB] 

    class Config:
        from_attributes = True