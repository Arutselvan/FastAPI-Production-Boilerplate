from fastapi import APIRouter

from .import_data import import_router

import_data_router = APIRouter()
import_data_router.include_router(
    import_router,
    tags=["Import"],
)
