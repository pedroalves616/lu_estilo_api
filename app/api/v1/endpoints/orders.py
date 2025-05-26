from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import order as crud_order
from app.schemas.order import OrderCreate, OrderUpdate, OrderInDB
from app.core.security import get_current_user, has_role 
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[OrderInDB])
async def read_orders(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    start_date: datetime = None,
    end_date: datetime = None,
    product_section: str = None,
    order_id: int = None,
    status_filter: str = None, 
    client_id: int = None,
    current_user: Any = Depends(has_role(["admin", "regular"])) 
) -> Any:
    """
    List all orders, including filters: period, product section, order ID, order status, and client.
    """
    orders = crud_order.order.get_multi_filtered(
        db, skip=skip, limit=limit, start_date=start_date, end_date=end_date,
        product_section=product_section, order_id=order_id, status=status_filter, client_id=client_id
    )
    return orders

@router.post("/", response_model=OrderInDB, status_code=status.HTTP_201_CREATED)
async def create_order(
    *,
    db: Session = Depends(get_db),
    order_in: OrderCreate,
    current_user: Any = Depends(has_role(["admin", "regular"])) 
) -> Any:
    """
    Create a new order containing multiple products, validating available stock.
    """
    order = crud_order.order.create(db, obj_in=order_in)
    return order

@router.get("/{order_id}", response_model=OrderInDB)
async def read_order(
    *,
    db: Session = Depends(get_db),
    order_id: int,
    current_user: Any = Depends(has_role(["admin", "regular"])) 
) -> Any:
    """
    Get information of a specific order.
    """
    order = crud_order.order.get(db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/{order_id}", response_model=OrderInDB)
async def update_order(
    *,
    db: Session = Depends(get_db),
    order_id: int,
    order_in: OrderUpdate,
    current_user: Any = Depends(has_role(["admin"])) 
) -> Any:
    """
    Update information of a specific order, including order status.
    """
    order = crud_order.order.get(db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order = crud_order.order.update(db, db_obj=order, obj_in=order_in)
    return order

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    *,
    db: Session = Depends(get_db),
    order_id: int,
    current_user: Any = Depends(has_role(["admin"]))
) -> None: 
    """
    Delete an order.
    """
    order = crud_order.order.get(db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    crud_order.order.remove(db, id=order_id)
    return None 