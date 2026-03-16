from fastapi import APIRouter

from .tags import tag_router

tags_router = APIRouter()
tags_router.include_router(
    tag_router,
    tags=["Tags"],
)

__all__ = ["tags_router"]
