from typing import Any, List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.crud.base import CRUDBase
from app.database.models import Order, Product, order_product_association
from app.schemas.order import OrderCreate, OrderUpdate, OrderProduct
from fastapi import HTTPException, status
from datetime import datetime

class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    def create(self, db: Session, *, obj_in: OrderCreate) -> Order:
        total_amount = 0.0
        order_products = []

        for item in obj_in.products:
            product = db.query(Product).get(item.product_id)
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {item.product_id} not found")
            if product.current_stock < item.quantity:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Insufficient stock for product {product.description}. Available: {product.current_stock}")

            total_amount += product.sale_price * item.quantity
            product.current_stock -= item.quantity 
            order_products.append(product)

        db_obj = Order(
            client_id=obj_in.client_id,
            total_amount=total_amount,
            products=order_products 
        )
        db.add(db_obj)

        
        for item in obj_in.products:
            db.execute(
                order_product_association.insert().values(
                    order_id=db_obj.id,
                    product_id=item.product_id,
                    quantity=item.quantity
                )
            )

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_filtered(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        product_section: Optional[str] = None,
        order_id: Optional[int] = None,
        status: Optional[str] = None,
        client_id: Optional[int] = None
    ) -> List[Order]:
        query = db.query(self.model).options(joinedload(self.model.products)) # Eager load products [cite: 13]

        if start_date:
            query = query.filter(self.model.order_date >= start_date)
        if end_date:
            query = query.filter(self.model.order_date <= end_date)
        if product_section:
            query = query.join(self.model.products).filter(Product.section.ilike(f"%{product_section}%"))
        if order_id:
            query = query.filter(self.model.id == order_id)
        if status:
            query = query.filter(self.model.status.ilike(f"%{status}%"))
        if client_id:
            query = query.filter(self.model.client_id == client_id)

        return query.offset(skip).limit(limit).all()

    def get(self, db: Session, id: Any) -> Optional[Order]:
        return db.query(self.model).options(joinedload(self.model.products)).filter(self.model.id == id).first()

order = CRUDOrder(Order)