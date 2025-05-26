from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.database.models import Product
from app.schemas.product import ProductCreate, ProductUpdate

class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get_multi_filtered(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        availability: Optional[bool] = None 
    ) -> List[Product]:
        query = db.query(self.model)
        if category:
            query = query.filter(self.model.section.ilike(f"%{category}%"))
        if min_price is not None:
            query = query.filter(self.model.sale_price >= min_price)
        if max_price is not None:
            query = query.filter(self.model.sale_price <= max_price)
        if availability is not None:
            if availability:
                query = query.filter(self.model.current_stock > 0)
            else:
                query = query.filter(self.model.current_stock <= 0)
        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: ProductCreate) -> Product:
        db_obj = Product(current_stock=obj_in.initial_stock, **obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

product = CRUDProduct(Product)