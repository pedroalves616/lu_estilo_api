from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.config import settings
from app.database.session import Base, engine
import uvicorn


app = FastAPI(
    title="Lu Estilo Backend API",
    description="API RESTful para facilitar a comunicação entre o time comercial, os clientes e a empresa Lu Estilo.",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json"
)


app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to Lu Estilo Backend API! Access /api/v1/docs for API documentation."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)