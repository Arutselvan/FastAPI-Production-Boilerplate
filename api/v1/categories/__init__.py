from fastapi import APIRouter

from .categories import category_router

categories_router = APIRouter()
categories_router.include_router(
    category_router,
    tags=["Categories"],
)

__all__ = ["categories_router"]
