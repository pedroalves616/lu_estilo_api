from fastapi import APIRouter

from app.api.v1.endpoints import auth, clients, products, orders, whatsapp

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(clients.router, prefix="/clients", tags=["Clients"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(orders.router, prefix="/orders", tags=["Orders"])
api_router.include_router(whatsapp.router, prefix="/whatsapp", tags=["WhatsApp"])