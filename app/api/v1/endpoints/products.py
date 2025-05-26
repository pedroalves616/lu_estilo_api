from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import product as crud_product
from app.schemas.product import ProductCreate, ProductUpdate, ProductInDB
from app.core.security import get_current_user, has_role 

router = APIRouter()

@router.get("/", response_model=List[ProductInDB])
async def read_products(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    min_price: float = None,
    max_price: float = None,
    availability: bool = None,
    current_user: Any = Depends(has_role(["admin", "regular"])) 
) -> Any:
    """
    List all products, with pagination and filters by category, price, and availability.
    """
    products = crud_product.product.get_multi_filtered(
        db, skip=skip, limit=limit, category=category,
        min_price=min_price, max_price=max_price, availability=availability
    )
    return products

@router.post("/", response_model=ProductInDB, status_code=status.HTTP_201_CREATED)
async def create_product(
    *,
    db: Session = Depends(get_db),
    product_in: ProductCreate,
    current_user: Any = Depends(has_role(["admin"])) 
) -> Any:
    """
    Create a new product.
    """
    
    product = crud_product.product.create(db, obj_in=product_in)
    return product

@router.get("/{product_id}", response_model=ProductInDB)
async def read_product(
    *,
    db: Session = Depends(get_db),
    product_id: int,
    current_user: Any = Depends(has_role(["admin", "regular"])) 
) -> Any:
    """
    Get information of a specific product.
    """
    product = crud_product.product.get(db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductInDB)
async def update_product(
    *,
    db: Session = Depends(get_db),
    product_id: int,
    product_in: ProductUpdate,
    current_user: Any = Depends(has_role(["admin"])) 
) -> Any:
    """
    Update information of a specific product.
    """
    product = crud_product.product.get(db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product = crud_product.product.update(db, db_obj=product, obj_in=product_in)
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    *,
    db: Session = Depends(get_db),
    product_id: int,
    current_user: Any = Depends(has_role(["admin"]))
) -> None: 
    """
    Delete a product.
    """
    product = crud_product.product.get(db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    crud_product.product.remove(db, id=product_id)
    return None 