from fastapi import APIRouter
from src.api.v1.category import router as category_router
from src.api.v1.subcategory import router as subcategory_router


main_router = APIRouter()
main_router.include_router(category_router)
main_router.include_router(subcategory_router)
