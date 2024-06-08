from fastapi import APIRouter
from app.api.v1.endpoints import (
    connection
)

api_router = APIRouter()
api_router.include_router(connection.router, prefix="/connection", tags=["connection"])
