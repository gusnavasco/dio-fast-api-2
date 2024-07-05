from fastapi import APIRouter

from tdd_project.controllers.product import router as product

api_router = APIRouter()
api_router.include_router(product, prefix="/products")
