from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.crud.base import CRUDBase
from app.database.models import Client
from app.schemas.client import ClientCreate, ClientUpdate

class CRUDClient(CRUDBase[Client, ClientCreate, ClientUpdate]):
    def get_by_email(self, db: Session, email: str) -> Optional[Client]:
        return db.query(Client).filter(Client.email == email).first()

    def get_by_cpf(self, db: Session, cpf: str) -> Optional[Client]:
        return db.query(Client).filter(Client.cpf == cpf).first()

    def get_multi_filtered(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        name: Optional[str] = None,
        email: Optional[str] = None
    ) -> List[Client]:
        query = db.query(self.model)
        if name:
            query = query.filter(self.model.name.ilike(f"%{name}%"))
        if email:
            query = query.filter(self.model.email.ilike(f"%{email}%"))
        return query.offset(skip).limit(limit).all()

client = CRUDClient(Client)