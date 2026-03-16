from fastapi import APIRouter, Depends

from core.fastapi.dependencies.authentication import AuthenticationRequired

from .approvals import approval_router

approvals_router = APIRouter()
approvals_router.include_router(
    approval_router,
    tags=["Approvals"],
    dependencies=[Depends(AuthenticationRequired)],
)

__all__ = ["approvals_router"]
