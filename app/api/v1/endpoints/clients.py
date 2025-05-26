from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import client as crud_client
from app.schemas.client import ClientCreate, ClientUpdate, ClientInDB
from app.core.security import get_current_user, has_role 

router = APIRouter()

@router.get("/", response_model=List[ClientInDB])
async def read_clients(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: str = None,
    email: str = None,
    current_user: Any = Depends(has_role(["admin", "regular"])) 
) -> Any:
    """
    List all clients, with pagination and filter by name and email.
    """
    clients = crud_client.client.get_multi_filtered(db, skip=skip, limit=limit, name=name, email=email)
    return clients

@router.post("/", response_model=ClientInDB, status_code=status.HTTP_201_CREATED)
async def create_client(
    *,
    db: Session = Depends(get_db),
    client_in: ClientCreate,
    current_user: Any = Depends(has_role(["admin"])) 
) -> Any:
    """
    Create a new client, validating email and CPF unique.
    """
    if crud_client.client.get_by_email(db, email=client_in.email):
        raise HTTPException(status_code=400, detail="Client with this email already exists")
    if crud_client.client.get_by_cpf(db, cpf=client_in.cpf):
        raise HTTPException(status_code=400, detail="Client with this CPF already exists")
    client = crud_client.client.create(db, obj_in=client_in)
    return client

@router.get("/{client_id}", response_model=ClientInDB)
async def read_client(
    *,
    db: Session = Depends(get_db),
    client_id: int,
    current_user: Any = Depends(has_role(["admin", "regular"])) 
) -> Any:
    """
    Get information of a specific client.
    """
    client = crud_client.client.get(db, id=client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.put("/{client_id}", response_model=ClientInDB)
async def update_client(
    *,
    db: Session = Depends(get_db),
    client_id: int,
    client_in: ClientUpdate,
    current_user: Any = Depends(has_role(["admin"])) 
) -> Any:
    """
    Update information of a specific client.
    """
    client = crud_client.client.get(db, id=client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    
    if client_in.email and client_in.email != client.email:
        if crud_client.client.get_by_email(db, email=client_in.email):
            raise HTTPException(status_code=400, detail="Another client with this email already exists")
    if client_in.cpf and client_in.cpf != client.cpf:
        if crud_client.client.get_by_cpf(db, cpf=client_in.cpf):
            raise HTTPException(status_code=400, detail="Another client with this CPF already exists")

    client = crud_client.client.update(db, db_obj=client, obj_in=client_in)
    return client

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    *,
    db: Session = Depends(get_db),
    client_id: int,
    current_user: Any = Depends(has_role(["admin"]))
) -> None: 
    """
    Delete a client.
    """
    client = crud_client.client.get(db, id=client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    crud_client.client.remove(db, id=client_id)
    return None 