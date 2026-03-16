from fastapi import APIRouter, Depends

from core.fastapi.dependencies.authentication import AuthenticationRequired

from .attachments import attachment_router

attachments_router = APIRouter()
attachments_router.include_router(
    attachment_router,
    tags=["Attachments"],
    dependencies=[Depends(AuthenticationRequired)],
)

__all__ = ["attachments_router"]
