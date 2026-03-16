from fastapi import APIRouter, Depends

from core.fastapi.dependencies.authentication import AuthenticationRequired

from .comments import comment_router

comments_router = APIRouter()
comments_router.include_router(
    comment_router,
    tags=["Comments"],
    dependencies=[Depends(AuthenticationRequired)],
)

__all__ = ["comments_router"]
