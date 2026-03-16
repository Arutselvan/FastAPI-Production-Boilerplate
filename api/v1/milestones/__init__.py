from fastapi import APIRouter, Depends

from core.fastapi.dependencies.authentication import AuthenticationRequired

from .milestones import milestone_router

milestones_router = APIRouter()
milestones_router.include_router(
    milestone_router,
    tags=["Milestones"],
    dependencies=[Depends(AuthenticationRequired)],
)

__all__ = ["milestones_router"]
