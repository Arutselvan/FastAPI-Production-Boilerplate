from fastapi import APIRouter, Depends

from core.fastapi.dependencies.authentication import AuthenticationRequired

from .projects import project_router

projects_router = APIRouter()
projects_router.include_router(
    project_router,
    tags=["Projects"],
    dependencies=[Depends(AuthenticationRequired)],
)

__all__ = ["projects_router"]
