from fastapi import APIRouter, Depends

from core.fastapi.dependencies.authentication import AuthenticationRequired

from .teams import team_router

teams_router = APIRouter()
teams_router.include_router(
    team_router,
    tags=["Teams"],
    dependencies=[Depends(AuthenticationRequired)],
)

__all__ = ["teams_router"]
